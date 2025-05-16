import sys
import os

import numpy as np

from typing import Sequence

from ._utils import metadata

from ._utils.common import checker
from ._utils.convert import convert_array_to_ansi

from .base import error
from .rect import Rect
from .math import Vector2
from .surface import Surface

__all__ = [
    'init',
    'quit',
    'get_init',
    'set_mode',
    'get_surface',
    'clear',
    'flip',
    'update',
    'Info',
    'set_caption',
    'get_caption',
    'get_window_size',
    'get_window_position',
    'set_window_position'
]

_init_require = checker('INITIALIZE_DISPLAY', 'video system not initialized')

class _VidInfo:
    __slots__ = ('bitsize', 'bytesize', 'masks', 'shifts', 'current_w', 'current_h', 'pixel_format')

def init():
    if not metadata.INITIALIZE_DISPLAY:
        sys.stdout.write('\x1b[?25l\x1b[2J\x1b[H')
        sys.stdout.flush()

        metadata.INITIALIZE_DISPLAY = True

def quit():
    if metadata.INITIALIZE_DISPLAY:
        sys.stdout.write('\x1b[2J\x1b[H\x1b[?25h')
        sys.stdout.flush()

        metadata.INITIALIZE_DISPLAY = False

def get_init():
    return metadata.INITIALIZE_DISPLAY

def set_mode(size, flags=0):
    metadata.WINDOW_SURFACE = Surface(size, flags)
    return metadata.WINDOW_SURFACE

def get_surface():
    return metadata.WINDOW_SURFACE

@_init_require
def clear():
    sys.stdout.write('\x1b[2J\x1b[H')
    sys.stdout.flush()

@_init_require
def flip():
    surface = metadata.WINDOW_SURFACE

    if surface is None:
        raise error("Display mode not set")

    x, y = metadata.POSITION_WINDOW
    x += 1

    for dy, line in enumerate(convert_array_to_ansi(surface._array).splitlines(), start=y + 1):
        sys.stdout.write(f'\x1b[{dy};{x}H{line}')
        sys.stdout.flush()

@_init_require
def update(*rects):
    if not rects:
        flip()
        return

    surface = metadata.WINDOW_SURFACE

    if surface is None:
        raise error("Display mode not set")

    length = len(rects)
    screen = np.zeros((surface.height, surface.width, 4), dtype=np.uint8)
    x, y = metadata.POSITION_WINDOW

    x += 1

    if length == 1 and isinstance(rects[0], Sequence) and all(isinstance(r, Sequence) for r in rects[0]):
        rects = rects[0]
    elif length != 1:
        rects = [rects]

    for rect in map(Rect, rects):
        x, y, w, h = rect
        screen[y:y+h, x:x+w, :3] = surface._array[y:y+h, x:x+w]
        screen[y:y+h, x:x+w, 3] = 1

    for dy, line in enumerate(convert_array_to_ansi(screen).splitlines(), start=y + 1):
        sys.stdout.write(f'\x1b[{dy};{x}H{line}')
        sys.stdout.flush()

@_init_require
def Info():
    info = _VidInfo()

    current_size = os.get_terminal_size()

    info.bitsize = 24
    info.bytesize = 8
    info.masks = (0xFF0000, 0x00FF00, 0x0000FF)
    info.shifts = (16, 8, 0)
    info.current_w = current_size.columns
    info.current_h = current_size.lines * 2
    info.pixel_format = 'RGB' # also RGB

    return info

def set_caption(caption, icontitle=None):
    if not isinstance(caption, str):
        raise TypeError(f"argument 1 must be str, not {type(caption).__name__}")
    if icontitle is not None and not isinstance(icontitle, str):
        raise TypeError(f"argument 2 must be str, not {type(icontitle).__name__}")

    sys.stdout.write(f'\x1b]0;{caption}\x07')
    sys.stdout.flush()

    metadata.CAPTION = caption
    metadata.ICON_TITLE = icontitle or ''

def get_caption():
    return (metadata.CAPTION, metadata.CAPTION) if metadata.CAPTION else ()

def get_window_size():
    surface = metadata.WINDOW_SURFACE

    if surface is None:
        raise error("No open window")

    return surface.size

def get_window_position():
    return metadata.POSITION_WINDOW

def set_window_position(*point):
    metadata.POSITION_WINDOW = tuple(Vector2(*point))