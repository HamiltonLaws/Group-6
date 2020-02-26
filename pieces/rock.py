from pieces.nullPiece import nullPiece

class Rock(nullPiece):
    def __init__(self, alliance, x, y):
        self.alliance = alliance
        self.x_coord = x
        self.y_coord = y

    def toString(self):
        return "R"