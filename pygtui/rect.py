from ._utils.seq import Seq
from ._utils.common import ensure_seq

from .math import Vector2

class Rect(Seq):

    def _cvrt(self, value):
        return int(value)

    def __init__(self, *args):
        length = len(args)

        if length == 0:
            self._seq = [0, 0, 0, 0]

        elif length == 1:
            self._seq = ensure_seq(map(int, args[0]), 4)

        elif length == 2:
            topleft, size = ensure_seq(args, 2)
            left, top = ensure_seq(map(int, topleft), 2)
            width, height = ensure_seq(map(int, size), 2)

            self._seq = [left, top, width, height]

        else:
            self._seq = ensure_seq(map(int, args), 4)

    @property
    def left(self):
        return self[0]

    @property
    def top(self):
        return self[1]

    @property
    def width(self):
        return self[2]

    @property
    def height(self):
        return self[3]

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def topleft(self):
        return (self.left, self.top)

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def centerx(self):
        return self.left + self.width / 2

    @property
    def centery(self):
        return self.top + self.height / 2

    @property
    def center(self):
        return (self.centerx, self.centery)

    @left.setter
    def left(self, value):
        self[0] = value

    @top.setter
    def top(self, value):
        self[1] = value

    @width.setter
    def width(self, value):
        self[2] = value

    @height.setter
    def height(self, value):
        self[3] = value

    @right.setter
    def right(self, value):
        self.left = value - self.width

    @bottom.setter
    def bottom(self, value):
        self.top = value - self.height

    @topleft.setter
    def topleft(self, value):
        self[0:2] = value

    @size.setter
    def size(self, value):
        self[2:4] = value

    @centerx.setter
    def centerx(self, value):
        self.left = value - self.width / 2

    @centery.setter
    def centery(self, value):
        self.top = value - self.height / 2

    @center.setter
    def center(self, value):
        self.centerx, self.centery = value

    def contains(self, *rect):
        rect = Rect(*rect)
        return (
            self.left <= rect.left and
            self.top <= rect.top and
            self.right >= rect.right and
            self.bottom >= rect.bottom
        )

    def colliderect(self, *rect):
        rect = Rect(*rect)
        return (
            self.left <= rect.right and
            self.right >= rect.left and
            self.top <= rect.bottom and
            self.bottom >= rect.top
        )

    def collidepoint(self, *point):
        point = Vector2(*point)
        return self.left <= point.x <= self.right and self.top <= point.y <= self.bottom