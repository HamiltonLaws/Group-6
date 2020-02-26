from pieces.nullPiece import nullPiece

class Bishop(nullPiece):
    def __init__(self, alliance, x, y):
        self.alliance = alliance
        self.x_coord = x
        self.y_coord = y

    def toString(self):
        return "B"