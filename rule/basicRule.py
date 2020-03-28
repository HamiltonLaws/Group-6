class Rule:
    board = None
    piecesMoves = []
    piece = None
    moveList = []
    removeList = []
    def __init__(self, board, piecesMoves, piece):
        self.board = board
        self.moveList = piecesMoves
        self.piece = piece
    
    def Check(self):
        self.removeList.clear()

class checkPieces(Rule):
    def __init__(self, board, moveList, piece):
        super().__init__(board, moveList, piece)

    def Check(self):
        super().Check()
        for i in self.moveList:
            if self.board[i[0]][i[1]].pieceOccupy.toString() != "0":
                if self.board[i[0]][i[1]].pieceOccupy.alliance == self.piece.alliance:
                    self.removeList.append(i)
                elif self.piece.toString() == "P":
                    if self.piece.alliance == "W" and i[0] < self.piece.x_coord and i[1] == self.piece.y_coord:
                        self.removeList.append(i)
                    elif self.piece.alliance == "B" and i[0] > self.piece.x_coord and i[1] == self.piece.y_coord:
                        self.removeList.append(i)
                if len(self.moveList) == 0 or self.piece.toString() != "N" and self.piece.toString() != "K":
                    for j in self.moveList:
                        if j in self.removeList:
                            continue
                        if j[0] == i[0] == self.piece.x_coord:
                            if j[1] < i[1] < self.piece.y_coord:
                                self.removeList.append(j)
                            elif j[1] > i[1] > self.piece.y_coord:
                                self.removeList.append(j)
                        elif j[1] == i[1] == self.piece.y_coord:
                            if j[0] < i[0] < self.piece.x_coord:
                                self.removeList.append(j)
                            elif j[0] > i[0] > self.piece.x_coord:
                                self.removeList.append(j)
                        elif j[1] > i[1] > self.piece.y_coord and j[0] < i[0] < self.piece.x_coord:
                            self.removeList.append(j)
                        elif j[1] < i[1] < self.piece.y_coord and j[0] < i[0] < self.piece.x_coord:   
                            self.removeList.append(j)
                        elif j[1] > i[1] > self.piece.y_coord and j[0] > i[0] > self.piece.x_coord:  
                            self.removeList.append(j)
                        elif j[1] < i[1] < self.piece.y_coord and j[0] > i[0] > self.piece.x_coord:   
                            self.removeList.append(j)
        self.moveList = [i for i in self.moveList if i not in self.removeList]
        
class checked:
    playerPieceMoves = []
    opponentPieceMoves= []
    playerKingPlace = []
    opponentKingPlace = []
    playerKingMoves= []
    opponentKingMoves = []
    board = None
    alliance= None
    message = False
    def __init__(self, board, alliance):
        self.board = board
        self.alliance = alliance
        

    def Clear(self):
        self.playerPieceMoves.clear()
        self.opponentPieceMoves.clear()
        self.playerKingPlace.clear()
        self.opponentKingPlace.clear()
        self.message = False
        self.playerKingMoves.clear()
        self.opponentKingMoves.clear()

class Check(checked):
    def _init_(self,board,alliance):
        super().__init__(board,alliance)
    
    def isCheck(self):
        super().Clear()
        curent = None
        curentMove = None
        # pieceMoves retuns a list of all the posible moves from the current player, kingPlace returns the placment of the oppoite king
        for rows in range(8):
            for cols in range(8):
                curent = self.board[rows][cols].pieceOccupy
                if(curent.toString() != "0" and curent.toString() != "K" and curent.alliance == self.alliance):
                    curentMove = curent.validMove(self.board)
                    self.playerPieceMoves.append(curentMove)
                elif(curent.toString() != "0" and curent.toString() != "K" and curent.alliance != self.alliance):
                    curentMove = curent.validMove(self.board)
                    self.opponentPieceMoves.append(curentMove)
                elif(curent.toString() == "K" and curent.alliance != self.alliance):
                    curentMove = curent.validMove(self.board)
                    self.opponentKingMoves.append(curentMove)
                    self.opponentKingPlace = [curent.x_coord,curent.y_coord]
                elif(curent.toString() == "K" and curent.alliance == self.alliance):
                    curentMove = curent.validMove(self.board)
                    self.playerKingMoves.append(curentMove)
                    self.playerKingPlace = [curent.x_coord,curent.y_coord]
        #check the other king is in check           
        for i in range(len(self.playerPieceMoves)):
            for j in range(len(self.playerPieceMoves[i])):
                if(self.opponentKingPlace == self.playerPieceMoves[i][j]):
                    self.message = True
        return self.message  

