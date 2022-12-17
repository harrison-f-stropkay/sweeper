BOMB = -1
NOT_BOMB = -2
FLAG = -3
HIDDEN = -4

def symbol(input: int) -> str:
    if input == BOMB:
        return '*'
    elif input == FLAG:
        return 'F'
    elif input == HIDDEN:
        return '.'
    elif input == 0:
        return ' '
    else:
        return str(input)