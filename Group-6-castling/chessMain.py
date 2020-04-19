from board.chessBoard import Board
from pieces.nullPiece import nullPiece
from rule.basicRule import Check
from rule.basicRule import Castling
import pygame, os, sys, time

class Option:
    hovered = False

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 0, 0)
        else:
            return (100, 100, 100)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

pygame.init()

black, white = (222, 184, 135), (255, 255, 255)

ui_width, ui_height = 600, 600

selectedPiece = None

screen = pygame.display.set_mode((ui_width, ui_height))
screen = pygame.display.get_surface()
#screen.blit(pygame.transform.flip(screen, False, True), dest=(0, 0))

pygame.display.set_caption("ChessA")

clock = pygame.time.Clock()

allTiles = []
allPieces = []
currentPieces = []
kingMove = []
checked = False
wPieces= []
bPieces= []

pieceMove = []
currentAlliance = "W"

chessBoard = Board()
chessBoard.createBoard()

flip = False

x_origin = None
y_origin = None
passPawn = None
### Promoting part ###
menu_font = pygame.font.Font(None, 40)
options = [Option("QUEEN", (140, 50)), Option("BISHOP", (140, 100)),
           Option("ROOK", (140, 150)), Option("KNIGHT", (140, 200))]

def promoteCheck():
    black, white = (0, 0, 0), (255, 255, 255)
    pygame.draw.rect(screen, black, [125, 35, 145, 210])
    pygame.draw.rect(screen, white, [135, 45, 125, 190])
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get UI coordinate
                cols, rows = pygame.mouse.get_pos()
                #print(cols, rows)
                if 140 < cols <250:
                    if 50 < rows < 80:
                        return "Q"
                    if 100 < rows < 130:
                        return "B"
                    if 150 < rows < 180:
                        return "R"
                    if 200 < rows < 230:
                        return "N"
        # gameDisplay.fill(white)

        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
            pygame.display.update()
        #pygame.display.update()
        clock.tick(15)
### End Promoting part ###

def switchSide():
    global flip
    global selectedPiece
    global passPawn
    flip = not flip
    drawBoard()
    #The check condition#
    checked = Check(chessBoard.board,currentAlliance).isCheck()
    drawPieces(flip)
    #let the player know they are in check
    if(checked == True):
        print(currentAlliance, " in in check")
    drawPieces(flip)
    if passPawn is not None:
        passPawn.passP = False
        passPawn = None

    drawBoard()
    drawPieces(flip)
    if selectedPiece.toString() == "P" and selectedPiece.passP is True:
        passPawn = selectedPiece

def square(x_coord, y_coord, width, height, color):
    pygame.draw.rect(screen, color, [x_coord, y_coord, width, height])
    allTiles.append([color, [x_coord, y_coord, width, height]])

def drawBoard():
    x_coord = 0
    y_coord = 0
    color = 0
    width = 75
    height = 75

    for _ in range(8):
        for _ in range(8):
            if color % 2 == 0:
                square(x_coord, y_coord, width, height, white)
                x_coord += 75
            else:
                square(x_coord, y_coord, width, height, black)
                x_coord += 75
            color += 1
        color += 1
        x_coord = 0
        y_coord += 75


def castleRook(prevY, newY, selectedPiece):       
    print("move rook")
    print("toString after call", selectedPiece.toString())
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
                chessBoard.updateBoard(0, 7, nullPiece())
            elif (newY == prevY - 2): # black left
                chessBoard.updateBoard(0, 3, chessBoard.board[0][0].pieceOccupy)
                chessBoard.updateBoard(0, 0, nullPiece())
        else:
            if (newY == prevY + 2): # white right
                chessBoard.updateBoard(7, 5, chessBoard.board[7][7].pieceOccupy)
                chessBoard.updateBoard(7, 7, nullPiece())
            elif (newY == prevY - 2): # white left
                chessBoard.updateBoard(7, 3, chessBoard.board[7][0].pieceOccupy)
                chessBoard.updateBoard(7, 0, nullPiece())



def drawPieces(flip):
    global currentAlliance
    global allPieces
    global wPieces
    global bPieces
    allPieces.clear()
    wPieces.clear()
    bPieces.clear()
    x_coord = 0
    y_coord = 0
    width = 75
    height = 75
    global currentAlliance

    if flip is False:
        currentAlliance = "W"
        for rows in range(8):
            for cols in range(8):
                if not chessBoard.board[rows][cols].pieceOccupy.toString() == "0":
                    img = pygame.image.load("./art/" 
                            + chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper()
                            + chessBoard.board[rows][cols].pieceOccupy.toString().upper()
                            + ".png")
                    img = pygame.transform.scale(img, (width, height))
                    if(chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper() == "W"):
                        wPieces.append([y_coord, x_coord])
                    else:
                        bPieces.append([y_coord, x_coord])
                    allPieces.append([[y_coord, x_coord], img]) 
                x_coord += 75
            x_coord = 0
            y_coord += 75
    else:
        currentAlliance = "B"
        for rows in reversed(range(8)):
            for cols in reversed(range(8)):
                if not chessBoard.board[rows][cols].pieceOccupy.toString() == "0":
                    img = pygame.image.load("./art/" 
                            + chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper()
                            + chessBoard.board[rows][cols].pieceOccupy.toString().upper()
                            + ".png")
                    img = pygame.transform.scale(img, (width, height))
                    if(chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper() == "W"):
                        wPieces.append([y_coord, x_coord])
                    else:
                        bPieces.append([y_coord, x_coord])
                    allPieces.append([[y_coord, x_coord], img])
                x_coord += 75
            x_coord = 0
            y_coord += 75

    for img in allPieces:
        screen.blit(img[1], (img[0][1],img[0][0]))

