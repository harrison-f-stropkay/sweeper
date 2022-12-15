from field import Field
import numpy as np
import random
import codes

class Minefield(Field):
    def __init__(self, height, width, num_bombs) -> None:
        super().__init__(height, width, False)
        self.num_bombs = num_bombs
        self.first_guess = True
        
        # get (num_bombs + 1) random integers in our range using a partial Fisher–Yates shuffle
        sequence = np.arange(0, height * width)
        for i in range(num_bombs + 1):
            random_index = random.randrange(len(sequence))
            sequence[random_index], sequence[i] = sequence[i], sequence[random_index]

        # insert values of True into tiles representing bombs
        for i in range(num_bombs):
            cur_tile = divmod(sequence[i], width)
            self.tiles[cur_tile] = True

        # save the extra random tile in case the user selects a bomb tile on first guess
        self.extra_tile = divmod(sequence[num_bombs], width)

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
            return self.tile_value(y, x)

    



