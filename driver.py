from minesweeper_cli import MinesweeperCLI

# beginner:      (9, 9, 10)
# intermediate:  (16, 16, 40)
# expert:        (30, 16, 99)

wins = 0
number_games = 10
for i in range(number_games):
    if MinesweeperCLI(9, 9, 10).play(auto_play=True):
        wins += 1
print(f"\nWins: {wins}/{number_games}\n")
