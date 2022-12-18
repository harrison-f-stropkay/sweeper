import codes
from board import Board

# returns True if game is won, False if lost
def play(board) -> bool:
    print(board)
    # game loop
    while board.status == codes.ONGOING:
        board.flip(scan_guess())
        print(board)
    # print concluding message
    if board.status == codes.WON:
        print("Game won!")
        return True
    else:
        print("Game lost.")
        return False
    
    

def scan_guess() -> tuple:
    while True:
        try:
            line = input("Guess: ")
            line_split = line.split()
            return (int(line_split[0]), int(line_split[1]))
            # TODO move to except if more than 2 or given or if theyre out of bounds
        except:
            print("Invalid input, try again. Usage: int int. Example: 5 2 for row 5, column 2")


    

test = Board(10, 10, 10)
play(test)