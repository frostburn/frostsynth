def _separate_bytes2(iterable):
    iterable = iter(iterable)
    while True:
        v = int(next(iterable) * 32767)
        yield v & 255
        yield (v >> 8) & 255

def iter_dumps(iterable, width=2):
    """Converts numbers from iterable in the range from -1 to 1 into signed integers 'width' wide. And dumps them into a string or a bytearray."""
    if width==1:
        return bytearray(map(lambda x: int(x * 127) & 255, iterable))
    elif width==2:
        return bytearray(_separate_bytes2(iterable))
    
    raise ValueError("Only widths 1 and 2 supported.")
