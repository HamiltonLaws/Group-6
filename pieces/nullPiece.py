class nullPiece:
    alliance = None
    x_coord = None
    y_coord = None
    board = None
    piecesMoves = []

    def __init__(self):
        pass

    def toString(self):
        return "0"

    def validMove(self, board):
        return []