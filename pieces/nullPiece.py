from pieces.piece import piece

class nullPiece(piece):

    def __init__(self):
        pass

    def toString(self):
        return "0"

    def validMove(self, board):
        return []