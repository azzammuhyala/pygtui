from .math import Vector2
from .rect import Rect
from .color import Color

def rect(surface, color, rect):
    color = Color(color)
    rect = Rect(rect)

    x1 = min(rect.right, surface.width)
    y1 = min(rect.bottom, surface.height)
    x2 = max(rect.left, 0)
    y2 = max(rect.top, 0)

    surface.array[y2:y1, x2:x1] = color

def pixel(surface, color, pos, width=1):
    color = Color(color)
    pos = Vector2(pos)
    radius = width // 2

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            px = pos.x + dx
            py = pos.y + dy
            if 0 <= px < surface.width and 0 <= py < surface.height:
                surface.array[py, px] = color

def line(surface, color, start_pos, end_pos, width=1):
    color = Color(color)
    start_pos = Vector2(start_pos)
    end_pos = Vector2(end_pos)

    dx = abs(end_pos.x - start_pos.x)
    dy = abs(end_pos.y - start_pos.y)

    x, y = start_pos.x, start_pos.y
    sx = 1 if end_pos.x > start_pos.x else -1
    sy = 1 if end_pos.y > start_pos.y else -1

    if dx > dy:
        err = dx / 2
        while x != end_pos.x:
            pixel(surface, color, (x, y), width)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2
        while y != end_pos.y:
            pixel(surface, color, (x, y), width)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    pixel(surface, color, (x, y), width)

def circle(surface, color, center, radius, width=1):
    color = Color(color)
    center = Vector2(center)

    for y in range(center.y - radius, center.y + radius + 1):
        for x in range(center.x - radius, center.x + radius + 1):
            if (x - center.x)**2 + (y - center.y)**2 <= radius**2:
                if width == 1:
                    surface.array[y, x] = color
                else:
                    for i in range(-width // 2, width // 2 + 1):
                        for j in range(-width // 2, width // 2 + 1):
                            if (x + i - center.x)**2 + (y + j - center.y)**2 <= radius**2:
                                surface.array[y + i, x + j] = color

def polygon(surface, color, points, width=1):
    color = Color(color)
    points = list(map(Vector2, points))

    n = len(points)
    for i in range(n):
        start_pos = points[i]
        end_pos = points[(i + 1) % n]
        line(surface, color, start_pos, end_pos, width)