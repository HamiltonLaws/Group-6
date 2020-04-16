from board.chessBoard import Board
from titlePage import TitlePage
from pieces.nullPiece import nullPiece
from rule.basicRule import Check
from rule.basicRule import staleMate
from Bot import dumbBot
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
Pieces = []
kingMove = []
check = None
checked = False
staleCheck = False
moves = {"W": 0, "B": 0}
wPieces= []
bPieces= []
playerAlliance = None
stalemate = None
protector = None
count = 0

pieceMove = []
currentAlliance = "W"

chessBoard = Board()
chessBoard.createBoard()

flip = False

x_origin = None
y_origin = None
passPawn = None

title = TitlePage("ChessA")
mode = title.ModeSelect(screen,clock)

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
    global Pieces
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
                    elif chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper() == "B":
                        bPieces.append([y_coord, x_coord])
                    allPieces.append([[y_coord, x_coord], img])
                    Pieces.append((y_coord, x_coord))
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
                    elif chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper() == "B":
                        bPieces.append([y_coord, x_coord])
                    allPieces.append([[y_coord, x_coord], img])
                    Pieces.append([y_coord, x_coord])
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
    global moves
    global count
    global gO
    if moves[currentAlliance] == 50:
        print("50 Shade of Stale")
        gO = True
    #The check condition#
    check = Check(chessBoard.board,currentAlliance)
    checked = check.isCheck()#change#
    
    if currentAlliance == "W":
        currentAlliance = "B"
    else:
        currentAlliance = "W"
    if mode == "P2F":
        flip = not flip

    #let the player know they are in check
    if(checked == True):
        #make a UI popup
        print(currentAlliance, " in in check")

    if passPawn is not None:
        passPawn.passP = False
        passPawn = None

    drawBoard()
    drawPieces(flip)
    if selectedPiece.toString() == "P" and selectedPiece.passP is True:
        passPawn = selectedPiece
    if count == 4:
        if stalemate.repetitionCheck():
            gO = True
        count = 0

def startGame(mode):
    global playerAlliance
    global stalemate
    global currentPieces
    if mode == "Quit":
        exit()
    elif mode == "DB" or mode == "CB":
        Alliance = ["W", "B"]
        playerAlliance = random.choice(Alliance)
        drawBoard()
        drawPieces(False)
        currentPieces = wPieces
        stalemate = staleMate(chessBoard.board, wPieces, bPieces, Pieces)
    else:
        drawBoard()
        drawPieces(False)
        currentPieces = wPieces
        stalemate = staleMate(chessBoard.board, wPieces, bPieces, Pieces)

gO = False
startGame(mode)

while not gO:

    if currentAlliance == "W":
        currentPieces = wPieces
    else:
        currentPieces = bPieces
    if mode == "DB" and currentAlliance != playerAlliance:
        selectedPiece, move = dumbBot(chessBoard, currentPieces).randomMoves()
        if move != 0:
            moves[currentAlliance] += move
        else:
            moves[currentAlliance] = 0
        print(moves)
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
                        #Checks for conditons need to an UI
                        if(checked == True):
                            protector = check.toProtect()
                            if(protector == True):
                                print("Must move a pice to protect the king or move the king to another positon")
                                if(selectedPiece.toString()=='K'):
                                    pieceMove = check.isCheckMate()
                                else:
                                    pieceMove = selectedPiece.validMove(chessBoard.board) 
                            else:
                                print("King must be moved")
                                if(selectedPiece.toString() != 'K'):
                                    pieceMove = []
                                else:
                                    pieceMove = check.isCheckMate()
                                    if(pieceMove == []):
                                        print(currentAlliance, " Is in checkMate") 
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
                        if chessBoard.board[bRows][bCols].pieceOccupy.toString() != "0":
                            moves[currentAlliance] = 0
                        else:
                            moves[currentAlliance] += 1
                        if selectedPiece.toString() == "P":
                            moves[currentAlliance] = 0
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
                        if selectedPiece.fMove:
                            selectedPiece.fMove = False
                        chessBoard.updateBoard(bRows, bCols, selectedPiece)
                        chessBoard.updateBoard(x_origin, y_origin, nullPiece())
                        count += 1
                        print(moves)
                        # promoting check
                        if selectedPiece.toString() == "P":
                            if selectedPiece.alliance == "W" and selectedPiece.x_coord == 0:
                                promoteTo = check.promoteCheck(screen,clock)
                                chessBoard.promote(selectedPiece.x_coord, selectedPiece.y_coord, "W", promoteTo)

                            if selectedPiece.alliance == "B" and selectedPiece.x_coord == 7:
                                promoteTo = check.promoteCheck(screen,clock)
                                chessBoard.promote(selectedPiece.x_coord, selectedPiece.y_coord, "B", promoteTo)

                        switchSide()

        pygame.display.update()
        clock.tick(60)
