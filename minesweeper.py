import codes
from minefield import Minefield
from gamefield import Gamefield


class Minesweeper:
    def __init__(self, width, height, number_bombs) -> None:
        self.number_tiles = width * height
        self.number_bombs = number_bombs
        self.minefield = Minefield(width, height, number_bombs)
        self.gamefield = Gamefield(width, height, number_bombs)
        self.number_flipped = 0
        self.first_guess = True
        self.game_status = codes.ONGOING 

    def flip(self, tile) -> None:
        if self.gamefield.tiles[tile] == codes.FLAGGED:
            print("Error. Cannot flip a flagged tile.")
            return
        # on first guess, initialize tile values (after moving a guessed bomb if necessary)
        if self.first_guess:
            self.minefield.swap_bomb_if_necessary(tile)
            self.minefield.set_tile_values()
            self.first_guess = False
        # if tile is unflipped, flip it
        if self.gamefield.tiles[tile] == codes.HIDDEN:
            self.gamefield.tiles[tile] = self.minefield.tiles[tile]
            self.number_flipped += 1
        # if tile is flipped and has guaranteed flippable neighbors, flip them via recursion
        elif self.gamefield.is_flipped(tile):
            guarantee_neighbors = self.gamefield.get_guarantee_neighbors(tile)
            if guarantee_neighbors != None and guarantee_neighbors[1] == codes.HIDDEN:
                for guarantee_neighbor in guarantee_neighbors:
                    self.flip(guarantee_neighbor)
        # if guess is a zero tile, flip all hidden neighboring tiles via recursion
        if self.minefield.tiles[tile] == 0:
            for neighbor in self.gamefield.get_neighbors(tile):
                if self.gamefield.tiles[neighbor] == codes.HIDDEN:
                    self.flip(neighbor)
        # update game status
        if self.minefield.tiles[tile] == codes.BOMB:
            self.game_status = codes.LOST
        elif self.number_flipped == self.number_tiles - self.number_bombs:
            self.game_status = codes.WON
            
        self.last_flip = tile            
    def flag_or_unflag(self, tile) -> None:
        if self.gamefield.tiles[tile] == codes.FLAGGED:
            self.gamefield.tiles[tile] = codes.HIDDEN
            self.gamefield.number_flagged -= 1
        else:
            self.gamefield.tiles[tile] = codes.FLAGGED
            self.gamefield.number_flagged += 1
