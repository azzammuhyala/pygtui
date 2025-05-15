import numpy as np

from .bufferproxy import BufferProxy
from .rect import Rect
from .math import Vector2
from .color import Color

__all__ = [
    'Surface'
]

class Surface:

    __slots__ = ('_array', '_flags', '_buffer')

    def __init__(self, size, flags=0):
        w, h = Vector2(size)

        if w < 0 or h < 0:
            raise ValueError("invalid resolution for Surface")

        self._array = np.zeros((h, w, 3), dtype=np.uint8)
        self._flags = flags
        self._buffer = BufferProxy(self)

    def __repr__(self):
        return f'<Surface({self.width}x{self.height}x24)>'

    @property
    def width(self):
        return self._array.shape[1]

    @property
    def height(self):
        return self._array.shape[0]

    @property
    def size(self):
        return (self.width, self.height)

    def copy(self):
        surface = type(self)(self.size, self._flags)
        surface._array = self._array.copy()
        return surface

    def blit(self, source, dest, area=None):
        if not isinstance(source, Surface):
            raise TypeError("blit source must be a Surface")

        if area is not None:
            source = source.subsurface(*area)

        x, y = Vector2(dest)

        w = min(source.width, self.width - x)
        h = min(source.height, self.height - y)

        if w <= 0 or h <= 0:
            return

        self._array[y:y+h, x:x+w] = source._array[0:h, 0:w]

    def fill(self, *color):
        self._array[:, :, :] = Color(*color)

    def subsurface(self, *rect):
        x, y, w, h = Rect(*rect)

        if not self.get_rect().colliderect(x, y, w, h):
            raise ValueError("subsurface rectangle outside surface area")

        surface = Surface(self.size, self._flags)
        surface._array = self._array[y:y+h, x:x+w]

        return surface

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_size(self):
        return self.size

    def get_flags(self):
        return self._flags

    def get_buffer(self):
        return self._buffer

    def get_rect(self, **kwargs):
        return Rect(0, 0, self.width, self.height).move_to(**kwargs)

    def get_at(self, *point):
        x, y = Vector2(*point)
        return tuple(map(int, self._array[y, x]))

    def set_at(self, point, color):
        x, y = Vector2(point)
        self._array[y, x] = Color(color)