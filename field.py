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

def buffer(input="") -> str:
    return str(input).ljust(3)