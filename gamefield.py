import numpy as np
from minefield import *
import codes

class GameField:
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.game_field = np.full((height, width), codes.HIDDEN)

    def __str__(self) -> str:
        # add top blank line and top left corner space
        result = "\n" + buffer()
        # add x indices
        for x in range(self.tiles_width):
            result += buffer(x)
        result += "\n"
        # add y indices and tile values
        for y in range(self.tiles_height):
            result += buffer(y)
            for x in range(self.tiles_width):
                match self.gamefield[y, x]:
                    case codes.HIDDEN:
                        result += buffer()
                    case codes.BOMB:
                        result += buffer('*')
                    case codes.FLAGGED:
                        result += buffer('F')
                    case _:
                        result += buffer(str(self.gamefield[y, x]))
            result += "\n"
        return result

    def neightbors_iterate(self, y, x, func(self, y, x)):
        y_min, y_max = max(y - 1, 0), min(y + 1, self.height - 1)
        x_min, x_max = max(x - 1, 0), min(x + 1, self.width - 1)
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                func(self, y, x)