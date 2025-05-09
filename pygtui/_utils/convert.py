import numpy as np

def convert_array_to_ansi(array):
    if not isinstance(array, np.ndarray):
        raise ValueError("convert_array_to_ansi() arg array must be a numpy array")
    if array.dtype != np.uint8:
        raise ValueError("convert_array_to_ansi() arg array must be of type uint8")
    if len(array.shape) != 3:
        raise ValueError("convert_array_to_ansi() arg array must be a 3D dimension/shape")
    if array.shape[2] != 3:
        raise ValueError("convert_array_to_ansi() arg array only supports 3 channels with RGB format")

    height, width, _ = array.shape
    lines = []

    for y in range(0, height, 2):
        if y + 1 < height:
            lines.append(''.join(f'\x1b[38;2;{";".join(map(str, array[y, x]))}m\x1b[48;2;{";".join(map(str, array[y + 1, x]))}m\u2580' for x in range(width)))
        else:
            lines.append(''.join(f'\x1b[38;2;{";".join(map(str, array[y, x]))}m\u2580' for x in range(width)))

    return '\x1b[0m\n'.join(lines) + '\x1b[0m'