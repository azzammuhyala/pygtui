import re

from ._utils.error import error
from ._utils.seq import Seq

__all__ = [
    'Vector',
    'Vector2',
    'Vector3',
]

class Vector(Seq):

    __slots__ = ()

    def _cvrt(self, value):
        return int(value)

    def __init_subclass__(cls, length):
        super().__init_subclass__()
        cls._length = length
        cls._regex = re.compile(r'\s*(x|,|-|\ )\s*'.join(r'(-?\d+)' for _ in range(length)))

    def __init__(self, *args):
        length = len(args)

        if length == 0:
            self._seq = [0] * self._length

        elif length == 1:
            arg = args[0]

            if isinstance(arg, str):
                matched = self._regex.match(arg)
                if matched:
                    self._seq = [self._cvrt(matched.group(i)) for i in range(1, self._length * 2 + 1, 2)]
                else:
                    raise error

            else:
                self._seq = list(map(self._cvrt, arg))

        else:
            self._seq = list(map(self._cvrt, args))

        if len(self._seq) != self._length:
            raise error

class Vector2(Vector, length=2):

    __slots__ = ()

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

class Vector3(Vector, length=3):

    __slots__ = ()

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