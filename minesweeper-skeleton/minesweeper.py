# Harrison Stropkay

import numpy as np
import random

class Minesweeper:
    def __init__(self, board_height, board_width, num_bombs) -> None:
        self.board_height = board_height
        self.board_width = board_width
        self.num_bombs = num_bombs
        self.board = np.zeros([board_height, board_width], np.int8)
        
        # get (num_bombs + 1) random integers in our range using a partial Fisher–Yates shuffle
        sequence = np.arange(0, board_width * board_height)
        for i in range(num_bombs + 1):
            random_index = random.randrange(len(sequence))
            sequence[random_index], sequence[i] = sequence[i], sequence[random_index]
        print(sequence)

        # insert values of -1 into board representing bombs
        for i in range(num_bombs):
            cur_tile = divmod(sequence[i], board_width)
            self.board[cur_tile] = -1

            # increment the value of each neighboring non-bomb tile
            y_min = max(0, cur_tile[0] - 1)
            x_min = max(0, cur_tile[1] - 1)
            y_max = min(board_height - 1, cur_tile[0] + 1)
            x_max = min(board_width - 1, cur_tile[1] + 1)
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    if self.board[y, x] != -1:
                        self.board[y, x] += 1

        # save the extra random tile in case the user selects a bomb tile on first guess
        self.extra_tile = divmod(sequence[num_bombs], board_width)
        print("Extra random tile: " + str(self.extra_tile))


    def __str__(self) -> str:
        # add top left corner space
        result = buffer() * 2

        # add width indices
        for x in range(self.board_width):
            result += buffer(x)
        result += "\n\n"

        for y in range(self.board_height):
            # add height indices
            result += buffer(y)
            result += buffer()
            for x in range(self.board_width):
                # add tile values
                result += buffer(self.board[y, x])
            result += "\n"

        return result



def buffer(*args) -> str:
    input = str(args[0]) if args else ""
    buffer_length = 3
    return input.rjust(buffer_length)




test_board = Minesweeper(20, 30, 250)
print(test_board)

