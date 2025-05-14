from ._utils.sequence import Seq

__all__ = [
    'Vector2',
    'Vector3',
]

class Vector2(Seq, length=2):

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

class Vector3(Seq, length=3):

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