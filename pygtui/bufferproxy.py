# NOTE: this module does not use this buffer like in native pygame, this module uses ndarray completely

import numpy as np

from ._utils import metadata

from ._utils.common import to_bytes

__all__ = [
    'BufferProxy'
]

class BufferProxy:

    def __init__(self, parent):
        self._parent = parent

    def __repr__(self):
        return f'<{type(self).__name__}({self.length})>'

    @property
    def parent(self):
        return self._parent

    @property
    def length(self):
        return self._parent.width * self._parent.height * 3

    @property
    def raw(self):
        return self._parent._array.tobytes()

    @parent.setter
    def parent(self, _):
        raise AttributeError(f"attribute 'parent' of '{metadata.MODULE_NAME}.bufferproxy.BufferProxy' objects is not writable")

    @length.setter
    def length(self, _):
        raise AttributeError(f"attribute 'length' of '{metadata.MODULE_NAME}.bufferproxy.BufferProxy' objects is not writable")

    @raw.setter
    def raw(self, _):
        raise AttributeError(f"attribute 'raw' of '{metadata.MODULE_NAME}.bufferproxy.BufferProxy' objects is not writable")

    @parent.deleter
    def parent(self):
        raise AttributeError(f"attribute 'parent' of '{metadata.MODULE_NAME}.bufferproxy.BufferProxy' objects is not writable")

    @length.deleter
    def length(self):
        raise AttributeError(f"attribute 'length' of '{metadata.MODULE_NAME}.bufferproxy.BufferProxy' objects is not writable")

    @raw.deleter
    def raw(self):
        raise AttributeError(f"attribute 'raw' of '{metadata.MODULE_NAME}.bufferproxy.BufferProxy' objects is not writable")

    def write(self, buffer, offset=0):
        raw = bytearray(self.raw)
        buffer = to_bytes(buffer)

        if buffer is None:
            raise TypeError(f"a bytes-like object is required, not '{type(buffer).__name__}'")
        if not isinstance(offset, int):
            raise TypeError(f"'{type(offset).__name__}' object cannot be interpreted as an integer")
        if not (0 <= offset < len(raw)):
            raise IndexError("'offset' is out of range")

        raw[offset:offset + len(buffer)] = buffer
        self._parent._array = np.frombuffer(raw, dtype=np.uint8,
                                                 count=self.length).reshape((self._parent.height,
                                                                             self._parent.width,
                                                                             3))