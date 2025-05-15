import sys

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
    for name_module in metadata.MODULES:
        if name_module == 'base':
            continue

        try:
            full_module_name = metadata.MODULE_NAME + '.' + name_module

            if full_module_name not in sys.modules:
                import_module(full_module_name)

            getattr(sys.modules[full_module_name], callname, None)()
        except:
            pass

def init():
    _callshorcut('init')
    metadata.INITIALIZE = True

def quit():
    try:
        metadata.QUIT_CALLABLE()
    except:
        pass

    _callshorcut('quit')
    metadata.INITIALIZE = False

def get_init():
    return metadata.INITIALIZE

def get_error():
    return metadata.ERROR_MESSAGE

def set_error(message):
    metadata.ERROR_MESSAGE = str(message)

def register_quit(callable):
    metadata.QUIT_CALLABLE = callable