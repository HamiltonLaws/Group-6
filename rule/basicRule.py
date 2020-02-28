class Rule:
    board = None
    piecesMoves = []
    piece = None
    def __init__(self, board, moveList, piece):
        self.board = board
        self.piecesMoves = moveList
        self.piece = piece

class sameAlliance(Rule):
    def __init__(self, board, moveList, piece):
        super().__init__(board, moveList, piece)

    def checkAlliance(self):
        for i in self.piecesMoves:
            rows = i[0]
            cols = i[1]
            if self.board[rows][cols].pieceOccupy.alliance == self.piece.alliance:
                self.piecesMoves.remove([rows, cols])
                if self.piece.toString() != "N" or self.piece.toString() != "K":
                    x = self.board[rows][cols].pieceOccupy.x_coord
                    y = self.board[rows][cols].pieceOccupy.y_coord


        return self.piecesMoves