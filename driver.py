from minesweeper_cli import MinesweeperCLI

total = 0
for i in range(100):
    if MinesweeperCLI(16, 16, 40).auto_play():
        total += 1
print("total:", total)



# 91/100 on beginner    (9, 9, 10)
# 64/100 on intermediate  (16, 16, 40)
# 32/100 on expert      (30, 16, 99)