/*
    /dev/input enabled jack client by Lumi Pakkanen.

    Makefile? Just gcc client.c -lm -ljack -O3

    Based on an example client by Ian Esten.
*/

/*
    Copyright (C) 2004 Ian Esten
    
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
*/

#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <fcntl.h>
#include <linux/input.h>

#include <jack/jack.h>
#include <jack/midiport.h>

#define INIT_BUTTON (129)
#define INIT_AXIS (130)
#define BUTTON (1)
#define AXIS (2)

#define NONE (-555)

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))

typedef struct joy_description {
    unsigned short time;
    int num_buttons;
    int num_axis;
} joy_description;

typedef struct joy_event {
    unsigned short time;
    unsigned short code;
    signed short axis;
    unsigned char type;
    unsigned char num;
} joy_event;

int fd;

int init_joy(joy_description* joy_desc)
{
    int i;
    joy_event ev[64];
    int rb = read(fd, ev, sizeof(joy_event) * 64);
    if (rb < 0){
        return rb;
    }
    else {
        joy_desc->time = 0;
        joy_desc->num_buttons = 0;
        joy_desc->num_axis = 0;
        for (i=0; i < rb / sizeof(joy_event); i++){
            if (i==0){
                joy_desc->time = ev[i].time;
            }
            if (ev[i].type == INIT_BUTTON){
                joy_desc->num_buttons += 1;
            }
            else if (ev[i].type == INIT_AXIS){
                joy_desc->num_axis += 1;
            }
            else {
                printf("Unkown event type %d encountered during joy initialization.\n", ev[i].type);
            }
        }
    }
    return 0;
}

#define TABLE_SIZE (1024)
double SIN_TABLE[TABLE_SIZE];
double COS_TABLE[TABLE_SIZE];

void init_tables()
{
    size_t i;
    for (i = 0; i < TABLE_SIZE; i++){
        SIN_TABLE[i] = sin(2 * M_PI * i / (double) TABLE_SIZE);
        COS_TABLE[i] = cos(2 * M_PI * i / (double) TABLE_SIZE);
    }
}

double sine(double x)
{
    x = x * TABLE_SIZE;
    double floor_x = floor(x);
    size_t index = ((size_t)floor_x) & (TABLE_SIZE - 1);
    return SIN_TABLE[index] + (SIN_TABLE[(index + 1) & (TABLE_SIZE - 1)] - SIN_TABLE[index]) * (x - floor_x);
}

double cosine(double x)
{
    x = x * TABLE_SIZE;
    double floor_x = floor(x);
    size_t index = ((size_t)floor_x) & (TABLE_SIZE - 1);
    return COS_TABLE[index] + (COS_TABLE[(index + 1) & (TABLE_SIZE - 1)] - COS_TABLE[index]) * (x - floor_x);
}

double frand()
{
    return 2.0 * rand() / (double)RAND_MAX - 1.0;
}

long long current_block = 0;
double t = 0.0;
int accidental = 0;
int octave = 0;
double pitch_bend = 0.0;
double modulation = 0.0;
double volume = 0.0;
double smooth_volume = 0.0;
double tremolo = 0.0;
double a = 0.0;
double sa = 0.0;
double b = 0.0;
double sb = 0.0;

#define MAX_POLYPHONY (128)
#define VOICES (3)
#define FADE_TIME (0.2)
int note_on_key[MAX_POLYPHONY];
double phases[MAX_POLYPHONY * VOICES];
double _deltas[MAX_POLYPHONY * VOICES];
double freqs[MAX_POLYPHONY];
double note_on_times[MAX_POLYPHONY];
double note_off_times[MAX_POLYPHONY];


//jack_port_t *input_port;
jack_port_t *output_port;

jack_default_audio_sample_t SAMPDELTA;


void calc_note_frqs(jack_default_audio_sample_t srate)
{
    SAMPDELTA = 1.0 / srate;
}

