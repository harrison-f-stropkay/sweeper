# Harrison Stropkay

import numpy as np
import random


class Minesweeper:
    BOMB = -1
    GAME_OVER = -2

    def __init__(self, tiles_height, tiles_width, num_bombs) -> None:
        self.tiles_height = tiles_height
        self.tiles_width = tiles_width
        self.num_bombs = num_bombs
        self.tiles = np.full([tiles_height, tiles_width], False)
        self.has_lost = False
        
        # get (num_bombs + 1) random integers in our range using a partial Fisher–Yates shuffle
        sequence = np.arange(0, tiles_width * tiles_height)
        for i in range(num_bombs + 1):
            random_index = random.randrange(len(sequence))
            sequence[random_index], sequence[i] = sequence[i], sequence[random_index]

        # insert values of True into tiles representing bombs
        for i in range(num_bombs):
            cur_tile = divmod(sequence[i], tiles_width)
            self.tiles[cur_tile] = True

        # save the extra random tile in case the user selects a bomb tile on first guess
        self.extra_tile = divmod(sequence[num_bombs], tiles_width)

    def reveal_tile(self, y, x) -> int:
        if self.has_lost:
            return self.GAME_OVER
        else:
            if self.tiles[y, x]:
                self.has_lost = True
                return self.GAME_OVER
            else:
                count = 0
                y_min, y_max = max(y - 1, 0), min(y + 1, self.tiles_height - 1)
                x_min, x_max = max(x - 1, 0), min(x + 1, self.tiles_width - 1)
                for y in range(y_min, y_max + 1):
                    for x in range(x_min, x_max + 1):
                        if self.tiles[y, x]:
                            count += 1
                return count

    def __str__(self) -> str:
        # add top left corner space
        result = " " * 2
        # add x indices
        for x in range(self.tiles_width):
            result += buffer('r', x)
        result += "\n"
        # add y indices and tile values
        for y in range(self.tiles_height):
            result += str(y) + " "
            for x in range(self.tiles_width):
                result += buffer('r', self.tiles[y, x])
            result += "\n"
        return result


def buffer(direction, *args) -> str:
    buffer_length = 7
    # set input to " " if input is not given as argument
    input = str(args[0]) if args else ""
    match direction:
        case 'l':
            return input.ljust(buffer_length)

        case 'r':
            return input.rjust(buffer_length)

        case 'c':
            if(len(input) > buffer_length):
                return input
            else:
                num_spaces = buffer_length - len(input)
                num_spaces_left = num_spaces // 2
                num_spaces_right = round(num_spaces / 2)
                return ' ' * num_spaces_left + input + ' ' * num_spaces_right
        # return error and usage if invalid direction is given
        case _:
            return "Error. Usage: buffer('l' | 'r', [input])"


test_tiles = Minesweeper(10, 12, 15)
print(test_tiles)

