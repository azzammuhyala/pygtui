from .error import error

def boundary(n, nmin, nmax):
    return max(nmin, min(n, nmax))

def ensure_seq(sequence, k):
    sequence = list(sequence)
    length = len(sequence)

    if length != k:
        raise error(f"length sequence must be equal to {k}, got {length}")

    return sequence

def name(obj):
    return type(obj).__name__

def to_milliseconds(seconds):
    return int(seconds * 1000)

def to_seconds(miliseconds):
    return miliseconds / 1000