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

    #Returns a Boolean if opponent will be in Chekc DONE
    def isCheck(self):
        super().Clear()
        curent = None
        curentMove = None
        # pieceMoves retuns a list of all the posible moves from the current player, kingPlace returns the placment of the oppoite king
        for rows in range(8):
            for cols in range(8):
                curent = self.board[rows][cols].pieceOccupy #add validMove here
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
        print("King Move Return", self.opponentKingMoves)          
        for i in range(len(self.playerPieceMoves)):
            for j in range(len(self.playerPieceMoves[i])):
                if(self.opponentKingPlace == self.playerPieceMoves[i][j]):
                    self.message = True
        return self.message
        
    #Checks to see if King can move where they will not be in Check DONE
    def isCheckMate(self):
        kingMove =  self.opponentKingMoves  
        kingMoveRemove = []
        kingMoveReturn = self.opponentKingMoves
        print("King Move Return", kingMoveReturn) 
        print("Player piece move", self.playerPieceMoves)    
        for i in range(len(self.playerPieceMoves)):
            for j in range(len(self.playerPieceMoves[i])):
                for k in range(len(kingMove)):
                    for x in range(len(kingMove[k])):
                        if(kingMove[k][x]== self.playerPieceMoves[i][j]):
                            kingMoveRemove.append([kingMove[k][x]])
        #Checks to see if king can move to aother spot and not be in check
        print("King move remove", kingMoveRemove)
        if(kingMove == kingMoveRemove):
            kingMoveReturn = []
        else:
            for i in range(len(kingMove)):   
                for j in range(len(kingMoveRemove)):
                    for k in range(len(kingMoveRemove)):
                        for x in range(len(kingMoveRemove[k])):
                            if(kingMove[i][j] == kingMoveRemove[k][x]):
                                kingMoveReturn[i].remove(kingMove[i][j])
                                #kingMoveRemove.append(kingMove[i][j])
        print("King Move Return", kingMoveReturn)
        return kingMoveReturn

    #to see if you can move a piece to protect king from check INPROGRESS
    def toProtect(self):
        kingMove = []
        kingMove =  self.opponentKingMoves  
        kingMoveRemove = []
        print("The king can innicaly move here: ",self.opponentKingMoves)     
        if(self.message == True):
            for i in range(len(self.playerPieceMoves)):
                for j in range(len(self.playerPieceMoves[i])):
                    for k in range(len(kingMove)):
                        if(kingMove[k]== self.playerPieceMoves[i][j]):
                            kingMoveRemove.append(kingMove[k])
            #check to see if anoter piece can protect the king
            print("King Remove List ", kingMoveRemove)
            for i in range(len(self.opponentPieceMoves)):
                for j in range(len(self.opponentPieceMoves[i])):
                    for k in range(len(kingMoveRemove)):
                        if(kingMoveRemove[k] == self.opponentPieceMoves[i][j]):
                            print("this is king move",kingMove[k], "this is opponent move ", self.opponentPieceMoves[i][j])
                            kingMove.remove(kingMoveRemove[k]) 
        return kingMove

    #To see if your a piece is protecting you from check IPROGRESS
    def isProtecting(self):
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

