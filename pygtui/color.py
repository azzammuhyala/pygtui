import re

from ._utils.common import boundary
from ._utils.constants import NAMED_COLOR
from ._utils.sequence import Seq

__all__ = [
    'Color'
]

_hex = re.compile(r'^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')
_rvalue_float = r'(-?(?:\d+\.\d+|\.\d+|\d+))'

class _FloatVector3(Seq, length=3,
                         type=float,
                         rvalue=_rvalue_float,
                         default=0.0):
    __slots__ = ()

class _FloatVector4(Seq, length=4,
                         type=float,
                         rvalue=_rvalue_float,
                         default=0.0):
    __slots__ = ()

def _type_color(value):
    value = int(value)
    return boundary(255 + value if value < 0 else value, 0, 255)

class Color(Seq, length=3, type=_type_color):

    __slots__ = ()

    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]

            if isinstance(arg, str):
                arg = arg.strip().lower()

                if arg in NAMED_COLOR:
                    arg = NAMED_COLOR[arg]

                matched = _hex.match(arg)

                if matched:
                    arg = matched.group(1)
                    if len(arg) == 3:
                        args = (
                            int(arg[0]*2, 16),
                            int(arg[1]*2, 16),
                            int(arg[2]*2, 16)
                        )
                    else:
                        args = (
                            int(arg[0:2], 16),
                            int(arg[2:4], 16),
                            int(arg[4:6], 16)
                        )

            elif isinstance(arg, int) and 0x000000 <= arg <= 0xFFFFFF:
                args = (
                    (arg >> 16) & 0xFF,
                    (arg >> 8) & 0xFF,
                    arg & 0xFF
                )

        super().__init__(*args)

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
        r, g, b = self.normalized

        return (1 - r, 1 - g, 1 - b)

    @property
    def cmyk(self):
        r, g, b = self.normalized

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
        r, g, b = self.normalized

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
        r, g, b = self.normalized

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

        return (r / 255, g / 255, b / 255)

    @r.setter
    def r(self, value):
        self[0] = value

    @g.setter
    def g(self, value):
        self[1] = value

    @b.setter
    def b(self, value):
        self[2] = value

    @cmy.setter
    def cmy(self, value):
        c, m, y = _FloatVector3(value)

        self.r = (1 - c) * 255
        self.g = (1 - m) * 255
        self.b = (1 - y) * 255

    @cmyk.setter
    def cmyk(self, value):
        c, m, y, k = _FloatVector4(value)

        self.r = (1 - c) * (1 - k) * 255
        self.g = (1 - m) * (1 - k) * 255
        self.b = (1 - y) * (1 - k) * 255

    @hsv.setter
    def hsv(self, value):
        h, s, v = _FloatVector3(value)

        h = h / 60
        c = v * s
        x = c * (1 - abs((h % 2) - 1))
        m = v - c

        if 0 <= h < 1:
            r, g, b = c, x, 0
        elif 1 <= h < 2:
            r, g, b = x, c, 0
        elif 2 <= h < 3:
            r, g, b = 0, c, x
        elif 3 <= h < 4:
            r, g, b = 0, x, c
        elif 4 <= h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        self.r = (r + m) * 255
        self.g = (g + m) * 255
        self.b = (b + m) * 255

    @hsl.setter
    def hsl(self, value):
        h, s, l = _FloatVector3(value)

        h = h / 60
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h % 2) - 1))
        m = l - c / 2

        if 0 <= h < 1:
            r, g, b = c, x, 0
        elif 1 <= h < 2:
            r, g, b = x, c, 0
        elif 2 <= h < 3:
            r, g, b = 0, c, x
        elif 3 <= h < 4:
            r, g, b = 0, x, c
        elif 4 <= h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        self.r = (r + m) * 255
        self.g = (g + m) * 255
        self.b = (b + m) * 255

    @i1i2i3.setter
    def i1i2i3(self, value):
        i1, i2, i3 = _FloatVector3(value)

        self.r = boundary(255, 0, round(i1 + (2/3) * i2 - (1/3) * i3))
        self.g = boundary(255, 0, round(i1 - (1/3) * i2 + (2/3) * i3))
        self.b = boundary(255, 0, round(i1 - (2/3) * i2 - (1/3) * i3))

    @normalized.setter
    def normalized(self, value):
        r, g, b = _FloatVector3(value)

        self.r = r * 255
        self.g = g * 255
        self.b = b * 255

    @classmethod
    def from_cmy(cls, *object):
        color = cls()
        color.cmy = _FloatVector3(*object)
        return color

    @classmethod
    def from_cmyk(cls, *object):
        color = cls()
        color.cmyk = _FloatVector4(*object)
        return color

    @classmethod
    def from_hsv(cls, *object):
        color = cls()
        color.hsv = _FloatVector3(*object)
        return color

    @classmethod
    def from_hsl(cls, *object):
        color = cls()
        color.hsl = _FloatVector3(*object)
        return color

    @classmethod
    def from_i1i2i3(cls, *object):
        color = cls()
        color.i1i2i3 = _FloatVector3(*object)
        return color

    @classmethod
    def from_normalize(cls, *object):
        color = cls()
        color.normalized = _FloatVector3(*object)
        return color

    def normalize(self):
        return self.normalized

    def grayscale(self):
        r, g, b = self
        gray = round(0.2989 * r + 0.5870 * g + 0.1140 * b)
        return Color(gray, gray, gray)