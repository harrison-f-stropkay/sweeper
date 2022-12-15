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

    def neighbors_iterate(self, y, x, func, arg) -> None:
        y_min, y_max = max(y - 1, 0), min(y + 1, self.height - 1)
        x_min, x_max = max(x - 1, 0), min(x + 1, self.width - 1)
        for current_y in range(y_min, y_max + 1):
            for current_x in range(x_min, x_max + 1):
                # skips iteration of given tile
                if current_y == y and current_x == x:
                    continue
                # call function with each neighbor value and given parameter
                func(self.tiles[current_y, current_x], arg)

    def tile_value(self, y, x) -> int:
        def if_bomb_add_one(value, arg) -> None:
            if value == codes.BOMB:
                arg[0] += 1

        count = [0]
        self.neighbors_iterate(y, x, if_bomb_add_one, count)
        return count[0]


def buffer(input="") -> str:
    return str(input).ljust(3)


test_field = Field(10, 10, codes.HIDDEN)
test_field.tiles[5, 4] = codes.BOMB
test_field.tiles[5, 5] = codes.BOMB
test_field.tiles[5, 6] = codes.BOMB
print(test_field.tile_value(4, 4))