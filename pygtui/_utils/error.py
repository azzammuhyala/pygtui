from . import metadata

class error(RuntimeError):
    pass

def check_initialized():
    if not metadata.INITIALIZE:
        raise error("module not initialized")