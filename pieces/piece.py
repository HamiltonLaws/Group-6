class piece:
    alliance = None
    x_coord = None
    y_coord = None
    board = None
    piecesMoves = []

    def __init__(self, alliance, x, y):
        self.alliance = alliance
        self.x_coord = x
        self.y_coord = y

    def toString(self):
        return "0"

    def validMove(self, board):
        self.board = board