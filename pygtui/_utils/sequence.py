import re

from operator import add, sub, mul, truediv, floordiv, pow, mod, neg

def op(self, other, func):
    return type(self)(
        func(a, b)
        for a, b in zip(
            type(self)(self),
            type(self)(other)
        )
    )

class Seq:

    """
    Base class of sequence elements.

    The length of this class sequence is constant that mean cannot add or delete elements.
    """

    __slots__ = ('_seq',)

    @classmethod
    def _convert(cls, value):
        try:
            return cls._type(value)
        except BaseException as e:
            raise cls._error from e

    def __init_subclass__(cls, length,
                               type=int,
                               rsep=r'\s*(x|X|,|\ )\s*',
                               rvalue=r'(-?\d+)',
                               default=0,
                               **kwargs):

        super().__init_subclass__(**kwargs)

        cls._length = length
        cls._type = staticmethod(type)
        cls._default = default
        cls._error = TypeError(f"argument must be {cls.__name__} style object")
        cls._regex = re.compile(rsep.join(rvalue for _ in range(length)))

    def __init__(self, *args):
        if type(self) is Seq:
            raise TypeError("Seq is an abstract class and cannot be instantiated directly")

        length = len(args)

        if length == 0:
            seq = [self._default] * self._length

        elif length == 1:
            arg = args[0]

            if isinstance(arg, str):
                matched = self._regex.match(arg)
                if not matched:
                    raise self._error
                seq = [self._convert(matched.group(i)) for i in range(1, self._length * 2 + 1, 2)]

            else:
                seq = list(map(self._convert, arg))

        else:
            seq = list(map(self._convert, args))

        if len(seq) != self._length:
            raise self._error

        self._seq = seq

    def __getitem__(self, index):
        return self._seq[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            self._seq[index] = map(self._convert, value)
            if len(self._seq) != self._length:
                raise self._error
        else:
            self._seq[index] = self._convert(value)

    def __iter__(self):
        return iter(self._seq)

    def __len__(self):
        return self._length

    def __add__(self, other):
        return op(self, other, add)

    def __sub__(self, other):
        return op(self, other, sub)

    def __mul__(self, other):
        return op(self, other, mul)

    def __truediv__(self, other):
        return op(self, other, truediv)

    def __floordiv__(self, other):
        return op(self, other, floordiv)

    def __pow__(self, other):
        return op(self, other, pow)

    def __mod__(self, other):
        return op(self, other, mod)

    def __radd__(self, other):
        return op(other, self, add)

    def __rsub__(self, other):
        return op(other, self, sub)

    def __rmul__(self, other):
        return op(other, self, mul)

    def __rtruediv__(self, other):
        return op(other, self, truediv)

    def __rfloordiv__(self, other):
        return op(other, self, floordiv)

    def __rpow__(self, other):
        return op(other, self, pow)

    def __rmod__(self, other):
        return op(other, self, mod)

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __imul__(self, other):
        return self * other

    def __itruediv__(self, other):
        return self / other

    def __ifloordiv__(self, other):
        return self // other

    def __ipow__(self, other):
        return self ** other

    def __imod__(self, other):
        return self % other

    def __neg__(self):
        return type(self)(map(neg, self))

    def __eq__(self, other):
        return self._seq == type(self)(other)._seq

    def __ne__(self, other):
        return self._seq != type(self)(other)._seq

    def __contains__(self, other):
        return other in self._seq

    def __reversed__(self):
        return reversed(self._seq)

    def __repr__(self):
        return type(self).__name__ + '(' + ', '.join(map(str, self._seq)) + ')'

    def copy(self):
        return type(self)(self)

    def update(self, *args):
        self.__init__(*args)