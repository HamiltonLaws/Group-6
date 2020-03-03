from board.chessBoard import Board
from pieces.nullPiece import nullPiece
import pygame, os, sys, time

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
wPieces= []
bPieces= []

pieceMove = []
currentAlliance = "W"

chessBoard = Board()
chessBoard.createBoard()

flip = [False]

x_origin = None
y_origin = None

def switchSide():
    global flip
    flip[0] = not flip[0]
    drawBoard()
    drawPieces(flip[0])

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
drawPieces(flip[0])
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
                        x_origin = bRows
                        y_origin = bCols
                        print(selectedPiece, "at coordination: [", bRows, ", ", bCols, "]")
                        pieceMove = selectedPiece.validMove(chessBoard.board)
                        print("validMoves:", pieceMove)
                        drawBoard()
                        drawPieces(flip[0])
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
                        if chessBoard.board[bRows][bCols].pieceOccupy.toString() == "0":
                            selectedPiece.x_coord = bRows
                            selectedPiece.y_coord = bCols
                            chessBoard.updateBoard(bRows, bCols, selectedPiece)
                            chessBoard.updateBoard(x_origin, y_origin, nullPiece())
                            switchSide()
                            
                
        if event.type == pygame.MOUSEMOTION and not selectedPiece == None and pygame.mouse.get_pressed() == (1, 0, 0):
            #get UI coordinate
            cols, rows = pygame.mouse.get_pos()
            
        if event.type == pygame.MOUSEBUTTONUP and not selectedPiece == None and pygame.mouse.get_pressed() == (1, 0, 0):
            #get UI coordinate
            cols, rows = pygame.mouse.get_pos()
    
    pygame.display.update()
    clock.tick(60)