import numpy as np
from field import Field
import codes

class Gamefield(Field):
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.tiles = np.full((height, width), codes.HIDDEN)

