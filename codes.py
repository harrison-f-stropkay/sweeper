BOMB = -1
NOT_BOMB = -2
FLAGGED = -3
HIDDEN = -4

def symbol(input: int) -> str:      # TODO maybe detect if input is boolean so minefield can use boolean values?
    match(input):
        case [BOMB]: 
            return '*'
        case [NOT_BOMB]: 
            return '.'
        case [FLAGGED]:
            return 'F'
        case [HIDDEN]:
            return ' '
        case _:
            return str(input)