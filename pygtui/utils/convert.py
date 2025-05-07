def convert_array_to_ansi(array):
    height, width, _ = array.shape
    lines = []

    for y in range(0, height, 2):
        string = ''

        if y + 1 < height:
            for x in range(width):
                string += f'\x1b[38;2;{";".join(map(str, array[y, x]))}m\x1b[48;2;{";".join(map(str, array[y + 1, x]))}m\u2580'
        else:
            for x in range(width):
                string += f'\x1b[38;2;{";".join(map(str, array[y, x]))}m\u2580'

        lines.append(string)

    return '\x1b[0m\n'.join(lines) + '\x1b[0m'