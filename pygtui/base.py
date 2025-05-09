import sys

from ._utils import metadata

__version__ = '0.0.1'
__all__ = [
    'init',
    'quit',
    'get_init',
    'get_error',
    'set_error',
    '__version__'
]

def init():
    if not metadata.INITIALIZE:
        metadata.INITIALIZE = True

def quit():
    if metadata.INITIALIZE:
        sys.stdout.write('\x1b[?25h')

        if metadata.SURFACE_INSTANCE:
            from .display import clear
            clear()
            metadata.SURFACE_INSTANCE = None
        else:
            sys.stdout.flush()

        metadata.INITIALIZE = False

def get_init():
    return metadata.INITIALIZE

def get_error():
    return metadata.ERROR_MESSAGE

def set_error(message):
    metadata.ERROR_MESSAGE = str(message)