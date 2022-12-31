from minesweeper_cli import MinesweeperCLI


total = 0
for i in range(1000):
    if MinesweeperCLI(30, 16, 99).auto_play():
        total += 1
print("total:", total)


# with guessing flags:
# ~88/100 on beginner    (9, 9, 10)
# ~70/100 on intermediate  (16, 16, 40)
# 32/100 on expert      (30, 16, 99)

# without guessing flags:
# 876/1000 on beginner    (9, 9, 10)
# 705/100 on intermediate  (16, 16, 40)
# /100 on expert      (30, 16, 99)