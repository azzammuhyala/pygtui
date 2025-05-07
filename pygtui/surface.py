import numpy as np

from .rect import Rect
from .math import Vector2
from .color import Color

class Surface:

    def __init__(self, size, flags=0):
        w, h = Vector2(size)
        self._flags = flags
        self.array = np.zeros((h, w, 3), dtype=np.uint8)

    @property
    def width(self):
        return self.array.shape[1]

    @property
    def height(self):
        return self.array.shape[0]

    @property
    def size(self):
        return (self.width, self.height)

    def copy(self):
        return type(self)(self.size)

    def blit(self, surface, dest, area=None):
        x, y = Vector2(dest)
    
        if area is not None:
            surface = surface.crop(area)

        w = min(surface.width, self.width - x)
        h = min(surface.height, self.height - y)

        if w <= 0 or h <= 0:
            return

        self.array[y:y+h, x:x+w] = surface.array[0:h, 0:w]

    def crop(self, rect):
        rect = Rect(rect)
        surface = Surface(rect.size)

        surface.array[:] = self.array[rect.top:rect.bottom, rect.left:rect.right]

        return surface

    def fill(self, color):
        self.array[:, :, :] = Color(color)