import numpy as np

from ._utils.error import error

from .rect import Rect
from .math import Vector2
from .color import Color

from .constants import CONSTANT

class Surface:

    __slots__ = ('_array', '_flags')

    def __init__(self, size, flags=0):
        w, h = Vector2(size)

        if w < 0 or h < 0:
            raise error("invalid resolution for Surface")

        self._array = np.zeros((h, w, 3), dtype=np.uint8)
        self._flags = flags

    def __repr__(self):
        return f'<Surface({self.width}x{self.height}x32)>'

    @property
    def width(self):
        return self.array.shape[1]

    @property
    def height(self):
        return self.array.shape[0]

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, array):
        if not isinstance(array, np.ndarray) or array.dtype != np.uint8:
            raise error("Surface array must be a numpy array with type uint8")
        if len(array.shape) != 3 or array.shape[0] < 0 or array.shape[1] < 0 or array.shape[2] != 3:
            raise error("invalid resolution for Surface")

        oh, ow, _ = self._array.shape
        nh, nw, _ = array.shape

        if self._flags == CONSTANT and (ow != nw or oh != nh):
            raise error("Surface array resolution must match the Surface resolution")

        self._array = array

    def copy(self):
        surface = type(self)(self.size, self._flags)
        surface.array = self.array.copy()
        return surface

    def blit(self, source, dest, area=None):
        if not isinstance(source, Surface):
            raise error("blit source must be a Surface")

        x, y = Vector2(dest)

        if area is None:
            sw, sh = source.size
            array = source.array
        else:
            xc, yc, sw, sh = Rect(area)
            array = source.array[yc:yc+sh, xc:xc+sw]

        w = min(sw, self.width - x)
        h = min(sh, self.height - y)

        if w <= 0 or h <= 0:
            return

        self.array[y:y+h, x:x+w] = array[0:h, 0:w]

    def fill(self, *color):
        self.array[:, :, :] = Color(*color)

    def subsurface(self, *rect):
        x, y, w, h = Rect(*rect)

        if not self.get_rect().colliderect(x, y, w, h):
            raise error("subsurface rectangle outside surface area")

        surface = Surface(self.size, self._flags)
        surface.array = self.array[y:y+h, x:x+w]

        return surface

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_size(self):
        return self.size

    def get_flags(self):
        return self._flags

    def get_rect(self, **kwargs):
        rect = Rect(0, 0, self.width, self.height)
        for key, value in kwargs.items():
            setattr(rect, key, value)
        return rect

    def get_at(self, *point):
        x, y = Vector2(*point)
        return tuple(map(int, self.array[y, x]))

    def set_at(self, point, color):
        x, y = Vector2(*point)
        self.array[y, x] = Color(*color)