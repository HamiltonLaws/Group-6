from pieces.piece import piece
from rule.basicRule import checkPieces

class Pawn(piece):
    fMove = True

    def __init__(self, alliance, x, y):
        super().__init__(alliance, x, y)

    def toString(self):
        return "P"

    def validMove(self, board):
        super().validMove(board)
        if self.alliance == "W":
            self.piecesMoves.append([self.x_coord-1, self.y_coord])
            if self.fMove is True:
                self.piecesMoves.append([self.x_coord-2, self.y_coord])
                self.fMove = False
            if self.board[self.x_coord-1][self.y_coord+1].pieceOccupy.toString() != "0":
                self.piecesMoves.append([self.x_coord-1, self.y_coord+1])
            elif self.board[self.x_coord-1][self.y_coord-1].pieceOccupy.toString() != "0":
                self.piecesMoves.append([self.x_coord-1, self.y_coord-1])
        else:
            self.piecesMoves.append([self.x_coord+1, self.y_coord])
            if self.fMove is True:
                self.piecesMoves.append([self.x_coord+2, self.y_coord])
                self.fMove = False
            if self.y_coord+1 < 7 and self.board[self.x_coord+1][self.y_coord+1].pieceOccupy.toString() != "0":
                self.piecesMoves.append([self.x_coord+1, self.y_coord+1])
            if self.y_coord-1 > 0 and self.board[self.x_coord+1][self.y_coord-1].pieceOccupy.toString() != "0":
                self.piecesMoves.append([self.x_coord+1, self.y_coord-1])
        return checkPieces(board, self.piecesMoves, self)