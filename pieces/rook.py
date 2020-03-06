from pieces.piece import piece
from rule.basicRule import checkPieces

class Rook(piece):
    def __init__(self, alliance, x, y):
        super().__init__(alliance, x, y)

    def toString(self):
        return "R"

    def validMove(self, board):
        super().validMove(board)

        #add valid move for x_coord
        for i in range(0,8):
            move = i - self.x_coord
            if (move != 0):
                self.piecesMoves.append([self.x_coord + move, self.y_coord])

        #add valid move for y_coord
        for i in range(0,8):
            move = i - self.y_coord
            if (move != 0):
                self.piecesMoves.append([self.x_coord, self.y_coord+move])

        check = checkPieces(board, self.piecesMoves, self)
        check.Check()
        return check.moveList