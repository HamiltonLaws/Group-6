import pygame
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
   
class checkPieces(Rule):
    def __init__(self, board, moveList, piece):
        super().__init__(board, moveList, piece)

    def Check(self):
        self.removeList.clear()
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
    playerPiece = []
    opponentPiece = []
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
        self.opponentPiece.clear()
        self.playerPiece.clear()
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
                curent = self.board[rows][cols].pieceOccupy
                curentMove = curent.validMove(self.board)
                if(curent.toString() != "0" and curent.toString() != "K" and curent.alliance == self.alliance):
                    #self.playerPiece.extend((curent.toString(),[curent.x_coord,curent.y_coord]))
                    self.playerPieceMoves.extend(curentMove)
                elif(curent.toString() != "0" and curent.toString() != "K" and curent.alliance != self.alliance):
                    self.opponentPieceMoves.extend(curentMove)
                    #self.opponentPiece.extend((curent.toString(),[curent.x_coord,curent.y_coord]))
                elif(curent.toString() == "K" and curent.alliance != self.alliance):
                    self.opponentKingMoves.extend(curentMove)
                    self.opponentKingPlace = [curent.x_coord,curent.y_coord]
                elif(curent.toString() == "K" and curent.alliance == self.alliance):
                    self.playerKingMoves.extend(curentMove)
                    self.playerKingPlace = [curent.x_coord,curent.y_coord]
        #check the other king is in check  
        #print("Player pieces", self.playerPiece)          
        if self.opponentKingPlace in self.playerPieceMoves:
            self.message = True
        return self.message
        
    #Checks to see if King can move where they will not be in Check DONE
    def isCheckMate(self):
        kingMoveRemove = []
        kingMoveReturn = self.opponentKingMoves 
       #print("Player piece move", self.playerPieceMoves)    
        for i in range(len(kingMoveReturn)):
            if kingMoveReturn[i] in self.playerPieceMoves:
                kingMoveRemove.extend([kingMoveReturn[i]])
        #Checks to see if king can move to aother spot and not be in check
        if len(kingMoveReturn) == len(kingMoveRemove):
            kingMoveReturn = []
        else:
            for i in range(len(kingMoveReturn)):   
                if kingMoveReturn[i] in kingMoveRemove:
                    kingMoveRemove.append([kingMoveReturn[i]])
        kingMoveReturn = [i for i in kingMoveReturn if i not in kingMoveRemove]
        return kingMoveReturn

    #to see if you can move a piece to protect king from check DONE
    def toProtect(self):
        for i in range(len(self.opponentKingMoves)):
            if self.opponentKingMoves[i] in self.opponentPieceMoves:
                return True
            else:
                return False 



    #To see if your a piece is protecting you from check IPROGRESS
    #def isProtecting(self):
        #return True

### Promoting part ###
    def promoteCheck(self,screen,clock):
        options = [Option("QUEEN", (140, 50 - 7), screen), Option("BISHOP", (140, 100 - 7), screen),
                   Option("ROOK", (140, 150 - 7), screen), Option("KNIGHT", (140, 200 - 7), screen)]
        black, white = (0, 0, 0), (255, 255, 255)
        pygame.draw.rect(screen, black, [130, 40, 135, 200])
        #pygame.draw.rect(screen, white, [135, 45, 125, 190])
        pygame.draw.rect(screen, white, [135, 45, 125, 42])
        pygame.draw.rect(screen, white, [135, 95, 125, 42])
        pygame.draw.rect(screen, white, [135, 145, 125, 42])
        pygame.draw.rect(screen, white, [135, 195, 125, 40])
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # get UI coordinate
                    cols, rows = pygame.mouse.get_pos()
                    # print(cols, rows)
                    if 140 < cols < 250:
                        if 50 < rows < 80:
                            return "Q"
                        if 100 < rows < 130:
                            return "B"
                        if 150 < rows < 180:
                            return "R"
                        if 200 < rows < 230:
                            return "N"

            for option in options:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw(screen)
                pygame.display.update()
            clock.tick(15)

