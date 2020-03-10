from pieces.piece import piece
from rule.basicRule import checkPieces

class Queen(piece):
    def __init__(self, alliance, x, y):
        super().__init__(alliance, x, y)

    def toString(self):
        return "Q"
    
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

        for i in range(1,8):
            if(-1 <self.x_coord - i <8 and -1 <self.y_coord + i < 8 ):
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