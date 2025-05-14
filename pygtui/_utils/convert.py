def convert_array_to_ansi(array):
    height, width, channel = array.shape
    lines = []

    if channel == 3:
        for y in range(0, height, 2):
            col = ''

            if y + 1 < height:
                for x in range(width):
                    tr, tg, tb = array[y, x]
                    br, bg, bb = array[y + 1, x]
                    col += f'\x1b[38;2;{tr};{tg};{tb}m\x1b[48;2;{br};{bg};{bb}m\u2580'

            else:
                for x in range(width):
                    tr, tg, tb = array[y, x]
                    col += f'\x1b[38;2;{tr};{tg};{tb}m\u2580'

            lines.append(col)

    elif channel == 4:
        # NOTE: alpha only has values ​​0 and 1

        for y in range(0, height, 2):
            col = ''

            if y + 1 < height:
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

            else:
                for x in range(width):
                    tr, tg, tb, ta = array[y, x]
                    if ta:
                        col += f'\x1b[38;2;{tr};{tg};{tb}m\u2580'
                    else:
                        col += '\x1b[0m '

            lines.append(col)

    return '\x1b[0m\n'.join(lines) + '\x1b[0m'