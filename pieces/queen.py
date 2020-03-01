from pieces.piece import piece

class Queen(piece):
    def __init__(self, alliance, x, y):
        super().__init__(alliance, x, y)

    def toString(self):
        return "Q"
    
    def validMove(self, board):
        super().validMove(board)
        return []