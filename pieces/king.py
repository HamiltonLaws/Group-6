from pieces.piece import piece

class King(piece):
    def __init__(self, alliance, x, y):
        super().__init__(alliance, x, y)

    def toString(self):
        return "K"

    def validMove(self, board):
        super().validMove(board)
        return []