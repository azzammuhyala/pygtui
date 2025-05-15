import sys

from ._utils import metadata

__version__ = '0.0.1'
__all__ = [
    'error',
    'init',
    'quit',
    'get_init',
    'get_error',
    'set_error',
    '__version__'
]

class error(RuntimeError):
    __module__ = metadata.MODULE_NAME

def init():
    if not metadata.INITIALIZE:
        metadata.INITIALIZE = True

def quit():
    if metadata.INITIALIZE:

        if metadata.SURFACE_INSTANCE:
            sys.stdout.write('\x1b[2J\x1b[H\x1b[?25h')
            sys.stdout.flush()

            metadata.SURFACE_INSTANCE = None

        metadata.INITIALIZE = False

def get_init():
    return metadata.INITIALIZE

def get_error():
    return metadata.ERROR_MESSAGE

def set_error(message):
    metadata.ERROR_MESSAGE = str(message)