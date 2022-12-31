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
# TODO: fix prob above 1 for untouched // think I fixed it
# TODO: add don't flag mode for guess, see if it does better
# TODO: store all extra options with prob 1 in guarantees
# TODO: clean up options/options with guess to just use one of those?
# TODO: check if tile in guarantees has been flipped by flip of recursive 0 tile
# TODO: simple guarantee should just return the flipped tile that has a guarantee neighbor, would auto-flip

class Sweeper:
    def __init__(self, gamefield: Gamefield) -> None:
        self.gamefield = gamefield
        self.inside_edge_tiles = list()
        self.outside_edges = list()
        self.guarantees = set()

    def guess(self) -> tuple:
        if len(self.guarantees) > 0:
            return self.guarantees.pop()
        self.assess_inside_edge_tiles()
        if len(self.guarantees) > 0:
            return self.guarantees.pop()
        self.assess_outside_edges_and_untouched()
        if len(self.guarantees) > 0:
            return self.guarantees.pop()
        else:
            return self.prob_guess
    
    def assess_inside_edge_tiles(self) -> None:
        # set inside_edge_tiles
        self.inside_edge_tiles.clear()
        for tile in np.ndindex(self.gamefield.tiles.shape):
            if self.gamefield.in_inner_edge(tile):
                self.inside_edge_tiles.append(tile)
        # set guarantees
        for tile in self.inside_edge_tiles:
            guarantee_neighbors = self.gamefield.get_guarantee_neighbors(tile)
            if guarantee_neighbors != None:
                for guarantee_neighbor in guarantee_neighbors[0]:
                    # tuple: tile, guess, 1.0 (confidence in the guess)
                    self.guarantees.add((guarantee_neighbor, guarantee_neighbors[1], float(1)))        

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

    def assess_outside_edges_and_untouched(self) -> None:
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
        # this will also cause every first guess to be in the bottom right corner; optimal because unflipped corners result in an increase in 50-50 guesses 
        number_untouched_tiles = self.gamefield.get_number_untouched_tiles()
        if number_untouched_tiles > 0:
            expected_number_outside_edge_bombs = 0
            for prob in all_outside_edge_probs:
                expected_number_outside_edge_bombs += prob
            expected_number_untouched_bombs = self.gamefield.number_bombs - self.gamefield.number_flagged - expected_number_outside_edge_bombs
            options.append((self.gamefield.get_most_southeast_untouched_tile(), expected_number_untouched_bombs / number_untouched_tiles))
        # find and return the best option
        options_with_guess = list()
        guarantees_with_guess = list()
        for tile, prob in options:
            guess = codes.FLAGGED
            if prob <= 0.5:
                prob = 1 - prob
                guess = codes.FLIPPED
            option_with_guess = (tile, guess, prob)
            options_with_guess.append(option_with_guess)
            if prob == 1:
                guarantees_with_guess.append(option_with_guess)
        if False: #len(guarantees_with_guess) > 0:
            self.guarantees.update(guarantees_with_guess)
        else:
            flip_options_with_guess = list(filter(lambda option: option[1] == codes.FLIPPED, options_with_guess))
            if len(flip_options_with_guess) == 0:
                flip_options_with_guess = options_with_guess
            prob_argmax = np.argmax(list(zip(*flip_options_with_guess))[2])
            self.prob_guess = flip_options_with_guess[prob_argmax]

    def get_outside_edge_probs(self, outside_edge) -> list:
        guesses = len(outside_edge) * [codes.HIDDEN]
        tallies = len(outside_edge) * [0]
        # set tallies and get total number of configurations via recursion
        number_configurations = self.recursive_configuration(outside_edge, guesses, tallies, -1)
        # reset gamefield
        for tile in outside_edge:
            self.gamefield.tiles[tile] = codes.HIDDEN
        # create and return probs
        probs = list()
        for tally in tallies:
            probs.append(tally / number_configurations)
        return probs        

    def recursive_configuration(self, outside_edge: list, guesses: list, tallies: list, i) -> int:
        # for the root call, just recurse with the first configurations
        if i != -1:
            tile = outside_edge[i]
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
        # recurse with copies and return a recursive sum
        guesses_flag = guesses.copy(); guesses_flag[i + 1] = codes.FLAGGED
        guesses_flip = guesses.copy(); guesses_flip[i + 1] = codes.FLIPPED
        return self.recursive_configuration(outside_edge, guesses_flag, tallies, i + 1) + self.recursive_configuration(outside_edge, guesses_flip, tallies, i + 1)

        