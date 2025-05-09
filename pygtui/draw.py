from .math import Vector2
from .rect import Rect
from .color import Color

__all__ = [
    'rect',
    'line',
    'circle',
    'polygon'
]

def rect(surface, color, rect):
    sw, sh = surface.size
    l, t, w, h = Rect(rect)

    surface.array[max(t,0):min(t+h,sh), max(l,0):min(l+w,sw)] = Color(color)

def line(surface, color, start_pos, end_pos, width=1):
    sw, sh = surface.size
    array = surface.array
    color = Color(color)
    x1, y1 = Vector2(start_pos)
    x2, y2 = Vector2(end_pos)

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    vertical = dy > dx

    x, y = x1, y1
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    if width == 1:
        start, end = 0, 1
    else:
        distance = width // 2
        start, end = -distance, distance

    def draw():
        for i in range(start, end):
            if vertical:
                px = x + i
                if 0 <= px < sw and 0 <= y < sh:
                    array[y, px] = color
            else:
                py = y + i
                if 0 <= x < sw and 0 <= py < sh:
                    array[py, x] = color

    if dx > dy:
        err = dx / 2
        while x != x2:
            draw()
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2
        while y != y2:
            draw()
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    draw()

def circle(surface, color, center, radius, width=0):
    sw, sh = surface.size
    array = surface.array
    color = Color(color)
    cx, cy = Vector2(center)

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            px, py = cx + dx, cy + dy

            if 0 <= px < sw and 0 <= py < sh:
                distance = (dx ** 2 + dy ** 2)**0.5

                if width == 0 and distance <= radius:
                    array[py, px] = color

                elif width > 0 and radius - width / 2 <= distance <= radius + width / 2:
                    array[py, px] = color

def polygon(surface, color, points, width=0):
    array = surface.array
    color = Color(color)
    points = [Vector2(point) for point in points]

    num_points = len(points)
    for i in range(num_points):
        line(surface, color, points[i], points[(i + 1) % num_points], width)

    if width == 0:
        sorted_points = sorted(points, key=lambda p: p.y)
        min_y = sorted_points[0].y
        max_y = sorted_points[-1].y

        for y in range(min_y, max_y + 1):
            intersections = []
            for i in range(num_points):
                p1 = points[i]
                p2 = points[(i + 1) % num_points]

                if (p1.y <= y < p2.y) or (p2.y <= y < p1.y):
                    x_inter = p1.x + (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)
                    intersections.append(x_inter)

            intersections.sort()

            for i in range(0, len(intersections), 2):
                x1 = int(intersections[i])
                x2 = int(intersections[i + 1])
                for x in range(x1, x2 + 1):
                    array[y, x] = color