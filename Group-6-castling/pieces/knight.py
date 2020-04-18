from pieces.piece import piece
from rule.basicRule import checkPieces

class Knight(piece):
    def __init__(self, alliance, x, y):
        super().__init__(alliance, x, y)

    def toString(self):
        return "N"

    def validMove(self, board):
        super().validMove(board)

        # self.piecesMoves.append([self.x_coord-1, self.y_coord])
        # down right move
        if self.x_coord < 6 and self.y_coord < 7:
            self.piecesMoves.append([self.x_coord + 2, self.y_coord + 1])
        if self.x_coord < 7 and self.y_coord < 6:
            self.piecesMoves.append([self.x_coord + 1, self.y_coord + 2])
        # down left move
        if self.x_coord > 1 and self.y_coord < 7:
            self.piecesMoves.append([self.x_coord - 2, self.y_coord + 1])
        if self.x_coord > 0 and self.y_coord < 6:
            self.piecesMoves.append([self.x_coord - 1, self.y_coord + 2])
        # up right move
        if self.x_coord < 7 and self.y_coord > 1:
            self.piecesMoves.append([self.x_coord + 1, self.y_coord - 2])
        if self.x_coord < 6 and self.y_coord > 0:
            self.piecesMoves.append([self.x_coord + 2, self.y_coord - 1])
        # up left move
        if self.x_coord > 0 and self.y_coord > 1:
            self.piecesMoves.append([self.x_coord - 1, self.y_coord - 2])
        if self.x_coord > 1 and self.y_coord > 0:
            self.piecesMoves.append([self.x_coord - 2, self.y_coord - 1])

        check = checkPieces(board, self.piecesMoves, self)
        check.Check()
        return check.moveList