import re

from .utils.seq import SeqInt

_vector2 = re.compile(r'(-?\d+)\s*(x|,|\ |-)\s*(-?\d+)')
_vector3 = re.compile(r'(-?\d+)\s*(x|,|\ |-)\s*(-?\d+)\s*(x|,|\ |-)\s*(-?\d+)')

class Vector2(SeqInt):

    def __init__(self, *args):
        length = len(args)

        if length == 0:
            self._seq = [0, 0]
        elif length == 1:
            vector = args[0]
            if isinstance(vector, str):
                matched = _vector2.match(vector)
                if matched:
                    self._seq = [int(matched.group(1)), int(matched.group(3))]
            else:
                self._seq = [int(vector[0]), int(vector[1])]
        elif length == 2:
            self._seq = [int(args[0]), int(args[1])]

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def point(self):
        return (self.x, self.y)

    @x.setter
    def x(self, value):
        self[0] = int(value)

    @y.setter
    def y(self, value):
        self[1] = int(value)

    @point.setter
    def point(self, value):
        self[0:2] = value

class Vector3(SeqInt):

    def __init__(self, *args):
        length = len(args)

        if length == 0:
            self._seq = [0, 0, 0]
        elif length == 1:
            vector = args[0]
            if isinstance(vector, str):
                matched = _vector3.match(vector)
                if matched:
                    self._seq = [int(matched.group(1)), int(matched.group(3)), int(matched.group(5))]
            else:
                self._seq = [int(vector[0]), int(vector[1]), int(vector[2])]
        elif length == 3:
            self._seq = [int(args[0]), int(args[1]), int(args[2])]

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @property
    def point(self):
        return (self.x, self.y, self.z)

    @x.setter
    def x(self, value):
        self[0] = int(value)

    @y.setter
    def y(self, value):
        self[1] = int(value)

    @z.setter
    def z(self, value):
        self[2] = int(value)

    @point.setter
    def point(self, value):
        self[0:3] = value