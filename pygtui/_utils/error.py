from . import metadata

class error(RuntimeError):

    __module__ = metadata.MODULE_NAME

    def __init__(self, *args):
        if args:
            metadata.ERROR_MESSAGE = str(args[0]) if len(args) == 1 else str(args)
        else:
            metadata.ERROR_MESSAGE = ''

        super().__init__(*args)

def check_initialized():
    if not metadata.INITIALIZE:
        raise error("module not initialized")