BOMB = -1
NOT_BOMB = -2
FLAGGED = -3
HIDDEN = -4

def symbol(input: int) -> str:      # TODO maybe detect if input is boolean so minefield can use boolean values?
    if input == BOMB:
        return '*'
    elif input == NOT_BOMB: 
        return '.'
    elif input == FLAGGED:
        return 'F'
    elif input == HIDDEN:
        return ' '
    else:
        return str(input)