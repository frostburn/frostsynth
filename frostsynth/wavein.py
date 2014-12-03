import wave
import array

_sample_type_by_sample_width = {
    1: 'b',
    2: 'h',
    4: 'l'
}

def open(f, mode=None):
    wave_f = wave.open(f, mode)
    if isinstance(wave_f, wave.Wave_read):
        nchannels, sampwidth, framerate, nframes, comptype, compname = wave_f.getparams()
        if nchannels > 1:
            raise ValueError("Only 1 channel supported at the moment.")
        sample_type = _sample_type_by_sample_width[sampwidth]
        samples = array.array(sample_type)
        samples.frombytes(wave_f.readframes(nframes))
        return [sample / (1 << (sampwidth * 8 - 1)) for sample in samples]
    else:
        raise ValueError("Only mode 'r' supported.")
