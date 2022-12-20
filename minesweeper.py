import numpy as np
import random
import codes


class Minesweeper:
    def __init__(self, width, height, number_bombs) -> None:
        self.width = width
        self.height = height
        self.number_bombs = number_bombs
        self.first_guess = True
        self.game_tiles = np.full((width, height), codes.UNFLIPPED)
        self.status = codes.ONGOING
        self.number_unflipped = width * height - number_bombs
        # create tiles
        number_tiles = width * height
        real_tiles_list = []
        for i in range(number_bombs):
            real_tiles_list.append(codes.BOMB)
        for i in range(number_tiles - number_bombs):
            real_tiles_list.append(codes.NOT_BOMB)
        # Fisher–Yates shuffle
        for i in range(number_tiles):
            random_index = random.randrange(width * height - i)
            real_tiles_list[random_index], real_tiles_list[number_tiles - 1 - i] = real_tiles_list[number_tiles - 1 - i], real_tiles_list[random_index]
        # convert to numpy 2-d array
        self.real_tiles = np.array(real_tiles_list).reshape((width, height))

    def swap_bomb(self, location) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if self.real_tiles[x, y] == codes.NOT_BOMB:
                    self.real_tiles[x, y] = codes.BOMB
                    self.real_tiles[location] = codes.NOT_BOMB
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
                if self.real_tiles[x, y] == codes.BOMB:
                    continue
                value = 0
                for neighbor_location in self.get_neighbor_locations((x, y)):
                    if self.real_tiles[neighbor_location] == codes.BOMB:
                        value += 1
                self.real_tiles[x, y] = value
        
    def flip(self, location) -> None:
        # on first guess, move bomb if necessary then initialize all non-bomb tile values
        if self.first_guess:
            self.first_guess = False
            if self.real_tiles[location] == codes.BOMB:
                self.swap_bomb(location)
            self.set_tile_values()
        # when location maps to an unflipped tile, flip it
        if self.game_tiles[location] == codes.UNFLIPPED:
            self.game_tiles[location] = self.real_tiles[location]
            self.number_unflipped -= 1
        # when location maps to an unflipped tile t with value v, if t has v flagged neighbors, flip the rest of t's neighbors
        else:
            number_flagged_neighbors = 0
            for neighbor_location in self.get_neighbor_locations(location):
                if self.game_tiles[neighbor_location] == codes.FLAG:
                    number_flagged_neighbors += 1
            if number_flagged_neighbors == self.game_tiles[location]:
                for neighbor_location in self.get_neighbor_locations(location):
                    if self.game_tiles[neighbor_location] == codes.UNFLIPPED:
                        self.flip(neighbor_location)
        # if guess is a zero tile, flip all neighboring tiles (including neighbors of additional 0 tiles discovered in the process)
        if self.real_tiles[location] == 0:
            for neighbor_location in self.get_neighbor_locations(location):
                if self.game_tiles[neighbor_location] == codes.UNFLIPPED:
                    self.flip(neighbor_location)
        # change game status if necessary
        if self.real_tiles[location] == codes.BOMB:
            self.status = codes.LOST
        elif self.number_unflipped == 0:
            self.status = codes.WON

    def flag(self, location) -> None:
        self.game_tiles[location] = codes.FLAG                        

    def play(self) -> bool:
        print(self)
        # game loop
        while self.status == codes.ONGOING:
            cleaned_input = self.scan_guess()
            # when input is of the form x y
            if type(cleaned_input[0]) == int:
                location = cleaned_input
                if self.game_tiles[location] == codes.FLAG:
                    self.game_tiles[location] = codes.UNFLIPPED
                else:
                    self.flip(cleaned_input)
            # when input is of the form x y F
            else:
                location = cleaned_input[0]
                if self.game_tiles[location] == codes.UNFLIPPED:
                    self.flag(location)
                else:
                    print("Error. Cannot flag a revealed tile.")
            print(self)
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
                raise Exception()
            if location[0] < 0 or location[0] >= self.width:
                raise Exception()
            if location[1] < 0 or location[1] >= self.height:
                raise Exception()
            if len(line_split) == 3:
                if line_split[2] == "F":
                    return (location, line_split[2])
                else:
                    raise Exception()
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
                    result += buffer(codes.symbol(self.game_tiles[x, y]))
                elif mode == "true":
                    result += buffer(codes.symbol(self.real_tiles[x, y]))
            result += "\n"
        return result


def buffer(*args) -> str:
    input = args[0] if args else "" 
    return str(input).ljust(3)


test = Minesweeper(10, 10, 12)
test.play()
