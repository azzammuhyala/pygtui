import re

from operator import add, sub, mul, truediv, floordiv, pow, mod, neg, eq, ne

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

    def __neg__(self):
        return type(self)(map(neg, self))

    def __invert__(self):
        return type(self)(map(neg, self)) # alias

    def __eq__(self, other):
        return all(map(eq, self, type(self)(other)))

    def __ne__(self, other):
        return all(map(ne, self, type(self)(other)))

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

for func in (add, sub, mul, truediv, floordiv, pow, mod):
    func_name = func.__name__

    # define the wrapper (closure) function
    def wrapper(f):
        return lambda self, other: type(self)(map(f, self, type(self)(other)))

    # overload the operator functions
    setattr(Seq, '__' + func_name + '__', wrapper(func))

    def wrapper(f):
        return lambda self, other: type(self)(map(f, type(self)(other), self))

    # overload the reverse operator functions
    setattr(Seq, '__r' + func_name + '__', wrapper(func))

    # overload the in-place operator functions
    def wrapper(f):
        def inplace(self, other):
            self[:] = map(f, self, type(self)(other))
            return self
        return inplace

    setattr(Seq, '__i' + func_name + '__', wrapper(func))