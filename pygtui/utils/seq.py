class SeqInt:

    def __init__(self, *args):
        pass

    def __getitem__(self, index):
        return self._seq[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            self._seq[index] = map(int, value)
        else:
            self._seq[index] = int(value)

    def __repr__(self):
        return type(self).__name__ + '(' + ', '.join(map(str, self._seq)) + ')'

    def __len__(self):
        return len(self._seq)

    def copy(self):
        return type(self)(self)