import random
from board.chessBoard import Board
from pieces.nullPiece import nullPiece
from chessMain import promoteCheck

class Bot:
    board = None
    minionList = list()
    def __init__(self, board, pieces):