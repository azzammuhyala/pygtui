import sys
import shutil

import numpy as np

from .utils import metadata
from .utils.error import check_initialized
from .utils.screen import _DisplaySurface, clear as clear, flip as flip

def set_mode(*args, **kwargs):
    return _DisplaySurface(*args, **kwargs)

def set_caption(caption):
    check_initialized()

    sys.stdout.write(f'\x1b]0;{caption}\x07')
    sys.stdout.flush()