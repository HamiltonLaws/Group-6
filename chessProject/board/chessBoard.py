from pieces.nullPiece import nullPiece
from pieces.pawn import Pawn

class Tile:
    pieceOccupy = None
    def __init__(self, piece):
        pieceOccupy = piece

class Board:
    board = [[0 for i in range(8)] for j in range(8)]

    def createBoard(self):
        for rows in range(8):
            for cols in range(8):
                self.board[rows][cols] = Tile(nullPiece())

        for cols in range(8):
            self.board[1][cols] = Tile(Pawn("B", 1, cols))

        for cols in range(8):
            self.board[6][cols] = Tile(Pawn("W", 6, cols))

    '''
    def printBoard(self):
        for _ in range(8):
            for _ in range(8)
                print("|", end=self.board)
    '''