import numpy as np
import random
import codes
from field import Field


class Minefield(Field):
    def __init__(self, width, height, number_bombs) -> None:
        super().__init__(width, height, number_bombs)
        self.set_bombs()

    def set_bombs(self) -> None:
        tiles_list = list()
        for i in range(self.number_bombs):
            tiles_list.append(codes.BOMB)
        for i in range(self.number_tiles - self.number_bombs):
            tiles_list.append(codes.NOT_BOMB)
        # Fisher–Yates shuffle
        for i in range(self.number_tiles):
            random_index = random.randrange(self.number_tiles - i)
            tiles_list[random_index], tiles_list[self.number_tiles - 1 - i] = tiles_list[self.number_tiles - 1 - i], tiles_list[random_index]
        # convert to numpy 2-d array
        self.tiles = np.array(tiles_list).reshape((self.width, self.height))
        
    def swap_bomb_if_necessary(self, tile) -> None:
        if self.tiles[tile] == codes.BOMB:
            for y in range(self.height):
                for x in range(self.width):
                    if self.tiles[x, y] == codes.NOT_BOMB:
                        self.tiles[x, y] = codes.BOMB
                        self.tiles[tile] = codes.NOT_BOMB
                        return
        
    def set_tile_values(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y] == codes.BOMB:
                    continue
                value = 0
                for neighbor_tile in self.get_neighbors((x, y)):
                    if self.tiles[neighbor_tile] == codes.BOMB:
                        value += 1
                self.tiles[x, y] = value
