from pieces.nullPiece import nullPiece

class Knight(nullPiece):
    def __init__(self, alliance, x, y):
        self.alliance = alliance
        self.x_coord = x
        self.y_coord = y

    def toString(self):
        return "N"

    def validMove(self, board):
        
        return self.piecesMoves