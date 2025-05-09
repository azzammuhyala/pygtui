import sys

from ._utils import metadata

from ._utils.error import check_initialized
from ._utils.convert import convert_array_to_ansi

from .constants import CONSTANT
from .surface import Surface

__all__ = [
    'set_mode',
    'set_caption',
    'clear',
    'flip'
]

def set_mode(size, flags=0):
    check_initialized()

    metadata.SURFACE_INSTANCE = Surface(size, CONSTANT)

    sys.stdout.write('\x1b[?25l')
    clear()

    return metadata.SURFACE_INSTANCE

def set_caption(caption):
    check_initialized()

    sys.stdout.write(f'\x1b]0;{caption}\x07')
    sys.stdout.flush()

def clear():
    check_initialized()

    if metadata.SURFACE_INSTANCE:
        sys.stdout.write('\x1b[2J\x1b[H')
        sys.stdout.flush()

def flip():
    check_initialized()

    surface = metadata.SURFACE_INSTANCE
    if surface:
        sys.stdout.write('\x1b[H')
        sys.stdout.write(convert_array_to_ansi(surface.array))
        sys.stdout.flush()