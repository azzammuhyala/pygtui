import re

from ._utils.common import boundary
from ._utils.constants import NAMED_COLOR
from ._utils.error import error
from ._utils.seq import Seq

from .math import Vector

__all__ = ['Color']

_hex = re.compile(r'^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')

class _FloatVector3(Vector, length=3):

    __slots__ = ()

    def _cvrt(self, value):
        return float(value)

class _FloatVector4(Vector, length=4):

    __slots__ = ()

    def _cvrt(self, value):
        return float(value)

class Color(Seq):

    __slots__ = ()

    @classmethod
    def _cvrt(cls, value):
        value = int(value)
        return boundary(255 + value if value < 0 else value, 0, 255)

    def __init__(self, *args):
        length = len(args)

        if length == 0:
            self._seq = [0, 0, 0]

        elif length == 1:
            color = args[0]

            if isinstance(color, str):
                color = color.strip().lower()
                if color in NAMED_COLOR:
                    color = NAMED_COLOR[color]

                matched = _hex.match(color)
                if matched:
                    color = matched.group(1)
                    if len(color) == 3:
                        self._seq = [
                            int(color[0]*2, 16),
                            int(color[1]*2, 16),
                            int(color[2]*2, 16)
                        ]
                    else:
                        self._seq = [
                            int(color[0:2], 16),
                            int(color[2:4], 16),
                            int(color[4:6], 16)
                        ]

                else:
                    raise error("invalid color name")

            elif isinstance(color, int):
                if 0x000000 <= color <= 0xFFFFFF:
                    self._seq = [
                        (color >> 16) & 0xFF,
                        (color >> 8) & 0xFF,
                        color & 0xFF
                    ]

                else:
                    raise error("invalid color argument (integer out of acceptable range)")

            else:
                self._seq = list(map(self._cvrt, color))

        else:
            self._seq = list(map(self._cvrt, args))

        if len(self._seq) != 3:
            raise error("invalid color (color sequence must have size 3 or 4, and each element must be an integer in the range [0, 255])")

    @property
    def r(self):
        return self[0]

    @property
    def g(self):
        return self[1]

    @property
    def b(self):
        return self[2]

    @property
    def cmy(self):
        r, g, b = self

        return (1 - (r / 255), 1 - (g / 255), 1 - (b / 255))

    @property
    def cmyk(self):
        r, g, b = self

        r /= 255
        g /= 255
        b /= 255

        k = 1 - max(r, g, b)

        if k == 1:
            c = m = y = 0
        else:
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)

        return (c, m, y, k)

    @property
    def hsv(self):
        r, g, b = self

        r /= 255
        g /= 255
        b /= 255

        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        if delta == 0:
            h = 0
        elif cmax == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif cmax == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        elif cmax == b:
            h = (60 * ((r - g) / delta) + 240) % 360

        return (h, 0 if cmax == 0 else delta / cmax, cmax)

    @property
    def hsl(self):
        r, g, b = self

        r /= 255
        g /= 255
        b /= 255

        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        if delta == 0:
            h = 0
        elif cmax == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif cmax == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        elif cmax == b:
            h = (60 * ((r - g) / delta) + 240) % 360

        l = (cmax + cmin) / 2

        if delta == 0:
            s = 0
        else:
            s = delta / (1 - abs(2 * l - 1)) if l != 0 and l != 1 else delta / (cmax + cmin)

        return (h, s, l)

    @property
    def i1i2i3(self):
        r, g, b = self

        return ((r + g + b) / 3, (r - b) / 2, (2 * g - r - b) / 4)

    @property
    def normalized(self):
        r, g, b = self

    @r.setter
    def r(self, value):
        self[0] = value

    @g.setter
    def g(self, value):
        self[1] = value

    @b.setter
    def b(self, value):
        self[2] = value

    @classmethod
    def from_cmy(cls, *object):
        c, m, y = _FloatVector3(*object)

    @classmethod
    def from_cmyk(cls, *object):
        c, m, y, k = _FloatVector4(*object)

    @classmethod
    def from_hsv(cls, *object):
        h, s, v = _FloatVector3(*object)

    @classmethod
    def from_hsl(cls, *object):
        h, s, l = _FloatVector3(*object)

    @classmethod
    def from_i1i2i3(cls, *object):
        i1, i2, i3 = _FloatVector3(*object)

    def grayscale(self):
        r, g, b = self
        return int(round(0.2989 * r + 0.5870 * g + 0.1140 * b))