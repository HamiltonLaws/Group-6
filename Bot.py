from pieces.nullPiece import nullPiece
from rule.basicRule import Check
from rule.basicRule import staleMate
from rule.basicRule import Castling
import random

class Bot:
    selectedPiece = None
    pieceMove = None
    chessBoard = None
    pieces = None

    def __init__(self, chessBoard, pieces):
        self.chessBoard = chessBoard
        self.pieces = pieces

    def castleRook(self, prevY, newY, selectedPiece):       
        print("move rook")
        chessBoard = self.chessBoard
        # print("toString after call", selectedPiece.toString())
        # **old and new positions:
        # Lf bR = (0,0) => (0, 3)
        # Rt bR = (0,7) => (0, 5)
        # Lf wR = (7, 0) => (7, 3)
        # Rt wR = (7, 7) => (7, 5) 
        # bK (0, 4) => L (0, 2), R (0, 6)
        # wK (7, 4) => L (7, 2), R(7, 6)
        castleState = Castling(chessBoard, selectedPiece.validMove, selectedPiece)

        if(selectedPiece.toString() == "K" and castleState.canCastle()):
            if (selectedPiece.alliance == "B"):
                if (newY == prevY + 2): # black right
                    chessBoard.updateBoard(0, 5, chessBoard.board[0][7].pieceOccupy)
                    chessBoard.board[0][5].pieceOccupy.y_coord = 5
                    chessBoard.updateBoard(0, 7, nullPiece())
                elif (newY == prevY - 2): # black left
                    chessBoard.updateBoard(0, 3, chessBoard.board[0][0].pieceOccupy)
                    chessBoard.board[0][3].pieceOccupy.y_coord = 3
                    chessBoard.updateBoard(0, 0, nullPiece())
            else:
                if (newY == prevY + 2): # white right
                    chessBoard.updateBoard(7, 5, chessBoard.board[7][7].pieceOccupy)
                    chessBoard.board[7][5].pieceOccupy.y_coord = 5
                    chessBoard.updateBoard(7, 7, nullPiece())
                elif (newY == prevY - 2): # white left
                    chessBoard.updateBoard(7, 3, chessBoard.board[7][0].pieceOccupy)
                    chessBoard.board[7][3].pieceOccupy.y_coord = 3
                    chessBoard.updateBoard(7, 0, nullPiece())
    
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
        self.castleRook(y_origin, y, selectedPiece)
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
        moves = 0
        selectedPiece = None
        removeList = []
        while pieces:
            chosenPiece = random.choice(pieces)
            rows = (int)(chosenPiece[0]/75)
            cols = (int)(chosenPiece[1]/75)
            if (rows, cols) not in removeList:
                selectedPiece = chessBoard.board[rows][cols].pieceOccupy
                pieceMove = selectedPiece.validMove(chessBoard.board)
                if pieceMove == list():
                    removeList.append((rows, cols))
                    pieces = [i for i in pieces if i not in removeList]
                    selectedPiece = None
                    if pieces == set():
                        break
                    continue
                else: 
                    print("Bot selected", selectedPiece, "at coordination: [", selectedPiece.x_coord, ", ", selectedPiece.y_coord, "]")
                    ck = Castling(chessBoard, selectedPiece.validMove, selectedPiece)
                    if(selectedPiece.toString() == "K"):
                        if (selectedPiece.alliance == "B"):
                            if ck.canCastleR():
                                print("castle bR")
                                pieceMove.append([0, 6])
                            if ck.canCastleL():
                                print("castle bL")
                                pieceMove.append([0, 2])
                        else:
                            if ck.canCastleR():
                                print("castle wL")
                                pieceMove.append([7, 6])
                            if ck.canCastleL():
                                print("castle wR")
                                pieceMove.append([7, 2])
                    chosenMove = random.choice(pieceMove)
                    x = chosenMove[0]
                    y = chosenMove[1]
                    moves = super().Move(selectedPiece, x, y)
                    break
        return selectedPiece, moves