def boundary(n, nmin, nmax):
    return max(nmin, min(n, nmax))

def to_milliseconds(seconds):
    return int(seconds * 1000)

def to_seconds(miliseconds):
    return miliseconds / 1000

def to_bytes(value):
    if isinstance(value, bytes):
        return value
    elif isinstance(value, str):
        return value.encode()
    elif isinstance(value, bytearray):
        return bytes(value)
    return None