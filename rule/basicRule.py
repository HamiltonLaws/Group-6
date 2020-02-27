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
            x = i[0][0]
            y = i[0][0] 