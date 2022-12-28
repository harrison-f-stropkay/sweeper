import numpy as np
import codes
from gamefield import Gamefield

# TODO: efficiency: return a list of the guarantees and act accordingly, not one at a time
# TODO: improve set_inside_edges
# TODO: move outside edge, (inside edge?) to new file
# TODO: change all for x in ... for y in ... to 1 iterable call
# TODO: eventually ensure finding outside edge is DFS and finding their probs is BFS, could stop early if prob = 1 in BFS
# TODO: use zip instead of i in range()... ?
# TODO: what if bad flag leads to best_guess with no possible configurations, would divide by 0, fix that

    
class Sweeper:

    def __init__(self, gamefield: Gamefield) -> None:
        self.gamefield = gamefield
        self.guarantees = list()
        self.inside_edge_tiles = list()
        self.outside_edges = list()

    def guess(self) -> tuple:
        return self.guarantee_guess() or self.prob_guess()

    def guarantee_guess(self) -> tuple | None:
        if len(self.guarantees) == 0:
            self.update_guarantees()
        if len(self.guarantees) > 0:
            return self.guarantees.pop()
        else:
            return None
    
    def update_guarantees(self) -> None:
        self.update_inside_edge_tiles()
        for tile in self.inside_edge_tiles:
            guarantee_neighbors = self.gamefield.get_guarantee_neighbors(tile)
            if guarantee_neighbors != None:
                for guarantee_neighbor in guarantee_neighbors[0]:
                    # tuple: tile, guess, 1.0 (confidence in the guess)
                    self.guarantees.append((guarantee_neighbor, guarantee_neighbors[1], float(1)))

    def update_inside_edge_tiles(self) -> None:
        self.inside_edge_tiles.clear()
        for tile in np.ndindex(self.gamefield.tiles.shape):
            if self.gamefield.in_outer_edge(tile):
                self.inside_edge_tiles.append(tile)

    def update_outside_edges(self) -> None:
        self.outside_edges.clear()
        visited = np.full(self.gamefield.tiles.shape, False)
        for tile in np.ndindex(self.gamefield.tiles.shape):   
            outside_edge = list()
            self.seek_edge(tile, outside_edge, visited)
            if len(outside_edge) > 0:
                self.outside_edges.append(outside_edge)

    def seek_edge(self, tile, outside_edge: list, visited) -> None:
        if not visited[tile]:
            visited[tile] = True
            if self.gamefield.in_outer_edge(tile):
                outside_edge.append(tile)
                for neighbor in self.gamefield.get_neighbors(tile):
                    self.seek_edge(neighbor, outside_edge, visited)

    def prob_guess(self) -> tuple:
        self.update_outside_edges()
        # create combined lists of outside edge tiles and probs 
        all_outside_edge_tiles = list()
        all_outside_edge_probs = list()
        for outside_edge in self.outside_edges:
            all_outside_edge_tiles.extend(outside_edge)
            all_outside_edge_probs.extend(self.get_outside_edge_probs(outside_edge))
        # add outside edge tiles to a list of options
        options = list(zip(all_outside_edge_tiles, all_outside_edge_probs))
        # if untouched tile(s) exist, add the most southeast to options (least likely to receive the moved first guess bomb)
        number_untouched_tiles = self.gamefield.get_number_untouched_tiles()
        if number_untouched_tiles > 0:
            expected_number_outside_edge_bombs = 0
            for prob in all_outside_edge_probs:
                expected_number_outside_edge_bombs += prob
            expected_number_untouched_bombs = self.gamefield.number_bombs - self.gamefield.number_flagged - expected_number_outside_edge_bombs
            options.append((self.gamefield.get_most_southeast_tile(), expected_number_untouched_bombs / number_untouched_tiles))
        # find and return the best option
        options_with_guess = list()
        for tile, prob in options:
            guess = codes.FLAGGED
            if prob < 0.5:
                prob = 1 - prob
                guess = codes.FLIPPED
            options_with_guess.append((tile, guess, prob))
        return options_with_guess[np.argmin(options_with_guess[2])]

    def get_outside_edge_probs(self, outside_edge) -> list:
        guesses = len(outside_edge) * [codes.HIDDEN]
        tallies = len(outside_edge) * [0]
        # get tallies and total number of configurations via recursion; use them to create probs
        number_configurations = self.recursive_configuration(outside_edge, guesses, tallies, 0)
        probs = list()
        for tally in tallies:
            probs.append(tally / number_configurations)
        # reset game tiles and return
        for tile in outside_edge:
            self.gamefield.tiles[tile] = codes.HIDDEN
        return probs

    def recursive_configuration(self, outside_edge: list, guesses: list, tallies: list, i) -> int:
        tile = outside_edge[i]
        guess = guesses[i]
        # set gamefield to match current configuration
        for j in range(len(outside_edge)):
            self.gamefield.tiles[outside_edge[j]] = guesses[j]
        # if we've reached a dead end, return 0
        if not self.gamefield.is_guess_allowed(tile):
            return 0
        # if we have a complete configuration, add the configuration to tallies and return 1
        if i == len(outside_edge) - 1:
            for j in range(len(outside_edge)):
                if guesses[j] == codes.FLAGGED:
                    tallies[j] += 1
            return 1
        # otherwise, recurse with copies and return a recursive sum
        guesses_flag = guesses.copy(); guesses_flag[i + 1] = codes.FLAGGED
        guesses_flip = guesses.copy(); guesses_flip[i + 1] = codes.FLIPPED
        return self.recursive_configuration(outside_edge, guesses_flag, tallies, i + 1) + self.recursive_configuration(outside_edge, guesses_flip, tallies, i + 1)

        
        

        
        

            
