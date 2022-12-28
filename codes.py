BOMB = -1
NOT_BOMB = -2
FLAGGED = -3
HIDDEN = -4
FLIPPED = -5
UNSET = -7

WON = 1
LOST = 2
ONGOING = 3

def symbol(input: int) -> str:
    if input == BOMB:
        return '*'
    elif input == NOT_BOMB:
        return ' '
    elif input == FLAGGED:
        return 'F'
    elif input == HIDDEN:
        return '-'
    elif input == 0:
        return ' '
    else:
        return str(input)