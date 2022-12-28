import numpy as np
import itertools
import codes


# TODO: change self.tiles[tile] type thing to just tile value, get neighbors return tile values instead? prolly not tho
class Field:

    def __init__(self, width, height, number_bombs) -> None:
        self.width = width
        self.height = height
        self.number_bombs = number_bombs
        self.number_tiles = width * height
        self.tiles = np.full((width, height), codes.HIDDEN)

    def get_neighbors(self, tile, n=1) -> list[tuple]:
        x, y = tile
        x_min, x_max = max(x - n, 0), min(x + n, self.width - 1)
        y_min, y_max = max(y - n, 0), min(y + n, self.height - 1)
        neighbor_tiles = list()
        for current_tile in itertools.product(range(x_min, x_max + 1), range(y_min, y_max + 1)):
            if current_tile != tile:
                neighbor_tiles.append(current_tile)
        return neighbor_tiles

    def __str__(self):
        # add top space and top left corner space
        result = "\n" + buffer()
        # add x indices
        for x in range(self.width):
            result += buffer(x)
        result += "\n"
        # add y indices and tile values
        for y in range(self.height):
            result += buffer(y)
            for x in range(self.width):
                result += buffer(codes.symbol(self.tiles[x, y]))
            result += "\n"
        return result


def buffer(*args) -> str:
    input = args[0] if args else "" 
    return str(input).ljust(3)
