class Rule:
    board = None
    piecesMoves = []
    piece = None
    def __init__(self, board, moveList, piece):
        self.board = board
        self.piecesMoves = moveList
        self.piece = piece

class checkPieces(Rule):
    def __init__(self, board, moveList, piece):
        super().__init__(board, moveList, piece)

    def checkPieces(self):
        for i in self.piecesMoves:
            rows = i[0]
            cols = i[1]
            if self.board[rows][cols].pieceOccupy.toString() != "0":
                if self.board[rows][cols].pieceOccupy.alliance == self.piece.alliance:
                    self.piecesMoves.remove([rows, cols])
                if self.piece.toString() != "N" or self.piece.toString() != "K":
                    x = self.board[rows][cols].pieceOccupy.x_coord
                    y = self.board[rows][cols].pieceOccupy.y_coord
                    for j in self.piecesMoves:
                        if x < rows and j[0] < x:
                            self.piecesMoves.remove([j[0], j[1]])
                        elif x > rows and j[0] > x:
                            self.piecesMoves.remove([j[0], j[1]])
                        elif y < cols and j[1] < y:
                            self.piecesMoves.remove([j[0], j[1]])
                        elif y > cols and j[1] > y:
                            self.piecesMoves.remove([j[0], j[1]])
        return self.piecesMoves