import re

from ._utils.common import ensure_seq
from ._utils.seq import Seq

_vector2 = re.compile(r'(-?\d+)\s*(x|,|\ |-)\s*(-?\d+)')
_vector3 = re.compile(r'(-?\d+)\s*(x|,|\ |-)\s*(-?\d+)\s*(x|,|\ |-)\s*(-?\d+)')

class Vector2(Seq):

    def _cvrt(self, value):
        return int(value)

    def __init__(self, *args):
        length = len(args)

        if length == 0:
            self._seq = [0, 0]

        elif length == 1:
            vector = args[0]

            if isinstance(vector, str):
                matched = _vector2.match(vector)
                if matched:
                    self._seq = [
                        int(matched.group(1)),
                        int(matched.group(3))
                    ]

            else:
                self._seq = ensure_seq(map(int, vector), 2)

        else:
            self._seq = ensure_seq(map(int, args), 2)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @x.setter
    def x(self, value):
        self[0] = value

    @y.setter
    def y(self, value):
        self[1] = value

class Vector3(Seq):

    def _cvrt(self, value):
        return int(value)

    def __init__(self, *args):
        length = len(args)

        if length == 0:
            self._seq = [0, 0, 0]

        elif length == 1:
            vector = args[0]

            if isinstance(vector, str):
                matched = _vector3.match(vector)
                if matched:
                    self._seq = [
                        int(matched.group(1)),
                        int(matched.group(3)),
                        int(matched.group(5))
                    ]

            else:
                self._seq = ensure_seq(map(int, vector), 3)

        else:
            self._seq = ensure_seq(map(int, args), 3)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @x.setter
    def x(self, value):
        self[0] = value

    @y.setter
    def y(self, value):
        self[1] = value

    @z.setter
    def z(self, value):
        self[2] = value