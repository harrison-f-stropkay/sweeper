import codes
from minesweeper import Minesweeper
from sweeper import Sweeper


class MinesweeperCLI:
    def __init__(self, width, height, number_bombs) -> None:
        self.minesweeper = Minesweeper(width, height, number_bombs)
        self.sweeper = Sweeper(self.minesweeper.gamefield)

    def play(self, auto_play=False):
        while self.minesweeper.game_status == codes.ONGOING:
            print(self.minesweeper.gamefield)
            if auto_play:
                self.use_guess()
            else:
                tile, command = self.prompt()
                # input looks like: x y
                if command == codes.FLIPPED:
                    self.minesweeper.flip(tile)
                # input looks like: x y F
                elif command == codes.FLAGGED:
                    self.minesweeper.flag_or_unflag(tile)
                # input looks like: G (or empty)
                elif command == codes.GUESS:
                    self.use_guess()
        # when game is complete
        print(self.minesweeper.gamefield)
        if self.minesweeper.game_status == codes.WON:
            print("Game won!")
            return True
        else:
            print("Game lost.")
            return False

    def use_guess(self):
        tile, guess, prob = self.sweeper.guess()
        print(f"Confidence: {prob:.2f}")
        if guess == codes.FLIPPED:
            self.minesweeper.flip(tile)
        elif guess == codes.FLAGGED:
            self.minesweeper.flag_or_unflag(tile)

    def prompt(self) -> tuple:
        try:
            line = input("Guess: ")
            if line in ["G", ""]:
                return ((), codes.GUESS)
            line_split = line.split()
            tile = (int(line_split[0]), int(line_split[1]))
            if len(line_split) not in [2, 3]:
                raise Exception()
            if tile[0] < 0 or tile[0] >= self.minesweeper.gamefield.width:
                raise Exception()
            if tile[1] < 0 or tile[1] >= self.minesweeper.gamefield.height:
                raise Exception()
            if len(line_split) == 3:
                if line_split[2] == "F":
                    return (tile, codes.FLAGGED)
                else:
                    raise Exception()
            return (tile, codes.FLIPPED)
        except:
            print(
                "Invalid input, try again. Usage: x y [F]. Example: '5 2' to flip tile at column 5, row 2")
            return self.prompt()
