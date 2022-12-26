import numpy as np
import math
import random
import codes


class Minesweeper:
    def __init__(self, width, height, number_bombs) -> None:
        self.width = width
        self.height = height
        self.number_bombs = number_bombs
        self.number_bombs_remaining = number_bombs
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
            random_index = random.randrange(number_tiles - i)
            real_tiles_list[random_index], real_tiles_list[number_tiles - 1 - i] = real_tiles_list[number_tiles - 1 - i], real_tiles_list[random_index]
        # convert to numpy 2-d array
        self.real_tiles = np.array(real_tiles_list).reshape((width, height))



        self.inside_edges = []
        self.waters = []
        self.known = np.full(self.game_tiles.shape, False)

    def swap_bomb(self, location) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if self.real_tiles[x, y] == codes.NOT_BOMB:
                    self.real_tiles[x, y] = codes.BOMB
                    self.real_tiles[location] = codes.NOT_BOMB
                    return

    def get_neighbor_locations(self, location) -> list[tuple]:
        x, y = location
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
        
    def flip(self, location) -> list:
        flipped_tile_locations = []
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
            flipped_tile_locations.append(location)
        # when location maps to an unflipped tile t with value v, if t has v flagged neighbors, flip the rest of t's neighbors
        else:
            number_flagged_neighbors = 0
            for neighbor_location in self.get_neighbor_locations(location):
                if self.game_tiles[neighbor_location] == codes.FLAGGED:
                    number_flagged_neighbors += 1
            if number_flagged_neighbors == self.game_tiles[location]:
                flipped_tile_locations = []
                for neighbor_location in self.get_neighbor_locations(location):
                    if self.game_tiles[neighbor_location] == codes.UNFLIPPED:
                        recursive_flipped_tile_locations = self.flip(neighbor_location)
                        flipped_tile_locations.extend(recursive_flipped_tile_locations)
        # if guess is a zero tile, flip all neighboring tiles (including neighbors of additional 0 tiles discovered in the process)
        if self.real_tiles[location] == 0:
            for neighbor_location in self.get_neighbor_locations(location):
                if self.game_tiles[neighbor_location] == codes.UNFLIPPED:
                    recursive_flipped_tile_locations = self.flip(neighbor_location)
                    flipped_tile_locations.extend(recursive_flipped_tile_locations)
        # change game status if necessary
        if self.real_tiles[location] == codes.BOMB:
            self.status = codes.LOST
        elif self.number_unflipped == 0:
            self.status = codes.WON
        # return
        return flipped_tile_locations

    def flag(self, location) -> None:
        self.game_tiles[location] = codes.FLAGGED
        self.number_bombs_remaining -= 1

    def play(self) -> bool:
        print(self)
        # game loop
        while self.status == codes.ONGOING:
            location, command = self.prompt()
            # input looks like: x y F
            if command == "F":
                if self.game_tiles[location] == codes.UNFLIPPED:
                    self.flag(location)
                else:
                    print("Error. Cannot flag a revealed tile.")
            # input looks like: G (or empty)
            elif command == "G":
                self.set_outside_edges()
                self.set_inside_edges()
                print(self.guess())
            # input looks like: x y
            else:
                if self.game_tiles[location] == codes.FLAGGED:
                    self.game_tiles[location] = codes.UNFLIPPED
                else:
                    self.flip(location)
            # show player the current game state and update internals
            print(self)
        # print concluding message
        if self.status == codes.WON:
            print("Game won!")
            return True
        else:
            print("Game lost.")
            return False
    
    def prompt(self) -> tuple:
        try:
            line = input("Guess: ")
            if line in ["G", ""]:
                return ((), "G")
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
                    return (location, "F")
                else:
                    raise Exception()
            return (location, "")
        except:
            print("Invalid input, try again. Usage: x y [F]. Example: '5 2' to flip tile at column 5, row 2")
            return self.prompt()
            
    def __str__(self, mode="game"):
        # add top space and top left corner space
        result = "\n" + buffer()
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



