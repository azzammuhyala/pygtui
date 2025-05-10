import pygtui
import keyboard # pip install keyboard

pygtui.init()

pygtui.display.set_caption('Ini PyGame di Terminal!')

running = True
screen = pygtui.display.set_mode((60, 60))
clock = pygtui.time.Clock()

while running:
    clock.tick(60)

    if keyboard.is_pressed('esc'):
        running = False

    screen.fill('#FFFFFF')

    pygtui.draw.rect(screen, '#000000', (10, 10, 40, 40))
    pygtui.draw.rect(screen, '#FF4200', (0, 0, 10, 10))
    pygtui.draw.rect(screen, '#00FF00', (50, 0, 10, 10))
    pygtui.draw.rect(screen, '#0000FF', (0, 50, 10, 10))
    pygtui.draw.rect(screen, '#FF00FF', (50, 50, 10, 10))

    pygtui.display.flip()

pygtui.quit()
