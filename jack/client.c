/*
    /dev/input/ enabled jack client by Lumi Pakkanen (2015).

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

typedef enum {NOTE_ON, NOTE_OFF, PITCH_BEND, MODULATION, PITCH_BEND2, MODULATION2, VOLUME, TREMOLO, PARAM_A, PARAM_B} event_t;

typedef struct track_event {
    event_t type;
    long long sample;
    int key;
    double frequency;
    double value;
    int time_tag;
} track_event;

track_event *track_events;
size_t track_index;
size_t track_size;

void init_track_events()
{
    track_size = 1;
    track_events = (track_event*) malloc(sizeof(track_event) * track_size);
    track_index = 0;
}

void track_next()
{
    track_index++;
    if (track_index >= track_size){
        track_size <<= 1;
        track_events = (track_event*) realloc(track_events, sizeof(track_event) * track_size);
    }
}

/*
void track_note(long long sample, long long note_off_sample, double frequency, double velocity, double note_off_velocity, int time_tag, int note_off_time_tag)
{
    track_events[track_index].type = NOTE;
    track_events[track_index].sample = sample;
    track_events[track_index].note_off_sample = note_off_sample;
    track_events[track_index].frequency = frequency;
    track_events[track_index].value = velocity;
    track_events[track_index].note_off_velocity = note_off_velocity;
    track_events[track_index].time_tag = time_tag;
    track_events[track_index].note_off_time_tag = note_off_time_tag;

    track_next();
}
*/

void track_note(event_t type, long long sample, int key, double frequency, double velocity, int time_tag)
{
    track_events[track_index].type = type;
    track_events[track_index].sample = sample;
    track_events[track_index].key = key;
    track_events[track_index].frequency = frequency;
    track_events[track_index].value = velocity;
    track_events[track_index].time_tag = time_tag;

    track_next();
}

void track_simple(event_t type, long long sample, double value, int time_tag)
{
    track_events[track_index].type = type;
    track_events[track_index].sample = sample;
    track_events[track_index].value = value;
    track_events[track_index].time_tag = time_tag;

    track_next();
}

jack_default_audio_sample_t SRATE;
jack_default_audio_sample_t SAMPDELTA;
unsigned short INITIAL_TIME_TAG;

void track_dump_and_free()
{
    size_t i;
    char *type;
    FILE *outfile = fopen("events.json", "w");
    if (outfile == NULL){
        printf("Cannot open events.json\n");
        return;
    }
    fprintf(outfile, "{\"sampling rate\": %g,\n\"initial time tag\": %d,\n\"events\": [\n", SRATE, INITIAL_TIME_TAG);
    for (i = 0; i < track_index; i++){
        track_event e = track_events[i];
        if (e.type == NOTE_ON || e.type == NOTE_OFF){
            switch (e.type){
                case NOTE_ON:
                    type = "note on";
                    break;
                case NOTE_OFF:
                    type = "note off";
                    break;
                default:
                    type = "unknown note event";
            }
            fprintf(
                outfile, "{\"type\": \"%s\", \"sample\": %lld, \"key\": %d, \"frequency\": %g, \"velocity\": %g, \"time tag\": %d}",
                type, e.sample, e.key, e.frequency, e.value, e.time_tag
            );
        }
        else {
            switch (e.type){
                case PITCH_BEND:
                    type = "pitch bend";
                    break;
                case MODULATION:
                    type = "modulation";
                    break;
                case PITCH_BEND2:
                    type = "pitch bend 2";
                    break;
                case MODULATION2:
                    type = "modulation 2";
                    break;
                case VOLUME:
                    type = "volume";
                    break;
                case TREMOLO:
                    type = "tremolo";
                    break;
                case PARAM_A:
                    type = "param a";
                    break;
                case PARAM_B:
                    type = "param b";
                    break;
                default:
                    type = "unknown";
            }
            fprintf(outfile, "{\"type\": \"%s\", \"sample\": %lld, \"value\": %g, \"time tag\": %d}", type, e.sample, e.value, e.time_tag);
        }
        if (i < track_index - 1){
            fprintf(outfile, ",");
        }
        fprintf(outfile, "\n");
    }
    fprintf(outfile, "]\n}\n");
    if (fclose(outfile) != 0){
        printf("Error closing events.json\n");
    }
    free(track_events);
    track_index = -1;
    track_size = -1;
}

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