class Option:
    hovered = False
    def __init__(self, text, pos,screen):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw(screen)

    def draw(self,screen):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        menu_font = pygame.font.Font("C:\Windows\Fonts\Ebrima.ttf", 30)
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 0, 0)
        else:
            return (0, 0, 0)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
### End Promoting part ###


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

class staleMate(Rule):
    pieces = []
    pastBoard = []
    repetition = 0
    opPieces = []
    allPieces = []
    def __init__(self, board, wPieces, bPieces, allPieces):
        self.board = board
        self.pieces = wPieces
        self.opPieces = bPieces
        self.allPieces = allPieces
        self.updatePast()
    
    def updatePast(self):
        self.pastBoard.clear()
        for i in self.allPieces:
            self.pastBoard.append(i)
    
    def repetitionCheck(self):
        if set(self.pastBoard) & set(self.allPieces):
            self.repetition += 1
            print("Repetition", self.repetition)
            if self.repetition == 3:
                print("Desperate Stale")
                return True
        else:
            print("repetition False")
            self.repetition = 0
            self.updatePast()
            return self.staleCase1()
    
    def staleCase1(self):
        K1 = False
        K2 = False
        QP = False
        N = False
        bishop1Color = None
        bishop2Color = None
        if len(self.pieces) == 1 and len(self.opPieces) == 1:
            rows = (int)(self.pieces[0][0]/75)
            cols = (int)(self.pieces[1][1]/75)
            if self.board[rows][cols].pieceOccupy.toString() == "K":
                rows = (int)(self.pieces[0][0]/75)
                cols = (int)(self.pieces[1][1]/75)
                if self.board[rows][cols].pieceOccupy.toString() == "K":
                    print("Two King Dance Stale")
                    return True

        elif len(self.pieces) < 3 and len(self.opPieces) < 3:
            for i in self.pieces:
                rows = (int)(i[0]/75)
                cols = (int)(i[1]/75)
                if self.board[rows][cols].pieceOccupy.toString() == "K":
                    K1 = True
                elif self.board[rows][cols].pieceOccupy.toString() == "N":
                    N = True
                elif self.board[rows][cols].pieceOccupy.toString() == "B":
                    if (rows+cols)%2 == 0:
                        bishop1Color = "W"
                    else: 
                        bishop1Color = "B"
                else:
                    QP = True
                    break

            if K1 and (not QP or bishop1Color is None or not N):
                for j in self.opPieces:
                    rows = (int)(j[0]/75)
                    cols = (int)(j[1]/75)
                    if self.board[rows][cols].pieceOccupy.toString() == "K":
                        K1 = True
                    elif self.board[rows][cols].pieceOccupy.toString() == "N":
                        N = True
                    elif self.board[rows][cols].pieceOccupy.toString() == "B":
                        if (rows+cols)%2 == 0:
                            bishop2Color = "W"
                        else: 
                            bishop2Color = "B"
                    else:
                        QP = True
                        break
        
        if K1 and K2 and QP:
            print("Stale by case")
            return True
        elif K1 and K2 and (bishop1Color is not None or bishop2Color is not None or N):
            if bishop1Color is not None and bishop2Color is not None and bishop1Color == bishop2Color:
                print("Stale by case: same bishop")
                return True
            elif bishop1Color is None and bishop2Color is None and N:
                print("Stale by case: 1v2")
                return True
            elif (bishop1Color is None or bishop2Color is None) and not N:
                print("Stale by case: 1v2")
                return True
        else:
            return self.staleCase2()

    def staleCase2(self):
        count = 0
        for i in self.pieces:
            rows = (int)(i[0]/75)
            cols = (int)(i[1]/75)
            if not self.board[rows][cols].pieceOccupy.validMove:
                count += 1
            elif count == len(self.pieces):
                return True
            else:
                return False