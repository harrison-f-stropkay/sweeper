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

    def get_neighbors(self, tile) -> list[tuple]:
        y = tile[0]
        x = tile[1]
        y_min = max(y - 1, 0)
        x_min = max(x - 1, 0) 
        y_max = min(y + 1, self.height - 1)
        x_max = min(x + 1, self.width - 1)

        neighbors = []
        for current_y in range(y_min, y_max + 1):
            for current_x in range(x_min, x_max + 1):
                if current_y != y or current_x != x:
                    neighbors.append((current_y, current_x))
        return neighbors


def buffer(*args) -> str:
    input = args[0] if args else "" 
    return str(input).ljust(3)