#define BUFFER_LENGTH (4410)
typedef struct KS_string
{
    double buffer[BUFFER_LENGTH];
    int i;
    int l;
    double y0;
    double y1;
    double ratio;
    double mu;
} KS_string;

long long current_block = 0;
long long sample = 0;
double t = 0.0;
int accidental = 0;
int octave = 0;
double pitch_bend = 0.0;
double modulation = 0.0;
double pitch_bend2 = 0.0;
double modulation2 = 0.0;
double volume = 0.0;
double smooth_volume = 0.0;
double tremolo = 0.0;
double a = 0.0;
double sa = 0.0;
double b = 0.0;
double sb = 0.0;


#define MAX_POLYPHONY (128)
#define MAX_VOICES (3)
#define FADE_TIME (0.5)
int program_number = 0;
int current_voices = 3;
int note_on_keys[MAX_POLYPHONY];
double phases[MAX_POLYPHONY * MAX_VOICES];
double phase_deltas[MAX_POLYPHONY * MAX_VOICES];
double freqs[MAX_POLYPHONY];
double note_on_times[MAX_POLYPHONY];
long long note_on_samples[MAX_POLYPHONY];
unsigned short note_on_time_tags[MAX_POLYPHONY];
double note_on_velocities[MAX_POLYPHONY];
double note_off_times[MAX_POLYPHONY];
double note_off_velocities[MAX_POLYPHONY];
KS_string KS_strings[MAX_POLYPHONY];


jack_port_t *input_port;
jack_port_t *output_port;

void calc_note_frqs(jack_default_audio_sample_t srate)
{
    SRATE = srate;
    SAMPDELTA = 1.0 / srate;
}

