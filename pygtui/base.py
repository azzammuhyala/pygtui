import sys

from typing import Callable
from importlib import import_module

from ._utils import metadata

__version__ = '0.0.1'
__all__ = [
    'error',
    'BufferError',
    'init',
    'quit',
    'get_init',
    'get_error',
    'set_error',
    'register_quit',
    '__version__'
]

class error(RuntimeError):
    __module__ = metadata.MODULE_NAME

class BufferError(Exception):
    __module__ = metadata.MODULE_NAME

def _callshorcut(callname):
    success = 0
    fails = 0

    for name_module in metadata.MODULES:
        if name_module == 'base':
            continue

        full_module_name = metadata.MODULE_NAME + '.' + name_module

        if full_module_name not in sys.modules:
            import_module(full_module_name)

        try:
            func = getattr(sys.modules[full_module_name], callname, None)
            if isinstance(func, Callable):
                func()
                success += 1
        except:
            fails += 1

    metadata.INITIALIZE = callname == 'init'

    return (success, fails)

def init():
    return _callshorcut('init')

def quit():
    try:
        metadata.QUIT_CALLABLE()
    except:
        pass

    return _callshorcut('quit')

def get_init():
    return metadata.INITIALIZE

def get_error():
    return metadata.ERROR_MESSAGE

def set_error(message):
    metadata.ERROR_MESSAGE = str(message)

def register_quit(callable):
    metadata.QUIT_CALLABLE = callable