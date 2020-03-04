class Rule:
    board = None
    piecesMoves = []
    piece = None
    moveList = []
    def __init__(self, board, piecesMoves, piece):
        self.board = board
        self.moveList = piecesMoves
        self.piece = piece

class checkPieces(Rule):
    def __init__(self, board, moveList, piece):
        super().__init__(board, moveList, piece)

    def Check(self):
        for i in self.moveList:
            if self.board[i[0]][i[1]].pieceOccupy.toString() != "0":
                if self.board[i[0]][i[1]].pieceOccupy.alliance == self.piece.alliance:
                    self.moveList.remove([i[0], i[1]])
                if self.piece.toString() != "N" or self.piece.toString() != "K":
                    for j in self.moveList:
                        if j[1] < i[1] < self.piece.y_coord or j[1] > i[1] > self.piece.y_coord:
                            self.moveList.remove(j)
                        elif (j[0] < i[0] < self.piece.x_coord or j[0] > i[0] > self.piece.x_coord) and j[1] == i[1] == self.piece.y_coord:
                            self.moveList.remove(j)
                if self.piece.toString() == "P":
                    if self.piece.alliance == "W" and i[0] < self.piece.x_coord and i[1] == self.piece.y_coord:
                        self.moveList.remove(i)
                    elif self.piece.alliance == "B" and i[0] > self.piece.x_coord and i[1] == self.piece.y_coord:
                        self.moveList.remove(i)
        return self.moveList