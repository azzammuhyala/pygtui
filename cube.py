import pygtui

try:
    import pygame
except ModuleNotFoundError:
    # pygame belum ada di sistem
    pygame = None

import keyboard
import math

# pilih model modul disini (pygtui / pygame)
game = pygtui

game.init()

game.display.set_caption('Cube 3D')

running = True
screen = game.display.set_mode((120, 60))
clock = game.time.Clock()

# Titik-titik kubus (3D)
cube_points = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
]

# Edges: pasangan indeks titik yang membentuk sisi
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]

angle_x = 0
angle_y = 0

def rotate_x(point, angle):
    x, y, z = point
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    y2 = y * cos_theta - z * sin_theta
    z2 = y * sin_theta + z * cos_theta
    return (x, y2, z2)

def rotate_y(point, angle):
    x, y, z = point
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    x2 = x * cos_theta + z * sin_theta
    z2 = -x * sin_theta + z * cos_theta
    return (x2, y, z2)

def project(point):
    x, y, z = point
    z += 5  # menghindari pembagian dengan nol
    f = 85 / z
    x_proj = int(x * f) + 60
    y_proj = int(y * f) + 30
    return (x_proj, y_proj)

while running:
    clock.tick(24)

    if game is pygtui:
        # event untuk pygtui (menggunakan keyboard)
        if keyboard.is_pressed('esc'):
            running = False

    elif game is pygame:
        # event untuk pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    screen.fill('#000000')

    angle_x += 0.02
    angle_y += 0.02

    # Proyeksi semua titik ke 2D
    projected_points = []
    for point in cube_points:
        rotated = rotate_x(point, angle_x)
        rotated = rotate_y(rotated, angle_y)
        projected_points.append(project(rotated))

    # Gambar sisi-sisi
    for edge in edges:
        game.draw.line(
            screen,
            '#ffffff',
            projected_points[edge[0]],
            projected_points[edge[1]],
            2
        )

    game.display.flip()

game.quit()
