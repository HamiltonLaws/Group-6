from board.chessBoard import Board
from board.titlePage import TitlePage
from pieces.nullPiece import nullPiece
from rule.basicRule import Check
import pygame, os, sys, time, random

pygame.init()

black, white = (222, 184, 135), (255, 255, 255)

ui_width, ui_height = 600, 600

selectedPiece = None

screen = pygame.display.set_mode((ui_width, ui_height))
screen = pygame.display.get_surface()

pygame.display.set_caption("ChessA")

clock = pygame.time.Clock()

allTiles = []
allPieces = []
currentPieces = []
kingMove = []
check = None
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

    if flip is False:   
        for rows in range(8):
            for cols in range(8):
                if not chessBoard.board[rows][cols].pieceOccupy.toString() == "0":
                    img = pygame.image.load("./art/" 
                            + chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper()
                            + chessBoard.board[rows][cols].pieceOccupy.toString().upper()
                            + ".png")
                    img = pygame.transform.scale(img, (width, height))
                    if chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper() == "W":
                        wPieces.append([y_coord, x_coord])
                    else:
                        bPieces.append([y_coord, x_coord])
                    allPieces.append([[y_coord, x_coord], img]) 
                x_coord += 75
            x_coord = 0
            y_coord += 75
    else:
        for rows in reversed(range(8)):
            for cols in reversed(range(8)):
                if not chessBoard.board[rows][cols].pieceOccupy.toString() == "0":
                    img = pygame.image.load("./art/" 
                            + chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper()
                            + chessBoard.board[rows][cols].pieceOccupy.toString().upper()
                            + ".png")
                    img = pygame.transform.scale(img, (width, height))
                    if chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper() == "W":
                        wPieces.append([y_coord, x_coord])
                    else:
                        bPieces.append([y_coord, x_coord])
                    allPieces.append([[y_coord, x_coord], img])
                x_coord += 75
            x_coord = 0
            y_coord += 75

    for img in allPieces:
        screen.blit(img[1], (img[0][1],img[0][0]))

def switchSide():
    global flip
    global selectedPiece
    global passPawn
    global check
    global checked
    global currentAlliance
    global mode
    if currentAlliance == "W":
        currentAlliance = "B"
    else:
        currentAlliance = "W"
    if mode == "P2F":
        flip = not flip
    drawBoard()
    #The check condition#
    check = Check(chessBoard.board,currentAlliance)
    checked = check.isCheck()#change#
    drawPieces(flip)
    #let the player know they are in check
    if(checked == True):
        #make a UI popup
        print(currentAlliance, " in in check")

    if passPawn is not None:
        passPawn.passP = False
        passPawn = None

    drawBoard()
    drawPieces(flip)
    if selectedPiece is not None and selectedPiece.toString() == "P" and selectedPiece.passP is True:
        passPawn = selectedPiece

title = TitlePage("ChessA")
mode = title.ModeSelect(screen,clock)
if mode == "Quit":
    exit()
if mode == "DB" or mode == "CB":
    Alliance = ["W", "B"]
    playerAlliance = random.choice(Alliance)
    
def randomMoves(pieces):
    global selectedPiece
    global pieceMove
    global chessBoard
    selectedPiece = None
    pieceMove = None
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
    x_origin = selectedPiece.x_coord
    y_origin = selectedPiece.y_coord
    x = chosenMove[0]
    y = chosenMove[1]
    if selectedPiece.toString() == "P":
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

gO = False

drawBoard()
drawPieces(flip)
currentPieces = wPieces

while not gO:

    if currentAlliance == "W":
        currentPieces = wPieces
    else:
        currentPieces = bPieces
    if mode == "DB" and currentAlliance != playerAlliance:
        randomMoves(currentPieces)
        switchSide()
        continue

    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            gO = True
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #get UI coordinate
            cols, rows = pygame.mouse.get_pos()

            for i in currentPieces:
                if i[0] < rows < i[0]+75 and i[1] < cols < i[1]+75:
                    bRows = (int)(i[0]/75)
                    bCols = (int)(i[1]/75)
                    if currentAlliance == "B" and mode == "P2F":
                        bRows = (int)((525-i[0])/75)
                        bCols = (int)((525-i[1])/75)
                    if chessBoard.board[bRows][bCols].pieceOccupy.alliance == currentAlliance:
                        #print(bRows, bCols)
                        pieceMove.clear()
                        selectedPiece = chessBoard.board[bRows][bCols].pieceOccupy
                        x_origin = bRows
                        y_origin = bCols
                        print(selectedPiece, "at coordination: [", bRows, ", ", bCols, "]")
                        #update king moves if in check HAMILTON
                        #Make it so has to move king
                        #if clicked off king pieceMove is null?
                        if(selectedPiece.toString() == "K" and checked == True):
                            check.isCheck()
                            pieceMove = check.isCheckMate()
                        else:
                            pieceMove = selectedPiece.validMove(chessBoard.board)
                        print("validMoves:", pieceMove)
                        drawBoard()
                        drawPieces(flip)
                        for j in pieceMove:
                            j[0] = j[0]*75
                            j[1] = j[1]*75
                            if currentAlliance == "B" and mode == "P2F":
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

                        selectedPiece.x_coord = bRows
                        selectedPiece.y_coord = bCols
                        selectedPiece.fMove = False
                        chessBoard.updateBoard(bRows, bCols, selectedPiece)
                        chessBoard.updateBoard(x_origin, y_origin, nullPiece())
                        # promoting check
                        if selectedPiece.toString() == "P":
                            if selectedPiece.alliance == "W" and selectedPiece.x_coord == 0:
                                promoteTo = check.promoteCheck(screen,clock)
                                chessBoard.promote(selectedPiece.x_coord, selectedPiece.y_coord, "W", promoteTo)

                            if selectedPiece.alliance == "B" and selectedPiece.x_coord == 7:
                                promoteTo = check.promoteCheck(screen,clock)
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