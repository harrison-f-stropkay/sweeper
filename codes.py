BOMB = -1
NOT_BOMB = -2
FLAG = -3
UNKNOWN = -4

ONGOING = 0
LOST = -1
WON = 1

def symbol(input: int) -> str:
    if input == BOMB:
        return '*'
    elif input == NOT_BOMB:
        return ' '
    elif input == FLAG:
        return 'F'
    elif input == UNKNOWN:
        return '-'
    elif input == 0:
        return ' '
    else:
        return str(input)