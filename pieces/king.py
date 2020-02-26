from pieces.nullPiece import nullPiece

class King(nullPiece):
    def __init__(self, alliance, x, y):
        self.alliance = alliance
        self.x_coord = x
        self.y_coord = y

    def toString(self):
        return "K"