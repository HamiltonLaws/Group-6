from pieces.piece import piece
from rule.basicRule import checkPieces
from rule.basicRule import Castling

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

        # cState = Castling(board, self.piecesMoves, self)
        # if(cState.canCastle()):
        #     print("king true")
            # if(self.alliance == "B"):
            #     self.piecesMoves.append([0, 6])
            #     self.piecesMoves.append([0, 2])
            # else:
            #     self.piecesMoves.append([7, 6])
            #     self.piecesMoves.append([7, 2])


        validCheck = checkPieces(board, self.piecesMoves, self)
        validCheck.Check()
        return validCheck.moveList