# TODO: compare to probability of random tile having a bomb, choose random if better
# TODO: change everything to say location or opposite?
# TODO: efficiency: return a list of the guarantees and act accordingly, not one at a time
# TODO: improve set_inside_edges
# TODO: move sweeper to other file
    


    # returns the confidence in the guess
    def guess(self) -> float:
        # see if there is a guaranteed bomb or safe tile
        for edge in self.inside_edges:
            for location in edge:
                if (potential_neighbor := self.get_guarantee_neighbor(location)) == None:
                    continue
                assessment, location = potential_neighbor
                if assessment == codes.BOMB:
                    self.flag(location)
                    return float(1)
                if assessment == codes.NOT_BOMB:
                    self.flip(location)
                    return float(1)
        
        # otherwise, do what is most probably a good move
        # TODO: change codes.BOMB to codes.FLAGGED in sweeper cases
        location, guess, confidence = self.best_guess()
        print("Confidence, guess: ", confidence, ", ", guess)
        if guess == codes.FLAGGED:
            self.flag(location)
        elif guess == codes.FLIPPED:
            self.flip(location)
        return confidence
        

    def get_guarantee_neighbor(self, location) -> tuple | None:
        tile_value = self.game_tiles[location]
        number_flags = 0
        number_unflipped = 0
        # get info about neighbors
        for neighbor in self.get_neighbor_locations(location):
            if self.game_tiles[neighbor] == codes.FLAGGED:
                number_flags += 1
            elif self.game_tiles[neighbor] == codes.UNFLIPPED:
                number_unflipped += 1
        # if the info guarantees a tile value, return such an assessment  
        if tile_value in (number_flags, number_flags + number_unflipped):
            for neighbor in self.get_neighbor_locations(location):
                if self.game_tiles[neighbor] == codes.UNFLIPPED:
                    if tile_value == number_flags:
                        return (codes.NOT_BOMB, neighbor)
                    else:
                        return (codes.BOMB, neighbor)
        # when there are no obvious neighbor values
        return None


    def set_inside_edges(self) -> None:
        one_big_edge = set()
        for x in range(self.width):
            for y in range(self.height):
                if self.is_edge_tile((x, y)):
                    one_big_edge.add((x, y))
        self.inside_edges = [one_big_edge]


    def set_outside_edges(self) -> None:
        self.outside_edges = list()
        visited = np.full((self.width, self.height), False)
        for x in range(self.width):
            for y in range(self.height):
                location = (x, y)
                if not visited[location] and self.is_outer(location):
                    outside_edge = set()
                    self.seek_edge(location, outside_edge, visited)
                    self.outside_edges.append(outside_edge)
                else:
                    visited[location] = True
        for outside_edge in self.outside_edges:
            print(len(outside_edge), ": ", str(outside_edge))


    def seek_edge(self, location, outside_edge: set, visited) -> None:
        if not visited[location] and self.is_outer(location):
            visited[location] = True
            outside_edge.add(location)
            for neighbor in self.get_neighbor_locations(location):
                self.seek_edge(neighbor, outside_edge, visited)


    def is_flipped(self, location):
        tile_value = self.game_tiles[location]
        return tile_value >= 0 or tile_value == codes.FLIPPED


    def is_outer(self, location) -> bool:
        if self.is_flipped(location):
            return False
        for neighbor in self.get_neighbor_locations(location):
            if self.is_flipped(neighbor):
                return True
        return False
        

    def is_edge_tile(self, location) -> bool:
        has_flipped_neighbor = False
        has_unflipped_neighbor = False
        for neighbor in self.get_neighbor_locations(location):
            if self.game_tiles[neighbor] not in (codes.UNFLIPPED, codes.FLAGGED):
                has_flipped_neighbor = True
            elif self.game_tiles[neighbor] == codes.UNFLIPPED:
                has_unflipped_neighbor = True
        return has_flipped_neighbor and has_unflipped_neighbor


    # TODO: what if bad flag leads to best_guess with no possible configurations, would divide by 0, fix that


    def best_guess(self) -> tuple:
        self.prob_tiles = np.full((self.width, self.height), math.nan)

        # set all flipped tiles to flipped constant and get info for later
        number_flipped_tiles = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.game_tiles[x, y] >= 0:
                    self.prob_tiles[x, y] = codes.FLIPPED
                    number_flipped_tiles += 1

        # set all outside edge tiles probabilities and get info for later
        expected_number_outside_bombs = 0
        number_outside_tiles = 0
        for outside_edge in self.outside_edges:
            expected_number_outside_bombs += self.set_outside_edge_prob(outside_edge)
            number_outside_tiles += len(outside_edge)

        # find probability of a bomb being in an untouched tile
        expected_number_untouched_bombs = self.number_bombs_remaining - expected_number_outside_bombs
        number_untouched_tiles = self.width * self.height - number_flipped_tiles - number_outside_tiles
        probability_untouched_bomb = expected_number_outside_bombs / number_flipped_tiles

        # starting with untouched tile probability, see if any other probabilities are further from 0.5
        best_confidence = probability_untouched_bomb
        best_confidence_tile = None
        for x in range(self.width):
            for y in range(self.height):
                if self.prob_tiles[x, y] > 1 or self.prob_tiles[x, y] < 0:
                    continue
                current_confidence = 1 - (abs(self.prob_tiles[x, y] - 0.5))
                if current_confidence > best_confidence:
                    best_confidence = current_confidence
                    best_confidence_tile = (x, y)

        # if untouched is best, return the most south then east untouched tile (least likely to receive first guess bomb)
        flip_status = codes.FLAGGED if best_confidence > 0.5 else codes.FLIPPED
        if best_confidence_tile == None:
            for x in reversed(range(self.width)):
                for y in reversed(range(self.height)):
                    if self.game_tiles[x, y] == codes.UNFLIPPED:
                        return ((x, y), flip_status, best_confidence)
        else:
            return (best_confidence_tile, flip_status, best_confidence)

        # TODO: shouldn't need below line
        return ()

    # TODO: make outside edge its own object, put sweeper in its own too

    
    def set_outside_edge_prob(self, outside_edge) -> float:
        # relies on dicts being ordered, they are officially guaranteed to be ordered in python 3.7 and beyond
        tiles_to_sums = dict.fromkeys(outside_edge, 0)
        tiles_to_guesses = dict.fromkeys(outside_edge, codes.UNSET)
        rolling_sum = 0
        
        # put sums of all possible configurations in tiles_to_sums and get the total number of those configurations 
        number_configurations = self.recursive_configuration(tiles_to_guesses, tiles_to_sums)

        # set probability tiles for this edge and add probability to rolling sum
        for tile in outside_edge:
            probability = tiles_to_sums[tile] / number_configurations
            self.prob_tiles[tile] = probability
            rolling_sum += probability

        # reset game tiles
        for tile in outside_edge:
            self.game_tiles[tile] = codes.UNFLIPPED

        # return the expected number of bombs in this outside edge
        return rolling_sum



    def recursive_configuration(self, tiles_to_guesses: dict, tiles_to_sums) -> int:
        # if we complete a configuration, return 1
        # if we reach a dead end, return 0
        # if we are still in the middle of a potentially viable configuration, recursively add
        # so the root call of this function returns the number of complete configurations

        # first, set game tiles to match current configuration and get the current and next tile
        current_tile = None
        next_tile = None
        next_tile_set = False
        for tile, guess in tiles_to_guesses.items():
            self.game_tiles[tile] = guess
            if tile == codes.UNSET and not next_tile_set:
                next_tile = tile
                next_tile_set = True
            else:
                current_tile = tile

        # check that the current guess is viable at this stage in the configuration 
        if not self.guess_allowed(current_tile):
            return 0

        # in case we have a complete configuration
        if not next_tile_set:
            self.add_configuration_to_sums(tiles_to_guesses, tiles_to_sums)
            return 1

        # otherwise, recurse with copies
        flag_copy = tiles_to_guesses.copy()
        flip_copy = tiles_to_guesses.copy()
        flag_copy[next_tile] = codes.FLAGGED
        flip_copy[next_tile] = codes.FLIPPED
        return self.recursive_configuration(flag_copy, tiles_to_sums) + self.recursive_configuration(flip_copy, tiles_to_sums)

        
    def add_configuration_to_sums(self, tiles_to_guesses: dict, tiles_to_sums):
        for tile, guess in tiles_to_guesses:
            if guess == codes.BOMB:
                tiles_to_sums[tile] += 1
        
    
    def guess_allowed(self, location) -> bool:
        # for each numbered neighbor of location, see if guess is allowed
        for neighbor in self.get_neighbor_locations(location):
            if self.is_flipped(self.game_tiles[location]) and not self.guess_allowed_neighbor(neighbor):
                return False
        return True 
                
    
    def guess_allowed_neighbor(self, neighbor) -> bool:
        number_flags = 0
        number_flipped = 0
        number_neighbors = 0
        
        for neighbor_of_neighbor in self.get_neighbor_locations(neighbor):
            neighbor_of_neighbor_value = self.game_tiles[neighbor_of_neighbor]
            if neighbor_of_neighbor_value == codes.FLAGGED:
                number_flags += 1
            elif self.is_flipped(neighbor_of_neighbor_value):
                number_flipped += 1
            number_neighbors += 1

        neighbor_value = self.game_tiles[neighbor]
        too_many_flags = number_flags > neighbor_value
        too_many_flipped = number_flipped > number_neighbors - neighbor_value
        return too_many_flags or too_many_flipped
        

        
        

            


        
        
    




        
    

def buffer(*args) -> str:
    input = args[0] if args else "" 
    return str(input).ljust(3)



# expert:
# test = Minesweeper(30, 16, 99)

test = Minesweeper(12, 12, 12)
test.play()

