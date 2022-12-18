import codes

class Tile:
    def __init__(self, value) -> None:
        self.true_value: int = value
        self.game_value: int = codes.UNKNOWN