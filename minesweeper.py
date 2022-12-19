import numpy as np
import random
from tile import Tile
import codes

# TODO: make vscode recognize instance methods
# TODO: unflag / what happens if you flip/flag a flagged tile

class Minesweeper:
    def __init__(self, width, height, number_bombs) -> None:
        self.width = width
        self.height = height
        self.number_bombs = number_bombs
        self.first_guess = True
        self.tiles = np.empty((width, height))
        self.status = codes.ONGOING
        self.number_unflipped = width * height - number_bombs
        # create tiles
        number_tiles = width * height
        tiles_list = []
        for i in range(number_tiles - number_bombs):
            tiles_list.append(Tile(codes.NOT_BOMB))
        for i in range(number_bombs):
            tiles_list.append(Tile(codes.BOMB))
        # Fisher–Yates shuffle
        for i in range(number_tiles):
            random_index = random.randrange(width * height - i)
            tiles_list[random_index], tiles_list[number_tiles - 1 - i] = tiles_list[number_tiles - 1 - i], tiles_list[random_index]
        # convert to numpy 2-d array
        self.tiles = np.array(tiles_list, dtype=Tile).reshape((width, height))


    def swap_bomb(self, location) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[x, y].true_value == codes.NOT_BOMB:
                    self.tiles[x, y].true_value = codes.BOMB
                    self.tiles[location].true_value = codes.NOT_BOMB
                    return

    def get_neighbor_locations(self, location) -> list[tuple]:
        x, y = location[0], location[1]
        y_min, y_max = max(y - 1, 0), min(y + 1, self.height - 1)
        x_min, x_max = max(x - 1, 0), min(x + 1, self.width - 1)
        neighbor_locations = []
        for current_y in range(x_min, x_max + 1):
            for current_x in range(y_min, y_max + 1):
                if current_y != x or current_x != y:
                    neighbor_locations.append((current_y, current_x))
        return neighbor_locations

    def set_tile_values(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y].true_value == codes.BOMB:
                    continue
                value = 0
                for neighbor_location in self.get_neighbor_locations((x, y)):
                    if self.tiles[neighbor_location].true_value == codes.BOMB:
                        value += 1
                self.tiles[x, y].true_value = value

        
    def flip(self, location) -> None:
        # on first guess, move bomb if necessary then initialize all non-bomb tile values
        if self.first_guess:
            self.first_guess = False
            if self.tiles[location].true_value == codes.BOMB:
                self.swap_bomb(location)
            self.set_tile_values()
        # when location maps to an unflipped tile, flip it
        if self.tiles[location].game_value == codes.UNFLIPPED:
            self.tiles[location].game_value = self.tiles[location].true_value
            self.number_unflipped -= 1
        # when location maps to an unflipped tile t with value v, if t has v flagged neighbors, flip the rest of t's neighbors
        else:
            number_flagged_neighbors = 0
            for neighbor_location in self.get_neighbor_locations(location):
                if self.tiles[location].game_value == codes.FLAG:
                    number_flagged_neighbors += 1
            if number_flagged_neighbors == self.tiles[location].game_value:
                for neighbor_location in self.get_neighbor_locations(location):
                    self.flip(neighbor_location)

        # if guess is a zero tile, flip all neighboring tiles (including neighbors of additional 0 tiles discovered in the process)
        if self.tiles[location].true_value == 0:
            for neighbor_location in self.get_neighbor_locations(location):
                if self.tiles[neighbor_location].game_value == codes.UNFLIPPED:
                    self.flip(neighbor_location)
        # change game status if necessary
        if self.tiles[location].true_value == codes.BOMB:
            self.status = codes.LOST
        elif self.number_unflipped == 0:
            self.status = codes.WON
        
    def flag(self, location) -> None:
        self.tiles[location].game_value = codes.FLAG

    def play(self) -> bool:
        print(self)
        # game loop
        while self.status == codes.ONGOING:
            cleaned_input = self.scan_guess()
            if type(cleaned_input[0]) == tuple:
                self.flag(cleaned_input[0])
            else:
                self.flip(cleaned_input)
            print(self)
            print(self.__str__("true"))

        # print concluding message
        if self.status == codes.WON:
            print("Game won!")
            return True
        else:
            print("Game lost.")
            return False
    
    def scan_guess(self) -> tuple:
        try:
            line = input("Guess: ")
            line_split = line.split()
            location = (int(line_split[0]), int(line_split[1]))
            if len(line_split) not in [2, 3]:
                raise Exception() # "Too few or too many arguments given"
            if location[0] < 0 or location[0] >= self.width:
                raise Exception()
            if location[1] < 0 or location[1] >= self.height:
                raise Exception()
            if len(line_split) == 3:
                if line_split[2] == "F":
                    return (location, line_split[2])
                else:
                    raise Exception() # "Optional third argument must be 'F'"
            return location
        except:
            print("Invalid input, try again. Usage: x y [F]. Example: '5 2' to flip tile at column 5, row 2")
            return self.scan_guess()

            

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
                    result += buffer(codes.symbol(self.tiles[x, y].game_value))
                elif mode == "true":
                    result += buffer(codes.symbol(self.tiles[x, y].true_value))
            result += "\n"
        return result


def buffer(*args) -> str:
    input = args[0] if args else "" 
    return str(input).ljust(3)



test = Minesweeper(10, 10, 12)
test.play()