void reset_notes()
{
    int i, j;
    for (i=0; i < MAX_POLYPHONY; i++){
        note_on_key[i] = NONE;
        for (j = 0; j < VOICES; j++){
            phases[i + MAX_POLYPHONY * j] = 0.0;
        }
        freqs[i] = 0.0;
        note_on_times[i] = -INFINITY;
        note_off_times[i] = -INFINITY;
    }
}

int find_free_index()
{
    int i;
    for (i=0; i < MAX_POLYPHONY; i++){
        if (note_off_times[i] + FADE_TIME < t){
            return i;
        }
    }
    for (i=0; i < MAX_POLYPHONY; i++){
        if (note_off_times[i] <= t){
            return i;
        }
    }
    return 0;
}

int major_scale(int num)
{
    switch (num){
        case 0:
            return 0;
        case 1:
            return 2;
        case 2:
            return 4;
        case 3:
            return 5;
        case 4:
            return 7;
        case 5:
            return 9;
        case 6:
            return 11;
        default:
            if (num < 0){
                return major_scale(num + 7) - 12;
            }
            else {
                return major_scale(num - 7) + 12;
            }
    }
}

int minor_scale(int num){
    return major_scale(num - 2) + 4;
}

double get_freq(joy_event e)
{
    if (e.type == BUTTON){
        int key = minor_scale(e.num) + accidental + 12 * octave;
        return 220 * pow(2, (double)key / 12.0);
    }
    else {
        return 0.0;
    }
}

int process(jack_nframes_t nframes, void *arg)
{
    int i, j, k;
    joy_event ev[64];
    int rb;
    int next_index;
    double result, amplitude, bend_ratio, wf, aa, bb, x, note_on_t, note_off_t;
    jack_default_audio_sample_t *out = (jack_default_audio_sample_t *) jack_port_get_buffer (output_port, nframes);
    current_block++;
    rb = read(fd, ev, sizeof(joy_event) * 64);
    if (rb > 0){
        rb /= sizeof(joy_event);
        //printf("hi, %d events at %lld\n", rb, current_block);
        for (j=0; j < rb; j++){
            //printf("code %d\ntime %d\naxis %d\ntype %d\nnum %d\n\n", ev[j].code, ev[j].time, ev[j].axis, ev[j].type, ev[j].num);
            if (ev[j].type == BUTTON){
                if (ev[j].axis){
                    next_index = find_free_index();
                    note_on_key[next_index] = ev[j].num;
                    for (k = 0; k < VOICES; k++){
                        phases[next_index + MAX_POLYPHONY * k] = 0.0;
                    }
                    freqs[next_index] = get_freq(ev[j]);
                    note_on_times[next_index] = t;
                    note_off_times[next_index] = INFINITY;
                }
                else {
                    for (k=0; k < MAX_POLYPHONY; k++){
                        if (note_on_key[k] == ev[j].num){
                            note_off_times[k] = t;
                            note_on_key[k] = NONE;
                        }
                    }
                }
            }
            else if (ev[j].type == AXIS){
                if (ev[j].num == 6){
                    accidental = MAX(-1, MIN(1, ev[j].axis));
                }
                else if (ev[j].num == 7){
                    octave += MAX(-1, MIN(1, -ev[j].axis));
                }
                else if (ev[j].num == 2){
                    a = 0.5 + 0.5 * (ev[j].axis / 32767.0);
                }
                else if (ev[j].num == 5){
                    b = 0.5 + 0.5 * (ev[j].axis / 32767.0);
                }
                else if (ev[j].num == 0){
                    pitch_bend = 1.0 * ev[j].axis / 32767.0;
                }
                else if (ev[j].num == 1){
                    modulation = 0.5 * ev[j].axis / 32767.0;
                }
                else if (ev[j].num == 3){
                    volume = ev[j].axis / 32767.0;
                }
                else if (ev[j].num == 4){
                    tremolo = 0.5 * ev[j].axis / 32767.0;
                }
            }
        }
    }
    bend_ratio = pow(2.0, (pitch_bend + sine(7 * t) * modulation) / 12.0);
    for (i = 0; i < MAX_POLYPHONY; i++){
        double delta = freqs[i] * bend_ratio * SAMPDELTA;
        for (j = 0; j < VOICES; j++){
            _deltas[i + j * MAX_POLYPHONY] = delta * pow(2.0, frand() * 0.04);
        }
    }
    for (i = 0; i<nframes; i++){
        result = 0.0;
        for (j = 0; j < MAX_POLYPHONY; j++){
            if (note_off_times[j] + FADE_TIME > t){
                note_on_t = t - note_on_times[j];
                if (note_off_times[j] > t){
                    note_off_t = 0.0;
                }
                else {
                    note_off_t = t - note_off_times[j];
                }
                wf = 0.0;
                for (k = 0; k < VOICES; k++){
                    int index = j + k * MAX_POLYPHONY;
                    double x = phases[index];
                    x = x + 1.2 * sb * sine(2 * x + 2 * t);
                    double s = 0.5 + sa * 0.478;
                    wf += atan(s * sine(x) / (1.0 + s * cosine(x))) / asin(s);
                    wf += sine(phases[index]);
                    phases[index] += _deltas[index];
                }
                wf *= 0.4;
                result += wf * 0.2 * MAX(0, 1.0 - note_off_t / 0.1);
            }
        }
        sa = 0.8 * sa + 0.2 * a;
        sb = 0.8 * sb + 0.2 * b;
        smooth_volume = 0.8 * smooth_volume + 0.2 * volume;
        amplitude = 0.5 + 0.5 * smooth_volume;
        result *= amplitude * (1.0 + cosine(7 * t) * tremolo);
        out[i] = (jack_default_audio_sample_t) result;
        t += SAMPDELTA;
    }
    return 0;
}

