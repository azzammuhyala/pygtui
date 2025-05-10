from ._utils.seq import Seq
from ._utils.common import boundary

from .math import Vector2

__all__ = ['Rect']

class Rect(Seq, length=4):

    __slots__ = ()

    def __init__(self, *args):
        length = len(args)

        if length == 1:
            arg = args[0]

            if len(arg) == 2:
                args = (*arg[0], *arg[1])
            elif not isinstance(arg, str):
                args = arg

        elif length == 2:
            args = (*args[0], *args[1])

        super().__init__(*args)

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
    def x(self):
        return self.left

    @property
    def y(self):
        return self.top

    @property
    def w(self):
        return self.width

    @property
    def h(self):
        return self.height

    @property
    def centerx(self):
        return self.left + self.width // 2

    @property
    def centery(self):
        return self.top + self.height // 2

    @property
    def topleft(self):
        return (self.left, self.top)

    @property
    def topright(self):
        return (self.right, self.top)

    @property
    def bottomright(self):
        return (self.right, self.bottom)

    @property
    def bottomleft(self):
        return (self.left, self.bottom)

    @property
    def midleft(self):
        return (self.left, self.centery)

    @property
    def midtop(self):
        return (self.centerx, self.top)

    @property
    def midright(self):
        return (self.right, self.centery)

    @property
    def midbottom(self):
        return (self.centerx, self.bottom)

    @property
    def center(self):
        return (self.centerx, self.centery)

    @property
    def size(self):
        return (self.width, self.height)

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

    @x.setter
    def x(self, value):
        self.left = value

    @y.setter
    def y(self, value):
        self.top = value

    @w.setter
    def w(self, value):
        self.width = value
    
    @h.setter
    def h(self, value):
        self.height = value

    @centerx.setter
    def centerx(self, value):
        self.left = value - self.width / 2

    @centery.setter
    def centery(self, value):
        self.top = value - self.height / 2

    @topleft.setter
    def topleft(self, value):
        self.left, self.top = value

    @topright.setter
    def topright(self, value):
        self.right, self.top = value

    @bottomright.setter
    def bottomright(self, value):
        self.right, self.bottom = value

    @bottomleft.setter
    def bottomleft(self, value):
        self.left, self.bottom = value

    @midleft.setter
    def midleft(self, value):
        self.left, self.centery = value

    @midtop.setter
    def midtop(self, value):
        self.centerx, self.top = value

    @midright.setter
    def midright(self, value):
        self.right, self.centery = value

    @midbottom.setter
    def midbottom(self, value):
        self.centerx, self.bottom = value

    @center.setter
    def center(self, value):
        self.centerx, self.centery = value

    @size.setter
    def size(self, value):
        self.width, self.height = value

    def move(self, *point):
        x1, y1, w1, h1 = self
        x, y = Vector2(*point)

        return type(self)(x1 + x, y1 + y, w1, h1)

    def inflate(self, *point):
        x1, y1, w1, h1 = self
        x, y = Vector2(*point)

        return type(self)(x1 - x / 2, y1 - y / 2, w1 + x, h1 + y)

    def clamp(self, *rect):
        x1, y1, w1, h1 = self
        x2, y2, w2, h2 = type(self)(*rect)

        return type(self)(
            boundary(x1, x2, x2 + w2 - w1),
            boundary(y1, y2, y2 + h2 - h1),
            w1,
            h1
        )

    def clip(self, *rect):
        x1, y1, w1, h1 = self
        x2, y2, w2, h2 = type(self)(*rect)

        x = max(x1, x2)
        y = max(y1, y2)
        xw = min(x1 + w1, x2 + w2)
        yh = min(y1 + h1, y2 + h2)

        if xw <= x or yh <= y:
            return type(self)(0, 0, 0, 0)

        return type(self)(x, y, xw - x, yh - y)

    def union(self, *rect):
        x1, y1, w1, h1 = self
        x2, y2, w2, h2 = type(self)(*rect)

        x = min(x1, x2)
        y = min(y1, y2)

        return type(self)(
            x,
            y,
            max(x1 + w1, x2 + w2) - x,
            max(y1 + h1, y2 + h2) - y
        )

    def fit(self, *rect):
        x1, y1, w1, h1 = self
        x2, y2, w2, h2 = type(self)(*rect)

        inner_ratio = w1 / h1
        outer_ratio = w2 / h2

        if inner_ratio > outer_ratio:
            w = w2
            h = w2 / inner_ratio
        else:
            w = h2 * inner_ratio
            h = h2

        return type(self)(x2 + (w2 - w) / 2, y2 + (h2 - h) / 2, w, h)

    def normalize(self):
        x, y, w, h = self

        if w < 0:
            x += w
            w = -w
        if h < 0:
            y += h
            h = -h

        return type(self)(x, y, w, h)

    def contains(self, *rect):
        x1, y1, w1, h1 = self
        x2, y2, w2, h2 = type(self)(*rect)

        return (
            x1 <= x2 and
            y1 <= y2 and
            x1 + w1 >= x2 + w2 and
            y1 + h1 >= y2 + h2
        )

    def collidepoint(self, *point):
        x1, y1, w1, h1 = self
        x, y = Vector2(*point)

        return x1 <= x <= x1 + w1 and y1 <= y <= y1 + h1

    def colliderect(self, *rect):
        x1, y1, w1, h1 = self
        x2, y2, w2, h2 = type(self)(*rect)

        return (
            x1 <= x2 + w2 and
            x1 + w1 >= x2 and
            y1 <= y2 + h2 and
            y1 + h1 >= y2
        )