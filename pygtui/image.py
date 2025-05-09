import numpy as np

from PIL import Image

from .surface import Surface

def load(path, namehint=None):
    image = Image.open(path).convert('RGB')
    surface = Surface(image.size)
    surface.array = np.array(image)
    return surface