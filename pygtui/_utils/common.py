def boundary(n, nmin, nmax):
    return max(nmin, min(n, nmax))

def to_milliseconds(seconds):
    return int(seconds * 1000)

def to_seconds(miliseconds):
    return miliseconds / 1000