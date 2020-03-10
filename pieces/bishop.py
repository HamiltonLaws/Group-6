from pieces.piece import piece
from rule.basicRule import checkPieces

class Bishop(piece):
    def __init__(self, alliance, x, y):
        super().__init__(alliance, x, y)

    def toString(self):
        return "B"

    def validMove(self, board):
        super().validMove(board)
        for i in range(1, 8):
            if (-1 < self.x_coord - i < 8 and -1 < self.y_coord + i < 8):
                self.piecesMoves.append([self.x_coord - i, self.y_coord + i])
            if (-1 < self.x_coord - i < 8 and -1 < self.y_coord - i < 8):
                self.piecesMoves.append([self.x_coord - i, self.y_coord - i])
            if (-1 < self.x_coord + i < 8 and -1 < self.y_coord + i < 8):
                self.piecesMoves.append([self.x_coord + i, self.y_coord + i])
            if (-1 < self.x_coord + i < 8 and -1 < self.y_coord - i < 8):
                self.piecesMoves.append([self.x_coord + i, self.y_coord - i])

        validCheck = checkPieces(board, self.piecesMoves, self)
        validCheck.Check()
        return validCheck.moveList