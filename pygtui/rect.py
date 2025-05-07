from .utils.seq import SeqInt

class Rect(SeqInt):

    def __init__(self, *args):
        length = len(args)

        if length == 0:
            self._seq = [0, 0, 0, 0]
        elif length == 1:
            self._seq = [int(args[0][0]), int(args[0][1]), int(args[0][2]), int(args[0][3])]
        elif length == 2:
            self._seq = [int(args[0][0]), int(args[0][1]), int(args[1][0]), int(args[1][1])]
        elif length == 4:
            self._seq = [int(args[0]), int(args[1]), int(args[2]), int(args[3])]

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
        self[0:1] = value

    @size.setter
    def size(self, value):
        self[2:3] = value

    @centerx.setter
    def centerx(self, value):
        self.left = value - self.width / 2

    @centery.setter
    def centery(self, value):
        self.top = value - self.height / 2

    @center.setter
    def center(self, value):
        self.centerx, self.centery = value