import sys
import os

import numpy as np

from typing import Sequence

from ._utils import metadata

from ._utils.common import Singleton
from ._utils.convert import convert_array_to_ansi

from .rect import Rect
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
]

class _VidInfo(Singleton):

    @property
    def current_w(self):
        return os.get_terminal_size().columns

    @property
    def current_h(self):
        return os.get_terminal_size().lines * 2

    @property
    def current_size(self):
        return (self.current_w, self.current_h)

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

def clear():
    sys.stdout.write('\x1b[2J\x1b[H')
    sys.stdout.flush()

def flip():
    surface = metadata.WINDOW_SURFACE

    if surface:
        sys.stdout.write('\x1b[H' + convert_array_to_ansi(surface._array))
        sys.stdout.flush()

def update(*rects):
    if not rects:
        flip()
        return

    length = len(rects)

    if length == 1 and isinstance(rects[0], Sequence) and all(isinstance(r, Sequence) for r in rects[0]):
        rects = rects[0]
    elif length != 1:
        rects = [rects]

    surface = metadata.WINDOW_SURFACE

    if surface:
        screen = np.zeros((surface.height, surface.width, 4), dtype=np.uint8)

        for rect in map(Rect, rects):
            x, y, w, h = rect
            screen[y:y+h, x:x+w, :3] = surface._array[y:y+h, x:x+w]
            screen[y:y+h, x:x+w, 3] = 1

        sys.stdout.write('\x1b[H' + convert_array_to_ansi(screen))
        sys.stdout.flush()

def Info():
    return _VidInfo()

def set_icon(surface):
    pass

def set_caption(caption, icontitle=None):
    sys.stdout.write(f'\x1b]0;{caption}\x07')
    sys.stdout.flush()

    metadata.CAPTION = caption
    metadata.ICON_TITLE = icontitle

def get_caption():
    return (metadata.CAPTION, metadata.ICON_TITLE or '')