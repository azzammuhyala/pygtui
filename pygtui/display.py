import sys

import numpy as np

from typing import Sequence

from ._utils import metadata

from ._utils.error import check_initialized
from ._utils.convert import convert_array_to_ansi

from .constants import CONSTANT
from .rect import Rect
from .surface import Surface

__all__ = [
    'set_mode',
    'set_caption',
    'clear',
    'flip',
    'update'
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
        sys.stdout.write(convert_array_to_ansi(surface._array))
        sys.stdout.flush()

def update(*rects):
    if not rects:
        flip()
        return

    check_initialized()

    length = len(rects)

    if (length == 1 and
        isinstance(rects[0], Sequence) and
        all(isinstance(r, Sequence) for r in rects[0])):
        rects = rects[0]

    elif length != 1:
        rects = [rects]

    surface = metadata.SURFACE_INSTANCE

    if surface:
        screen = np.zeros((surface.height, surface.width, 4), dtype=np.uint8)

        for rect in map(Rect, rects):
            x, y, w, h = rect
            screen[y:y+h, x:x+w, :3] = surface._array[y:y+h, x:x+w]
            screen[y:y+h, x:x+w, 3] = 1

        sys.stdout.write('\x1b[H')
        sys.stdout.write(convert_array_to_ansi(screen))
        sys.stdout.flush()