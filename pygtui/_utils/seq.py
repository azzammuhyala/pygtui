from abc import ABC, abstractmethod
from operator import add, sub, mul, truediv, floordiv, pow, mod, neg

from .common import name

def op(self, other, func):
    return type(self)(
        func(a, b)
        for a, b in zip(
            type(self)(self),
            type(self)(other)
        )
    )

class Seq(ABC):

    __slots__ = ('_seq',)

    @abstractmethod
    def _cvrt(self, value):
        pass

    @abstractmethod
    def __init__(self, *args):
        pass

    def __getitem__(self, index):
        return self._seq[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            self._seq[index] = map(self._cvrt, value)
        else:
            self._seq[index] = self._cvrt(value)

    def __iter__(self):
        return iter(self._seq)

    def __len__(self):
        return len(self._seq)

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
        return not (self == other)

    def __contains__(self, other):
        return other in self._seq

    def __reversed__(self):
        return reversed(self._seq)

    def __repr__(self):
        return name(self) + '(' + ', '.join(map(str, self._seq)) + ')'

    def copy(self):
        return type(self)(self)

    def update(self, *args):
        self.__init__(*args)