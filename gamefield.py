
import numpy as np
from field import Field
import codes


class Gamefield(Field):

    def __init__(self, width, height, number_bombs) -> None:
        super().__init__(width, height, number_bombs)
        self.number_flagged = 0                             # ever used?

    def get_guarantee_neighbors(self, tile) -> tuple | None:
        number_flagged_neighbors = 0
        number_flipped_neighbors = 0
        unflipped_neighbors = list()
        # get info about neighbors
        for neighbor in self.get_neighbors(tile):
            if self.tiles[neighbor] == codes.FLAGGED:
                number_flagged_neighbors += 1
            elif self.tiles[neighbor] == codes.HIDDEN:
                unflipped_neighbors.append(neighbor)
            else:
                number_flipped_neighbors += 1
        # if the info tells us there are guarantees, return them 
        tile_value = self.tiles[tile]
        if tile_value == number_flagged_neighbors:
            return (unflipped_neighbors, codes.HIDDEN)
        elif tile_value - number_flagged_neighbors == len(unflipped_neighbors):
            return (unflipped_neighbors, codes.FLAGGED)
        else:
            return None

    def get_number_untouched_tiles(self) -> int:
        number_untouched_tiles = 0
        for tile in np.ndindex(self.tiles.shape):
            if self.is_untouched(tile):
                number_untouched_tiles += 1
        return number_untouched_tiles

    def get_most_southeast_tile(self) -> tuple | None:
        for y in reversed(range(self.height)):
            for x in reversed(range(self.width)):
                if self.is_untouched(self.tiles[x, y]):
                    return (x, y)
        return None

    def is_flipped(self, tile: tuple) -> bool:
        return self.tiles[tile] >= 0 or self.tiles[tile] == codes.FLIPPED

    def in_outer_edge(self, tile) -> bool:
        if self.tiles == codes.HIDDEN:
            for neighbor in self.get_neighbors(tile):
                if self.is_flipped(neighbor):
                    return True
        return False

    def in_inner_edge(self, tile) -> bool:
        if self.is_flipped(tile):
            for neighbor in self.get_neighbors(tile):
                if self.tiles[neighbor] == codes.HIDDEN:
                    return True
        return False

    def is_guess_allowed(self, tile) -> bool:
        for neighbor in self.get_neighbors(tile):
            if self.is_flipped(neighbor):
                if not self.is_guess_allowed_neighbor(neighbor):
                    return False
        return True 
                
    def is_guess_allowed_neighbor(self, neighbor) -> bool:
        number_flagged = 0
        number_flipped = 0
        number_neighbors = 0
        for neighbor_of_neighbor in self.get_neighbors(neighbor):
            if self.tiles[neighbor_of_neighbor] == codes.FLAGGED:
                number_flagged += 1
            elif self.is_flipped(neighbor_of_neighbor):
                number_flipped += 1
            number_neighbors += 1
        return number_flagged > self.tiles[neighbor] or number_flipped > number_neighbors - self.tiles[neighbor]

    def is_untouched(self, tile) -> bool:
        for neighbor in self.get_neighbors(tile):
            if self.is_flipped(neighbor):
                return False
        return True