class castling(Rule):

    def __init__(self, board, moveList, piece):
        super().__init__(board, moveList, piece)

    #fulfills requirements:
        # 1) selected castle hasn't moved
        # 2) king has not moved
        # 3) king is not in check
        # 4) squares between are not occupied
        # 5) king does not end on contested tile

        # bK = (0, 4); wK = (7, 4); bR = (0,0)(0,7); wR = (7,0)(7,7)
    def canCastle(self, board):
        kingMoved = True
        rookMoved = True
        kingInCheck = True     # waiting on Hamilton to pass check/mate boolean
        betwInCheck = True
        betwEmpty = False

        # sets the relative x coordinate depending on your alliance (side)
        if (self.alliance is "B"):
            kx = 0
        else:
            kx = 7

        # check your king's starting coordinate; if it's not there, auto fail
        if (self.board[kx][4].pieceOccupy.toString is "K"and self.board[kx][4].pieceOccupy.alliance is self.alliance):
            yourK = self.board[kx][4].pieceOccupy
            kingMoved = not yourK.fmove
        else:
            return False

        # has either rook moved?
        r1Moved = True         # which rook
        r2Moved = True
        cornerPiece1, cornerPiece2 = self.board[kx][7].pieceOccupy, self.board[kx][0].pieceOccupy
        if(cornerPiece1.toString is "R" and cornerPiece1.alliance is self.alliance):
            r1Moved = not cornerPiece1.fmove
        if(cornerPiece2.toString is "R" and cornerPiece2.alliance is self.alliance):
            r2Moved = not cornerPiece2.fmove
        rookMoved = r1Moved or r2Moved

        # are the spaces between empty?
        betw1Empty = False
        betw2Empty = False
        if(not r1Moved):
            for y in range(1, 4): # spaces (1, 2, 3) between left rook and king
                if(self.board[kx][y].pieceOccupy.toString is "0"):
                    betw1Empty = True
                else:
                    betw1Empty = False
                    break
        if(not r2Moved):
            for y in range(5, 7): # spaces (5, 6) between king and right rook
                if(self.board[kx][y].pieceOccupy.toString is "0"):
                    betw1Empty = True
                else:
                    betw1Empty = False
                    break
        betwEmpty = betw1Empty or betw2Empty

        ### Waiting for check/mate boolean

        # check all requirements
        if (betwEmpty and not kingInCheck and not kingMoved and not rookMoved and not kingInCheck and not betwInCheck):
            return True
    
class enPassant(Rule):
    # Precondition for the attack square to be added
    #   first condition pawn need to be at a specific row that depend on the alliance
    #   second condition the opponent pawn move 2 square on their first move and endup right next to opponent pawn
    #
    # Postcondition for removing the attack square that was added
    #   when player did not take oppotunity

    def __init__(self, board, moveList, piece):
        super().__init__(board, moveList, piece)

    def checkPawn(self):
        dict = {"W": 3, "B": 4}
        incre = {"W": -1, "B": 1}
        alliance = self.piece.alliance
        append = self.moveList.append
        y = self.piece.y_coord
        if y > 0:
            pieceLeft = self.board[dict[alliance]][y-1].pieceOccupy
            attLeft = self.board[dict[alliance] + incre[alliance]][y-1].pieceOccupy
        if y < 7:
            pieceRight = self.board[dict[alliance]][y+1].pieceOccupy
            attRight = self.board[dict[alliance] + incre[alliance]][y+1].pieceOccupy
        
        if self.piece.x_coord == dict[alliance]:
            #look on the left side
            if y > 0 and pieceLeft.toString() == "P" and pieceLeft.alliance != alliance:
                if pieceLeft.passP is True and attLeft.toString() == "0":
                        append([dict[alliance] + incre[alliance], y-1])
            #look on the right side                
            if y < 7 and pieceRight.toString() == "P" and pieceRight.alliance != alliance:
                if pieceRight.passP is True and attRight.toString() == "0":
                    append([dict[alliance] + incre[alliance], y+1])
