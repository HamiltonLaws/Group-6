class Rule:
    board = None
    piecesMoves = []
    def __init__(self, board, moveList):
        self.board = board
        self.piecesMoves = moveList

class sameAlliance(Rule):
    def __init__(self, board, moveList):
        super().__init__(board, moveList)

    def checkAlliance(self):
        for i in self.piecesMoves:
            rows =i[0]
            cols = i[1]
            if self.board[rows][cols].pieceOccupy == "0":
                self.piecesMoves.remove([rows, cols])
            return self.piecesMoves