gO = False

drawBoard()
drawPieces(flip)
currentPieces = wPieces

while not gO:

    if currentAlliance == "W":
        currentPieces = wPieces
    else:
        currentPieces = bPieces

    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            gO = True
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #get UI coordinate
            cols, rows = pygame.mouse.get_pos()

            whiteKing = chessBoard.board[7][4].pieceOccupy
            ci = Castling(chessBoard, whiteKing.validMove, whiteKing)
            print(ci.canCastle())

            

            for i in currentPieces:
                if i[0] < rows < i[0]+75 and i[1] < cols < i[1]+75:
                    bRows = (int)(i[0]/75)
                    bCols = (int)(i[1]/75)
                    if currentAlliance == "B":
                        bRows = (int)((525-i[0])/75)
                        bCols = (int)((525-i[1])/75)
                    if chessBoard.board[bRows][bCols].pieceOccupy.alliance == currentAlliance:
                        #print(bRows, bCols)
                        pieceMove.clear()
                        selectedPiece = chessBoard.board[bRows][bCols].pieceOccupy

                        ck = Castling(chessBoard, selectedPiece.validMove, selectedPiece)

                        # if(ck.canCastle()):
                        #     if (selectedPiece.alliance == "B"):
                        #         pieceMove.append([0, 6])
                        #         pieceMove.append([0, 2])
                        #     else:
                        #         print(pieceMove)
                        #         pieceMove.append([7, 6])
                        #         pieceMove.append([7, 2])
                        
                        x_origin = bRows
                        y_origin = bCols
                        print(selectedPiece, "at coordination: [", bRows, ", ", bCols, "]")
                        pieceMove = selectedPiece.validMove(chessBoard.board)
                        if(ck.canCastle() and selectedPiece.toString() == "K"):
                            if (selectedPiece.alliance == "B"):
                                    pieceMove.append([0, 6])
                                    pieceMove.append([0, 2])
                            else:
                                    pieceMove.append([7, 6])
                                    pieceMove.append([7, 2])

                        drawBoard()
                        drawPieces(flip)
                        for j in pieceMove:
                            j[0] = j[0]*75
                            j[1] = j[1]*75
                            if(currentAlliance == "B"):
                                j[0] = 525 - j[0]
                                j[1] = 525 - j[1]
                            img = pygame.image.load("./art/green_circle_neg.png")
                            img = pygame.transform.scale(img, (75, 75))
                            screen.blit(img, (j[1], j[0]))
                            currentPieces.extend([[j[0], j[1]]])
                        #print(currentPieces)
                        break
                    elif selectedPiece != None:
                        if selectedPiece.toString() == "P":

                            if selectedPiece.x_coord +2 == bRows or selectedPiece.x_coord -2 == bRows:
                                selectedPiece.passP = True

                            if selectedPiece.alliance == "B" and bCols != y_origin:
                                if chessBoard.board[bRows-1][bCols].pieceOccupy.toString() == "P":
                                    if chessBoard.board[bRows-1][bCols].pieceOccupy.passP == True:
                                        chessBoard.updateBoard(bRows-1, bCols, nullPiece())

                            if selectedPiece.alliance == "W" and bCols != y_origin:
                                if chessBoard.board[bRows+1][bCols].pieceOccupy.toString() == "P":
                                    if chessBoard.board[bRows+1][bCols].pieceOccupy.passP == True:
                                        chessBoard.updateBoard(bRows+1, bCols, nullPiece())



                        chessBoard.updateBoard(bRows, bCols, selectedPiece)
                        chessBoard.updateBoard(x_origin, y_origin, nullPiece())
                        print("selPiece x, y coord before: ", selectedPiece.x_coord, selectedPiece.y_coord)
                        prevKY = selectedPiece.y_coord
                        selectedPiece.x_coord = bRows
                        selectedPiece.y_coord = bCols
                        print("selPiece x, y coord after: ", selectedPiece.x_coord, selectedPiece.y_coord)
                        newKY = selectedPiece.y_coord
                        print("selectedPiece.toString before castleRook call", selectedPiece.toString())
                        castleRook(prevKY, newKY, selectedPiece)
                        selectedPiece.fMove = False
                        # promoting check
                        if selectedPiece.toString() == "P":
                            if selectedPiece.alliance == "W" and selectedPiece.x_coord == 0:
                                promoteTo = promoteCheck()
                                chessBoard.updateBoard(selectedPiece.x_coord, selectedPiece.y_coord, nullPiece())
                                chessBoard.promote(selectedPiece.x_coord, selectedPiece.y_coord, "W", promoteTo)

                            if selectedPiece.alliance == "B" and selectedPiece.x_coord == 7:
                                promoteTo = promoteCheck()
                                chessBoard.updateBoard(selectedPiece.x_coord, selectedPiece.y_coord, nullPiece())
                                chessBoard.promote(selectedPiece.x_coord, selectedPiece.y_coord, "B", promoteTo)

                        switchSide()
                            
                
        if event.type == pygame.MOUSEMOTION and not selectedPiece == None and pygame.mouse.get_pressed() == (1, 0, 0):
            #get UI coordinate
            cols, rows = pygame.mouse.get_pos()
            
        if event.type == pygame.MOUSEBUTTONUP and not selectedPiece == None and pygame.mouse.get_pressed() == (1, 0, 0):
            #get UI coordinate
            cols, rows = pygame.mouse.get_pos()
    
    pygame.display.update()
    clock.tick(60)