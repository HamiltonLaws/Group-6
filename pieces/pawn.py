from pieces.nullPiece import nullPiece
from rule.basicRule import sameAlliance

class Pawn(nullPiece):
    fMove = True

    def __init__(self, alliance, x, y):
        self.alliance = alliance
        self.x_coord = x
        self.y_coord = y

    def toString(self):
        return "P"

    def validMove(self, board):
        if self.alliance == "W":
            self.piecesMoves.append([self.x_coord-1, self.y_coord])
            if self.fMove is True:
                self.piecesMoves.append([self.x_coord-2, self.y_coord])
                self.fMove = False
        else:
            self.piecesMoves.append([self.x_coord+1, self.y_coord])
            if self.fMove is True:
                self.piecesMoves.append([self.x_coord+2, self.y_coord])
                self.fMove = False
        return sameAlliance(board, self.piecesMoves, self)