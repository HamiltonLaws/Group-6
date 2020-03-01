from pieces.piece import piece
from rule.basicRule import checkPieces

class Pawn(piece):
    fMove = True

    def __init__(self):
        super().__init__()

    def toString(self):
        return "P"

    def validMove(self, board):
        self.board = board
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
            if self.board[self.x_coord+1][self.y_coord+1].pieceOccupy.toString() != "0":
                self.piecesMoves.append([self.x_coord+1, self.y_coord+1])
            elif self.board[self.x_coord+1][self.y_coord-1].pieceOccupy.toString() != "0":
                self.piecesMoves.append([self.x_coord+1, self.y_coord-1])
        return checkPieces(board, self.piecesMoves, self)