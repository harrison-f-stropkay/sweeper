import numpy as np
import codes
from minefield import *
from gamefield import *

class SingleGame:
    def __init__(self, tiles_height, tiles_width, num_bombs) -> None:
        self.tiles_height = tiles_height
        self.tiles_width = tiles_height
        self.minefield = Minefield(tiles_height, tiles_width, num_bombs)
        self.gamefield = GameField(tiles_height, tiles_width)
    
    # returns True if game is won, False if lost
    def play(self) -> bool:
        print(self)
        while (True):
            y, x = scan_guess()
            result = self.minefield.reveal_tile(x, y)
            # automatically flip any tiles neighboring a 0 tile
            if result == 0:
                zero_tiles = [(y, x)]

                def flip(self, y, x) -> None:
                    self.gamefield = self.minefield.reveal_tile(y, x)

                while zero_tiles:
                    self.gamefield.neightbors_iterate(y, x, function (): )
                    
            # record tile value in game model
            self.gamefield[y, x] = result
            # show new model
            print(self)
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
