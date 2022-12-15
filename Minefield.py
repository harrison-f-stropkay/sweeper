import numpy as np
import random
import codes

class Minefield:
    def __init__(self, tiles_height, tiles_width, num_bombs) -> None:
        self.tiles_height = tiles_height
        self.tiles_width = tiles_width
        self.num_bombs = num_bombs
        self.tiles = np.full([tiles_height, tiles_width], False)
        self.first_guess = True
        
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
        # if first guess is a bomb tile, move that bomb to another tile
        if self.first_guess:
            self.first_guess = False
            if self.tiles[y, x]:
                self.tiles[y, x] = False
                self.tiles[self.extra_tile] = True
        # either return BOMB constant or the proper count
        if self.tiles[y, x]:
            return codes.BOMB
        else:
            count = 0
            y_min, y_max = max(y - 1, 0), min(y + 1, self.tiles_height - 1)
            x_min, x_max = max(x - 1, 0), min(x + 1, self.tiles_width - 1)      # TODO should use iterator in single_game
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    if self.tiles[y, x]:
                        count += 1
            return count

    



