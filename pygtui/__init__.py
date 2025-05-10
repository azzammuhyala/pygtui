from . import (
    base as base,
    color as color,
    constants as constants,
    display as display,
    draw as draw,
    font as font,
    image as image,
    math as math,
    rect as rect,
    surface as surface,
    time as time,
    transform as transform
)

from .base import *
from .constants import *
# from .color import Color as Color
# from .math import Vector as Vector, Vector2 as Vector2, Vector3 as Vector3
from .rect import Rect as Rect
from .surface import Surface as Surface

from ._utils.error import error as error

import os

if 'PYGTUI_HIDE_SUPPORT_PROMPT' not in os.environ:
    import sys
    from ._utils import metadata
    print(f'{metadata.MODULE_NAME} {__version__} (Terminal Modern, Python {".".join(map(str, sys.version_info[0:3]))})')