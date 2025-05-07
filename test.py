import pygtui
import keyboard # pip install keyboard

pygtui.init()

pygtui.display.set_caption('Ini adalah PyGame di Terminal!')

running = True
screen = pygtui.display.set_mode((60, 60))
clock = pygtui.time.Clock()

while running:
    if keyboard.is_pressed('esc'):
        running = False

    screen.fill('#FFFFFF')

    pygtui.draw.rect(screen, '#00FF00', (10, 10, 40, 40))
    pygtui.draw.rect(screen, '#0042FA', (0, 0, 10, 10))
    pygtui.draw.rect(screen, '#0042FA', (50, 0, 10, 10))
    pygtui.draw.rect(screen, '#0042FA', (0, 50, 10, 10))
    pygtui.draw.rect(screen, '#0042FA', (50, 50, 10, 10))

    pygtui.display.flip()

    clock.tick(60)

pygtui.quit()
