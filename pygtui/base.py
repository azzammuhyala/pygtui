import time
import sys

from .utils import metadata
from .utils.screen import clear

__version__ = '0.0.1'

def init():
    if not metadata.INITIALIZE:
        metadata.INITIALIZE = True
        metadata.TIME_INITIALIZE = time.time()

def quit():
    if metadata.INITIALIZE:
        sys.stdout.write('\x1b[?25h')

        if metadata.DISPLAY_INSTANCE:
            clear()
            metadata.DISPLAY_INSTANCE = None
        else:
            sys.stdout.flush()

        metadata.INITIALIZE = False

def get_init():
    return metadata.INITIALIZE