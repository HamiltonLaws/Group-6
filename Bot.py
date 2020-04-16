from pieces.nullPiece import nullPiece
from rule.basicRule import Check
from rule.basicRule import staleMate
import random

class Bot:
    selectedPiece = None
    pieceMove = None
    chessBoard = None
    pieces = None

    def __init__(self, chessBoard, pieces):
        self.chessBoard = chessBoard
        self.pieces = pieces
    
    def Move(self, selectedPiece, x, y):
        chessBoard = self.chessBoard
        x_origin = selectedPiece.x_coord
        y_origin = selectedPiece.y_coord
        moves = 0

        if chessBoard.board[x][y].pieceOccupy.toString() != "0":
            moves = 0
        else:
            moves = 1 

        if selectedPiece.toString() == "P":
            moves = 0
            if selectedPiece.x_coord +2 == x or selectedPiece.x_coord -2 == x:
                selectedPiece.passP = True

            if selectedPiece.alliance == "B" and y != y_origin:
                if chessBoard.board[x-1][y].pieceOccupy.toString() == "P":
                    if chessBoard.board[x-1][y].pieceOccupy.passP == True:
                        chessBoard.updateBoard(x-1, y, nullPiece())

            if selectedPiece.alliance == "W" and y != y_origin:
                if chessBoard.board[x+1][y].pieceOccupy.toString() == "P":
                    if chessBoard.board[x+1][y].pieceOccupy.passP == True:
                        chessBoard.updateBoard(x+1, y, nullPiece())
        selectedPiece.x_coord = x
        selectedPiece.y_coord = y
        selectedPiece.fMove = False
        chessBoard.updateBoard(x, y, selectedPiece)
        chessBoard.updateBoard(x_origin, y_origin, nullPiece())
        if selectedPiece.toString() == "P":
            promoteChoice = ["Q", "R", "N", "B"]
            if selectedPiece.alliance == "W" and selectedPiece.x_coord == 0:
                promoteTo = random.choice(promoteChoice)
                chessBoard.promote(selectedPiece.x_coord, selectedPiece.y_coord, "W", promoteTo)

            if selectedPiece.alliance == "B" and selectedPiece.x_coord == 7:
                promoteTo = random.choice(promoteChoice)
                chessBoard.promote(selectedPiece.x_coord, selectedPiece.y_coord, "B", promoteTo)

        return moves

class dumbBot(Bot):
    def __init__(self, chessBoard, pieces):
        super().__init__(chessBoard, pieces)

    def randomMoves(self):
        selectedPiece = self.selectedPiece
        chessBoard = self.chessBoard
        pieces = self.pieces
        while True:
            chosenPiece = random.choice(pieces)
            rows = (int)(chosenPiece[0]/75)
            cols = (int)(chosenPiece[1]/75)
            selectedPiece = chessBoard.board[rows][cols].pieceOccupy
            pieceMove = selectedPiece.validMove(chessBoard.board)
            if pieceMove == list():
                continue
            else: 
                break
        print("Bot selected", selectedPiece, "at coordination: [", selectedPiece.x_coord, ", ", selectedPiece.y_coord, "]")
        chosenMove = random.choice(pieceMove)
        x = chosenMove[0]
        y = chosenMove[1]
        moves = super().Move(selectedPiece, x, y)
        return selectedPiece, moves