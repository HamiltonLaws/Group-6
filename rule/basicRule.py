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
                    for j in self.piecesMoves:
                        x = self.board[j[0]][j[1]].pieceOccupy.x_coord
                        y = self.board[j[0]][j[1]].pieceOccupy.y_coord
                        if y < cols:
                            self.piecesMoves.remove([j[0], j[1]])
                        elif y > cols:
                            self.piecesMoves.remove([j[0], j[1]])
                        elif x < rows:
                            self.piecesMoves.remove([j[0], j[1]])
                        elif x > rows:
                            self.piecesMoves.remove([j[0], j[1]])
        return self.piecesMoves