int srate(jack_nframes_t nframes, void *arg)
{
    printf("the sample rate is now %" PRIu32 "/sec\n", nframes);
    calc_note_frqs((jack_default_audio_sample_t)nframes);
    return 0;
}

void jack_shutdown(void *arg)
{
    exit(1);
}

int main(int narg, char **args)
{
    fd = open("/dev/input/js0", O_RDONLY);
    if (fd > 0){
        printf("Device open at /dev/input/js0\n");
    }
    else {
        printf("Cannot open device at /dev/input/js0\n");
        exit(-1);
    }
    int flags = fcntl(fd, F_GETFL, 0);
    if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0){
        printf("Error setting non-blocking mode\n");
        exit(-1);
    }
    joy_description joy_desc;
    init_joy(&joy_desc);
    printf("time %d\nnumber of buttons %d\nnumber of axis %d\n\n", joy_desc.time, joy_desc.num_buttons, joy_desc.num_axis);

    init_tables();

    const char **ports;
    jack_client_t *client;

    if ((client = jack_client_new("joydev")) == 0)
    {
        fprintf(stderr, "jack server not running?\n");
        return 1;
    }

    reset_notes();

    calc_note_frqs(jack_get_sample_rate (client));

    jack_set_process_callback (client, process, 0);

    jack_set_sample_rate_callback (client, srate, 0);

    jack_on_shutdown (client, jack_shutdown, 0);

    //input_port = jack_port_register (client, "midi_in", JACK_DEFAULT_MIDI_TYPE, JackPortIsInput, 0);
    output_port = jack_port_register (client, "audio_out", JACK_DEFAULT_AUDIO_TYPE, JackPortIsOutput, 0);

    if (jack_activate (client))
    {
        fprintf(stderr, "cannot activate client");
        return 1;
    }

    ports = jack_get_ports (client, NULL, NULL,
                JackPortIsPhysical|JackPortIsInput);
    if (ports == NULL) {
        fprintf(stderr, "no physical playback ports\n");
        exit (1);
    }

    if (jack_connect (client, jack_port_name (output_port), ports[0])) {
        fprintf (stderr, "cannot connect output ports\n");
    }
    if (jack_connect (client, jack_port_name (output_port), ports[1])) {
        fprintf (stderr, "cannot connect output ports\n");
    }

    free (ports);

    /* run until interrupted */
    while(1)
    {
        sleep(1);
    }
    jack_client_close(client);
    close(fd);
    exit (0);
}

