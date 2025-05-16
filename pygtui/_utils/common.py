from ..base import error
from . import metadata

def boundary(n, nmin, nmax):
    return max(nmin, min(n, nmax))

def bounds(n, nmin, nmax):
    return nmin <= n <= nmax

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

def checker(name, message):
    def check(func):
        def wrapper(*args, **kwargs):
            if not getattr(metadata, name, False):
                raise error(message)
            return func(*args, **kwargs)
        return wrapper
    return check

_singleton_instances = {}
class Singleton:
    def __new__(cls, *args, **kwargs):
        if cls not in _singleton_instances:
            _singleton_instances[cls] = super().__new__(cls)
        return _singleton_instances[cls]