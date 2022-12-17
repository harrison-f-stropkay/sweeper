import numpy as np
import random
from tile import Tile
import codes

class Board:
    
    def __init__(self, width, height, number_bombs) -> None:
        self.BOMB = -1
        self.NOT_BOMB = -2
        self.FLAGGED = -3
        self.HIDDEN = -4

        self.width = width
        self.height = height
        self.number_bombs = number_bombs
        self.first_guess = True
        self.tiles = np.empty((width, height), Tile)

        # create tiles
        number_tiles = width * height
        tiles_list = []
        for i in range(number_tiles - number_bombs):
            tiles_list.append(Tile(0))
        for i in range(number_bombs):
            tiles_list.append(Tile(codes.BOMB))

        # store extra non-bomb tile
        self.extra_tile = tiles_list[0]

        # Fisher–Yates shuffle
        for i in range(number_tiles):
            random_index = random.randrange(width * height - i)
            tiles_list[random_index], tiles_list[number_tiles - 1 - i] = tiles_list[number_tiles - 1 - i], tiles_list[random_index]

        # convert to numpy 2-d array
        self.tiles = np.array(tiles_list, dtype=Tile).reshape((width, height))


    def swap_bomb(self, location) -> None:
        self.tiles[location].true_value = 0
        self.extra_tile.true_value = codes.BOMB

    def get_neighbor_locations(self, location) -> list[tuple]:
        x, y = location[0], location[1]
        y_min, y_max = max(y - 1, 0), min(y + 1, self.height - 1)
        x_min, x_max = max(x - 1, 0), min(x + 1, self.width - 1)
        neighbor_locations = []
        for current_y in range(x_min, x_max + 1):
            for current_x in range(y_min, y_max, + 1):
                if current_y != x or current_x != y:
                    neighbor_locations.append((current_y, current_x))
        return neighbor_locations

    def set_tile_values(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y].true_value == codes.BOMB:
                    continue
                for neighbor_location in self.get_neighbor_locations((x, y)):
                    if self.tiles[neighbor_location].true_value == codes.BOMB:
                        self.tiles[x, y].true_value += 1
        
    def flip(self, location) -> None:
        if self.first_guess:
            self.first_guess = False
            if self.tiles[location].true_value == codes.BOMB:
                self.swap_bomb(location)
            self.set_tile_values()
            self.tiles[location].game_value = self.tiles[location].true_value
        
    def flag(self, location) -> None:
        self.tiles[location].game_value = codes.FLAG
        


    def __str__(self, mode="game"):
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
                if mode == "game":
                    result += buffer(codes.symbol(self.tiles[y, x].game_value))
                elif mode == "true":
                    result += buffer(codes.symbol(self.tiles[y, x].true_value))
            result += "\n"
        return result




def buffer(*args) -> str:
    input = args[0] if args else "" 
    return str(input).ljust(3)


    
test = Board(10, 10, 95)
print(test.__str__("true"))
print(test)

test.flip((5, 2))

print(test.__str__("true"))
print(test)

