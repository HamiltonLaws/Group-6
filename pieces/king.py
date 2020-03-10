from pieces.piece import piece
from rule.basicRule import checkPieces

class King(piece):
    def __init__(self, alliance, x, y):
        super().__init__(alliance, x, y)

    def toString(self):
        return "K"

    def validMove(self, board):
        super().validMove(board)
        if self.x_coord < 7:
            self.piecesMoves.append([self.x_coord+1, self.y_coord])
            if 0 < self.y_coord < 7:
                self.piecesMoves.append([self.x_coord+1, self.y_coord+1])
                self.piecesMoves.append([self.x_coord+1, self.y_coord-1])
        if self.x_coord > 0:
            self.piecesMoves.append([self.x_coord-1, self.y_coord])
            if 0 < self.y_coord < 7:
                self.piecesMoves.append([self.x_coord-1, self.y_coord+1])
                self.piecesMoves.append([self.x_coord-1, self.y_coord-1])
        if 0 < self.y_coord < 7:
            self.piecesMoves.append([self.x_coord, self.y_coord+1])
            self.piecesMoves.append([self.x_coord, self.y_coord-1])

        validCheck = checkPieces(board, self.piecesMoves, self)
        validCheck.Check()
        return validCheck.moveList