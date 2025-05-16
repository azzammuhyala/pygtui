import time
import os

LOAD_TIME = time.monotonic()

MODULE_FILE = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
MODULE_NAME = os.path.basename(MODULE_FILE)
MODULES = [
    os.path.splitext(s)[0]
    for s in os.listdir(MODULE_FILE)
    if os.path.isfile(os.path.join(MODULE_FILE, s)) and s.endswith('.py') and not s.startswith('_')
]

# main
INITIALIZE = False
# submain
INITIALIZE_DISPLAY = False
INITIALIZE_FONT = False

QUIT_CALLABLE = None

WINDOW_SURFACE = None

POSITION_WINDOW = (0, 0)

ERROR_MESSAGE = ''

CAPTION = ''
ICON_TITLE = ''