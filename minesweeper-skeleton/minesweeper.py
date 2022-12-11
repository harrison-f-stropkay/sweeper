# Harrison Stropkay

import numpy as np
import random


class Minesweeper:
    def __init__(self, board_height, board_width, num_bombs) -> None:
        self.board_height = board_height
        self.board_width = board_width
        self.num_bombs = num_bombs
        self.board = np.full([board_height, board_width], False)
        
        # get (num_bombs + 1) random integers in our range using a partial Fisher–Yates shuffle
        sequence = np.arange(0, board_width * board_height)
        for i in range(num_bombs + 1):
            random_index = random.randrange(len(sequence))
            sequence[random_index], sequence[i] = sequence[i], sequence[random_index]

        # insert values of True into board representing bombs
        for i in range(num_bombs):
            cur_tile = divmod(sequence[i], board_width)
            self.board[cur_tile] = True

        # save the extra random tile in case the user selects a bomb tile on first guess
        self.extra_tile = divmod(sequence[num_bombs], board_width)

    def __str__(self) -> str:
        # add top left corner space
        result = " " * 2
        # add x indices
        for x in range(self.board_width):
            result += buffer('r', x)
        result += "\n"
        # add y indices and tile values
        for y in range(self.board_height):
            result += str(y) + " "
            for x in range(self.board_width):
                result += buffer('r', self.board[y, x])
            result += "\n"
        return result



def buffer(direction, *args) -> str:
    buffer_length = 7
    # set input to " " if input is not given as argument
    input = str(args[0]) if args else ""
    match direction:
        case 'l':
            return input.ljust(buffer_length)

        case 'r':
            return input.rjust(buffer_length)

        case 'c':
            if(len(input) > buffer_length):
                return input
            else:
                num_spaces = buffer_length - len(input)
                num_spaces_left = num_spaces // 2
                num_spaces_right = round(num_spaces / 2)
                return ' ' * num_spaces_left + input + ' ' * num_spaces_right
        # return error and usage if invalid direction is given
        case _:
            return "Error. Usage: buffer('l' | 'r', [input])"


test_board = Minesweeper(10, 12, 15)
print(test_board)

