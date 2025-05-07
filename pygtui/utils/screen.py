import sys

from . import metadata

from .convert import convert_array_to_ansi
from .error import check_initialized

from ..surface import Surface

def clear():
    check_initialized()

    if metadata.DISPLAY_INSTANCE:
        sys.stdout.write('\x1b[2J\x1b[H')
        sys.stdout.flush()

def flip():
    check_initialized()

    self = metadata.DISPLAY_INSTANCE
    if self:
        sys.stdout.write('\x1b[H')
        sys.stdout.write(convert_array_to_ansi(self.array))
        sys.stdout.flush()

class _DisplaySurface(Surface):

    def __new__(cls, *args, **kwargs):
        metadata.DISPLAY_INSTANCE = super(_DisplaySurface, cls).__new__(cls)
        return metadata.DISPLAY_INSTANCE

    def __init__(self, size, flags=0):
        check_initialized()

        super().__init__(size, flags)
        sys.stdout.write('\x1b[?25l')
        clear()