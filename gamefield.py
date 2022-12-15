import numpy as np
from minefield import *
import codes

class GameField:
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.game_field = np.full((height, width), codes.HIDDEN)

    