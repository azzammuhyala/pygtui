import re

from .utils.common import boundary
from .utils.constants import NAMED_COLOR
from .utils.seq import SeqInt

def _bound(n):
    return boundary(int(n), 0, 255)

_hex = re.compile(r'^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')

class Color(SeqInt):

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
                        self._seq = [int(color[0]*2, 16), int(color[1]*2, 16), int(color[2]*2, 16)]
                    else:
                        self._seq = [int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)]

            else:
                self._seq = [_bound(color[0]), _bound(color[1]), _bound(color[2])]

        elif length == 3:
            self._seq = [_bound(args[0]), _bound(args[1]), _bound(args[2])]

        else:
            raise ValueError('Color must be a string or a tuple of three integers')

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
    def rgb(self):
        return (self.r, self.g, self.b)

    @r.setter
    def r(self, value):
        self[0] = _bound(value)

    @g.setter
    def g(self, value):
        self[1] = _bound(value)

    @b.setter
    def b(self, value):
        self[2] = _bound(value)

    @rgb.setter
    def rgb(self, value):
        self[0:3] = map(_bound, value)