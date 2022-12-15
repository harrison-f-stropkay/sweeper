import numpy as np
import codes

class Field:
    def __init__(self, height, width, filler) -> None:
        self.height = height
        self.width = width
        self.tiles = np.full((height, width), filler)

    def __str__(self) -> str:
        # add top left corner space
        result = buffer()
        # add x indices
        for x in range(self.width):
            result += buffer(x)
        result += "\n"
        # add y indices and tile values
        for y in range(self.height):
            result += buffer(y)
            for x in range(self.width):
                result += buffer(codes.symbol(self.tiles[y, x]))
            result += "\n"
        return result

    def neightbors_iterate(self, y, x, func):
        y_min, y_max = max(y - 1, 0), min(y + 1, self.height - 1)
        x_min, x_max = max(x - 1, 0), min(x + 1, self.width - 1)
        for current_y in range(y_min, y_max + 1):
            for current_x in range(x_min, x_max + 1):
                # skips iteration of given tile
                if current_y == y and current_x == x:
                    continue
                # call function on each neighbor
                func(self, current_y, current_x)


def buffer(input="") -> str:
    return str(input).ljust(3)