void reset_notes()
{
    int i, j;
    for (i=0; i < MAX_POLYPHONY; i++){
        note_on_keys[i] = NONE;
        for (j = 0; j < MAX_VOICES; j++){
            phases[i + MAX_POLYPHONY * j] = 0.0;
        }
        freqs[i] = 0.0;
        note_on_times[i] = -INFINITY;
        note_off_times[i] = -INFINITY;
        KS_string *s = KS_strings + i;
        for (j = 0; j < BUFFER_LENGTH; j++){
            s->buffer[j] = 0.0;
        }
        s->i = 0;
        s->l = BUFFER_LENGTH;
        s->y0 = 0.0;
        s->y1 = 0.0;
        s->ratio = 1.0;
        s->mu = 0.0;
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

double get_midi_freq(int key)
{
    return 440 * pow(2, (key - 69) / 12.0);
}

void change_program(int num){
    program_number = num;
    switch (program_number){
        case 0:
            current_voices = 3;
            break;
        case 1:
            current_voices = 1;
            break;
        case 2:
            current_voices = 1;
            break;
        default:
            printf("Unknown program number %d\n", program_number);
    }
}

void init_note(int index)
{
    int i, j;
    if (program_number == 0){
        for (i = 0; i < current_voices; i++){
            phases[index + i * MAX_POLYPHONY] = 0.0;
        }
    }
    else if (program_number == 1 || program_number == 2){
        phases[index] = 0.0;
    }
    else if (program_number == 3){
        double v = note_on_velocities[index];
        KS_string *s = KS_strings + index;
        for (i = 0; i < BUFFER_LENGTH; i++){
            s->buffer[i] = frand() * v * v;
        }
        double l = SRATE / freqs[index];
        s->i = 0;
        s->l = (int)ceil(l);
        for (i = 0; pow(i, 1.5 + 0.5 * v) < s->l; i++){
            for (j = 0; j < s->l; j++){
                s->buffer[j] = s->buffer[j] * 0.5 + 0.25 * (s->buffer[(j + s->l - 1) % s->l] + s->buffer[(j + 1) % s->l]);
            }
        }
        for (i = 0; i < s->l; i++){
            double x = i / (double)s->l;
            s->buffer[i] += sine(x + tanh(sine(2 * x) * (0.5 + v))) * v * 0.3;
        }
        s->y0 = 0.0;
        s->y1 = 0.0;
        s->ratio = ceil(l) / l;
        s->mu = 0.0;
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
    // read /dev/input/
    if (fd > 0){
        rb = read(fd, ev, sizeof(joy_event) * 64);
    }
    else {
        rb = -2;
    }
    if (rb > 0){
        rb /= sizeof(joy_event);
        //printf("hi, %d events at %lld\n", rb, current_block);
        for (j=0; j < rb; j++){
            //printf("code %d\ntime %d\naxis %d\ntype %d\nnum %d\n\n", ev[j].code, ev[j].time, ev[j].axis, ev[j].type, ev[j].num);
            if (ev[j].type == BUTTON){
                if (ev[j].num < 9){
                    if (ev[j].axis){
                        next_index = find_free_index();
                        note_on_keys[next_index] = -ev[j].num - 1;
                        freqs[next_index] = get_freq(ev[j]);
                        note_on_times[next_index] = t;
                        note_on_samples[next_index] = sample;
                        note_off_times[next_index] = INFINITY;
                        note_on_time_tags[next_index] = ev[j].time;
                        note_on_velocities[next_index] = 0.7;
                        init_note(next_index);
                        track_note(NOTE_ON, sample, note_on_keys[next_index], freqs[next_index], note_on_velocities[next_index], ev[j].time);
                    }
                    else {
                        for (k=0; k < MAX_POLYPHONY; k++){
                            if (note_on_keys[k] == -ev[j].num - 1){
                                note_off_velocities[k] = 0.7;
                                track_note(NOTE_OFF, sample, note_on_keys[k], freqs[k], note_off_velocities[k], ev[j].time);
                                note_off_times[k] = t;
                                note_on_keys[k] = NONE;
                            }
                        }
                    }
                }
                else if (ev[j].axis){
                    if (ev[j].num == 9){
                        octave--;
                        printf("octave down to %d\n", octave);
                    }
                    else if (ev[j].num == 10){
                        octave++;
                        printf("octave up to %d\n", octave);
                    }
                }
            }
            else if (ev[j].type == AXIS){
                if (ev[j].num == 6){
                    accidental = MAX(-1, MIN(1, ev[j].axis));
                }
                else if (ev[j].num == 7){
                    //octave += MAX(-1, MIN(1, -ev[j].axis));
                }
                else if (ev[j].num == 2){
                    a = 0.5 + 0.5 * (ev[j].axis / 32767.0);
                    track_simple(PARAM_A, sample, a, ev[j].time);
                }
                else if (ev[j].num == 5){
                    b = 0.5 + 0.5 * (ev[j].axis / 32767.0);
                    track_simple(PARAM_B, sample, b, ev[j].time);
                }
                else if (ev[j].num == 0){
                    pitch_bend = 1.0 * ev[j].axis / 32767.0;
                    track_simple(PITCH_BEND, sample, pitch_bend, ev[j].time);
                }
                else if (ev[j].num == 1){
                    modulation = 0.5 * ev[j].axis / 32767.0;
                    track_simple(MODULATION, sample, modulation, ev[j].time);
                }
                else if (ev[j].num == 3){
                    volume = ev[j].axis / 32767.0;
                    track_simple(VOLUME, sample, volume, ev[j].time);
                }
                else if (ev[j].num == 4){
                    tremolo = 0.5 * ev[j].axis / 32767.0;
                    track_simple(TREMOLO, sample, tremolo, ev[j].time);
                }
            }
        }
    }
    // read midi
    void* port_buf = jack_port_get_buffer(input_port, nframes);
    jack_midi_event_t in_event;
    jack_nframes_t event_index = 0;
    jack_nframes_t event_count = jack_midi_get_event_count(port_buf);
    if (event_count > 0){
        //printf(" have %d midi events\n", event_count);
        for (event_index = 0; event_index < event_count; event_index++){
            jack_midi_event_get(&in_event, port_buf, event_index);
            //printf("    event %d time is %d, size is %zu\n", event_index, in_event.time, in_event.size);
            //for (i = 0; i < in_event.size; i++){
            //    printf("    byte %d is 0x%x\n", i, in_event.buffer[i]);
            //}
            unsigned char channel = in_event.buffer[0] & 0x0f;
            unsigned char type = in_event.buffer[0] & 0xf0;
            long long event_sample = sample + in_event.time;
            if (type == 0x90){
                next_index = find_free_index();
                note_on_keys[next_index] = in_event.buffer[1];
                freqs[next_index] = get_midi_freq(in_event.buffer[1]);
                note_on_times[next_index] = t + in_event.time * SAMPDELTA;
                note_on_samples[next_index] = event_sample;
                note_off_times[next_index] = INFINITY;
                note_on_time_tags[next_index] = -1;
                note_on_velocities[next_index] = in_event.buffer[2] / 127.0;
                init_note(next_index);
                track_note(NOTE_ON, note_on_samples[next_index], note_on_keys[next_index], freqs[next_index], note_on_velocities[next_index], -1);
            }
            else if (type == 0x80){
                for (k = 0; k < MAX_POLYPHONY; k++){
                    if (note_on_keys[k] == in_event.buffer[1]){
                        note_off_velocities[k] = in_event.buffer[2] / 127.0;
                        track_note(NOTE_OFF, event_sample, note_on_keys[k], freqs[k], note_off_velocities[k], -1);
                        note_off_times[k] = t + in_event.time * SAMPDELTA;
                        note_on_keys[k] = NONE;
                    }
                }
            }
            else if (type == 0xb0){
                unsigned char controller_number = in_event.buffer[1];
                if (controller_number == 0x01){
                    modulation2 = in_event.buffer[2] / 127.0;
                    track_simple(MODULATION2, event_sample, modulation2, -1);
                }
                if (controller_number == 0x78 || controller_number >= 0x7c){
                    for (k = 0; k < MAX_POLYPHONY; k++){
                        if (note_on_keys[k] >= 0){
                            note_off_velocities[k] = 1.0;
                            track_note(NOTE_OFF, event_sample, note_on_keys[k], freqs[k], note_off_velocities[k], -1);
                            note_off_times[k] = t + in_event.time * SAMPDELTA;
                            note_on_keys[k] = NONE;
                        }
                    }
                }
            }
            else if (type == 0xe0){
                int lsb = in_event.buffer[1];
                int msb = in_event.buffer[2];
                //int value = lsb + msb * 128 - 8192;
                if (msb < 64){
                    pitch_bend2 = 2 * (msb - 64) / 64.0;
                }
                else {
                    pitch_bend2 = 2 * (msb - 64) / 63.0;
                }
                track_simple(PITCH_BEND2, event_sample, modulation2, -1);
            }
            else if (type == 0xc0){
                change_program(in_event.buffer[1]);
            }
        }
    }
    bend_ratio = pow(2.0, (pitch_bend + pitch_bend2 + sine(7 * t) * (modulation + modulation2)) / 12.0);
    for (i = 0; i < MAX_POLYPHONY; i++){
        double delta = freqs[i] * bend_ratio * SAMPDELTA;
        if (program_number == 0){
            for (j = 0; j < current_voices; j++){
                phase_deltas[i + j * MAX_POLYPHONY] = delta * pow(2.0, frand() * 0.04);
            }
        }
        else if (program_number == 1){
            phase_deltas[i] = delta * pow(2, frand() * 0.01);
        }
        else if (program_number == 2){
            phase_deltas[i] = delta * pow(2, frand() * 0.005);
        }
    }
    for (i = 0; i<nframes; i++){
        result = 0.0;
        for (j = 0; j < MAX_POLYPHONY; j++){
            if (note_on_times[j] <= t && note_off_times[j] + FADE_TIME > t){
                note_on_t = t - note_on_times[j];
                double note_off_velocity;
                if (note_off_times[j] > t){
                    note_off_t = 0.0;
                    note_off_velocity = 0.0;
                }
                else {
                    note_off_t = t - note_off_times[j];
                    note_off_velocity = note_on_velocities[j];
                }
                double note_on_velocity = note_on_velocities[j];

                if (program_number == 0){
                    wf = 0.0;
                    for (k = 0; k < current_voices; k++){
                        double x = phases[j + k * MAX_POLYPHONY];
                        x = x + 1.2 * sb * sine(2 * x + 2 * t);
                        double s = 0.5 + sa * 0.478;
                        wf += atan(s * sine(x) / (1.0 + s * cosine(x))) / asin(s);
                    }
                    result += note_on_velocity * wf * 0.1 * MAX(0, 1.0 - note_off_t / 0.1);
                }
                else if (program_number == 1){
                    double x = phases[j];
                    result += 0.5 * note_on_velocity * sine(x + sine(x) * exp(-3 * note_on_t) * note_on_velocity) * exp(-note_on_t) * MAX(0, 1.0 - note_off_t / (0.2 - 0.1 * note_on_velocity));
                }
                else if (program_number == 2){
                    double x = phases[j];
                    result += 0.5 * MIN(1, note_on_t * 500) *
                              tanh(note_on_velocity * 3 *
                                sine(3 * x + (sine(2 * x + t) + sine(5 * x - t) * 0.6 * note_on_velocity) * 0.6 * exp(-4 * note_on_t) * note_on_velocity) * exp(-note_on_t)
                              ) * 
                              sqrt(note_on_velocity) * exp(-2 * note_on_t) * MAX(0, 1.0 - note_off_t * 10);
                }
                else if (program_number == 3){
                    KS_string *s = KS_strings + j;
                    s->mu += s->ratio * bend_ratio;
                    while (s->mu > 1.0){
                        s->y1 = s->y0;
                        if (note_off_t <= 0){
                            s->y0 = (s->y0 * 0.3 + 0.7 * s->buffer[s->i]) / (1.0 + 0.0001 * s->l);
                        }
                        else {
                            s->y0 = (s->y0 * 0.5 + 0.5 * s->buffer[s->i]) / (1.0 + 0.0001 * s->l);
                        }
                        s->buffer[s->i] = s->y0;
                        s->i = (s->i + 1) % s->l;
                        s->mu -= 1.0;
                    }
                    result += s->y1 + s->mu * (s->y0 - s->y1);
                }

                for (k = 0; k < current_voices; k++){
                    int index = j + k * MAX_POLYPHONY;
                    phases[index] += phase_deltas[index];
                }

            }
        }
        sa = 0.8 * sa + 0.2 * a;
        sb = 0.8 * sb + 0.2 * b;
        smooth_volume = 0.8 * smooth_volume + 0.2 * volume;
        amplitude = 0.5 + 0.5 * smooth_volume;
        result *= amplitude * (1.0 + cosine(7 * t) * tremolo);
        if (program_number == 1){
            result = 0.7 * result + 0.3 * tanh(12 * result);
        }
        out[i] = (jack_default_audio_sample_t) result;
        t += SAMPDELTA;
        current_block++;
        sample += nframes;
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
        int flags = fcntl(fd, F_GETFL, 0);
        if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0){
            printf("Error setting non-blocking mode\n");
            exit(-1);
        }
        joy_description joy_desc;
        init_joy(&joy_desc);
        INITIAL_TIME_TAG = joy_desc.time;
        printf("time %d\nnumber of buttons %d\nnumber of axis %d\n\n", joy_desc.time, joy_desc.num_buttons, joy_desc.num_axis);
    }
    else {
        printf("Cannot open device at /dev/input/js0\n");
        //exit(-1);
    }

    init_track_events();
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

    input_port = jack_port_register (client, "midi_in", JACK_DEFAULT_MIDI_TYPE, JackPortIsInput, 0);
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
    /*
    while(1)
    {
        sleep(1);
    }
    */
    printf("press enter to quit\n");
    getchar();
    printf("shutting down\n");
    jack_client_close(client);
    close(fd);
    track_dump_and_free();
    exit (0);
}

