import re

from ._utils.common import boundary, ensure_seq
from ._utils.constants import NAMED_COLOR
from ._utils.error import error
from ._utils.seq import Seq

__all__ = ['Color']

_hex = re.compile(r'^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')

class Color(Seq):

    __slots__ = ()

    def _cvrt(self, value):
        return boundary(int(value), 0, 255)

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
                self._seq = ensure_seq(map(self._cvrt, color), 3)

        else:
            self._seq = ensure_seq(map(self._cvrt, args), 3)

    def __neg__(self):
        return type(self)(map(lambda x: 255 - x, self))

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

        return (
            1 - (r / 255),
            1 - (g / 255),
            1 - (b / 255)
        )

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

        Cmax = max(r, g, b)
        Cmin = min(r, g, b)
        delta = Cmax - Cmin

        if delta == 0:
            h = 0
        elif Cmax == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif Cmax == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        elif Cmax == b:
            h = (60 * ((r - g) / delta) + 240) % 360

        if Cmax == 0:
            s = 0
        else:
            s = delta / Cmax

        v = Cmax

        return h, s, v

    @r.setter
    def r(self, value):
        self[0] = value

    @g.setter
    def g(self, value):
        self[1] = value

    @b.setter
    def b(self, value):
        self[2] = value