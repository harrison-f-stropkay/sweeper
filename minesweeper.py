import codes
from minefield import *
from gamefield import *
from field import Field


class SingleGame:
    def __init__(self, tiles_height, tiles_width, num_bombs) -> None:
        self.tiles_height = tiles_height
        self.tiles_width = tiles_height
        self.minefield = Minefield(tiles_height, tiles_width, num_bombs)
        self.gamefield = Gamefield(tiles_height, tiles_width)
        self.first_guess = True

    def reveal_tile(self, tile) -> None:
        # if first guess is a bomb tile, move that bomb to another tile
        if self.first_guess:
            self.first_guess = False
            if self.minefield.tiles[tile]:
                self.minefield.tiles[tile] = False
                self.minefield.tiles[self.minefield.extra_tile] = True
        # put tile value from minefield into gamefield
        self.gamefield.tiles[tile] = self.minefield.tile_value(tile)

    # returns True if game is won, False if lost
    def play(self) -> bool:
        print(self)
        while (True):
            guessed_tile = scan_guess()
            result = self.minefield.tiles[guessed_tile]
            # if player's first guess is a bomb tile, move that bomb to another tile
            if self.first_guess:
                self.first_guess = False
                if result == codes.BOMB:
                    self.minefield.tiles[guessed_tile] = codes.NOT_BOMB
                    self.minefield.tiles[self.minefield.extra_tile] = codes.BOMB
            # if player's guess is a zero tile, flip all neighboring tiles (including neighbors of additional 0 tiles discovered in the process)
            if result == 0:
                zero_tiles = [guessed_tile]
                while zero_tiles:
                    current_tile = zero_tiles.pop()
                    for neighbor in self.gamefield.get_neighbors(current_tile):
                        self.reveal_tile(neighbor)
                        if (self.gamefield.tiles[neighbor] == 0):
                            zero_tiles.append(neighbor)

            # record tile value in game model
            self.gamefield.tiles[guessed_tile] = result
            print(self.gamefield)
            # exit loop if game lost
            if result == codes.BOMB:
                print("Game over")
                return False

def scan_guess() -> tuple:
    while (True):
        try:
            line = input("Guess: ")
            line_split = line.split()
            return (int(line_split[0]), int(line_split[1]))
            # TODO move to except if more than 2 or given or if theyre out of bounds
        except:
            print("Invalid input, try again. Usage: int int. Example: 5 2 for row 5, column 2")


    

test_game = SingleGame(10, 10, 12)
#print(test_game.minefield)
test_game.play()
