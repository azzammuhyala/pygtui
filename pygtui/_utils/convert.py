def convert_array_to_ansi(array):
    height, width, channel = array.shape
    lines = []

    if channel == 3:
        for y in range(0, height, 2):
            if y + 1 < height:
                lines.append(''.join(f'\x1b[38;2;{";".join(map(str, array[y, x]))}m\x1b[48;2;{";".join(map(str, array[y + 1, x]))}m\u2580' for x in range(width)))
            else:
                lines.append(''.join(f'\x1b[38;2;{";".join(map(str, array[y, x]))}m\u2580' for x in range(width)))

    elif channel == 4:
        # alpha works only in the range of values ​​0 and 1

        for y in range(0, height, 2):

            if y + 1 < height:
                col = ''

                for x in range(width):
                    tr, tg, tb, ta = array[y, x]
                    br, bg, bb, ba = array[y + 1, x]
                    if ta and ba:
                        col += f'\x1b[38;2;{tr};{tg};{tb}m\x1b[48;2;{br};{bg};{bb}m\u2580'
                    elif ta:
                        col += f'\x1b[38;2;{tr};{tg};{tb}m\u2580'
                    elif ba:
                        col += f'\x1b[38;2;{br};{bg};{bb}m\u2584'
                    else:
                        col += '\x1b[0m '

                lines.append(col)

            else:
                col = ''

                for x in range(width):
                    tr, tg, tb, ta = array[y, x]
                    if ta:
                        col += f'\x1b[38;2;{tr};{tg};{tb}m\u2580'
                    else:
                        col += '\x1b[0m '

                lines.append(col)

    return '\x1b[0m\n'.join(lines) + '\x1b[0m'