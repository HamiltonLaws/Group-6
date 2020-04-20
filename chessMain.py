from board.chessBoard import Board
from titlePage import TitlePage
from pieces.nullPiece import nullPiece
from rule.basicRule import Check
from rule.basicRule import staleMate
from rule.basicRule import Castling
from Bot import dumbBot
import pygame, os, sys, time, random

pygame.init()

black, white = (0, 0, 0), (255, 255, 255)

ui_width, ui_height = 600, 600

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
selectedPiece = None
checked = False
staleCheck = False
moves = {"W": 0, "B": 0}
wPieces= []
bPieces= []
playerAlliance = None
stalemate = None
protector = None
count = 0
yText = 10

pieceMove = []
currentAlliance = "W"

chessBoard = Board()
chessBoard.createBoard()

flip = False

x_origin = None
y_origin = None
passPawn = None

def display_message(msg):
    global yText
    font = pygame.font.Font("C:\Windows\Fonts\Ebrima.ttf", 14) 
    text = font.render(msg, True, (255, 255, 255)) 
    textRect = text.get_rect()  
    textRect.center = (800, yText) 
    yText += 16
    screen.blit(text, textRect)
    a = True
    while a:
        for event in pygame.event.get(): 
            if event.type == pygame.MOUSEBUTTONDOWN : 
                a = False
        pygame.display.update()  
      

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
                        wPieces.append((y_coord, x_coord))
                    elif chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper() == "B":
                        bPieces.append((y_coord, x_coord))
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
                        wPieces.append((y_coord, x_coord))
                    elif chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper() == "B":
                        bPieces.append((y_coord, x_coord))
                    allPieces.append([[y_coord, x_coord], img])
                    Pieces.append((y_coord, x_coord))
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
        display_message("50 Shade of Stale")
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
        if(currentAlliance == "W"):
            display_message("White is in Check")
        else:
            display_message("Black is in Check")

    if passPawn is not None:
        passPawn.passP = False
        passPawn = None

    drawBoard()
    drawPieces(flip)
    stalemate.alliance = currentAlliance
    if stalemate.staleCase2():
        display_message("Stalemate")
        gO = True
    if selectedPiece.toString() == "P" and selectedPiece.passP is True:
        passPawn = selectedPiece
    if count == 4:
        if stalemate.repetitionCheck():
            display_message("Stalemate")
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

def main():
    global gO
    global currentAlliance
    global currentPieces
    global wPieces
    global bPieces
    global checked
    global mode
    global selectedPiece
    global pieceMove
    global count
    global moves
    
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
            if selectedPiece is None:
                gO = True
                display_message("Game Over, Bot lose")
                break
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
                if cols > 600 or rows > 600:
                    pass

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

                            ck = Castling(chessBoard, selectedPiece.validMove, selectedPiece)

                            if ck.canCastle() and selectedPiece.toString == "K":
                                if (selectedPiece.alliance == "B"):
                                    pieceMove.append([0, 6])
                                    pieceMove.append([0, 2])
                                else:
                                    print(pieceMove)
                                    pieceMove.append([7, 6])
                                    pieceMove.append([7, 2])
                            
                            if(checked == True):
                                kingMove = check.isCheckMate()
                                protector = check.toProtect()
                                if(protector == True):
                                    display_message("Must move a pice to protect the king or move king")
                                    if(selectedPiece.toString()=='K'):
                                        pieceMove = check.isCheckMate()
                                    else:
                                        pieceMove = selectedPiece.validMove(chessBoard.board) 
                                else:
                                    if(kingMove == []):
                                        if(currentAlliance == "W"):
                                            display_message("White Is in checkMate, Black Wins")
                                            time.sleep(2)
                                            gO = True 
                                        else:
                                            display_message("Black Is in checkMate, White Wins")
                                            time.sleep(2)
                                            gO = True 
                                    if(selectedPiece.toString() != 'K'):
                                        display_message("King must be moved")
                                        pieceMove = []
                                    else:
                                        pieceMove = check.isCheckMate()
                            else:
                                pieceMove = selectedPiece.validMove(chessBoard.board)
                                if(ck.canCastle() and selectedPiece.toString() == "K"):
                                    if (selectedPiece.alliance == "B"):
                                        pieceMove.append([0, 6])
                                        pieceMove.append([0, 2])
                                    else:
                                        pieceMove.append([7, 6])
                                        pieceMove.append([7, 2])
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
                            
                            prevKY = selectedPiece.y_coord
                            selectedPiece.x_coord = bRows
                            selectedPiece.y_coord = bCols
                            newKY = selectedPiece.y_coord
                            castleRook(prevKY, newKY, selectedPiece)
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

while 1:
    ui_width, ui_height = 600, 600
    screen = pygame.display.set_mode((ui_width, ui_height))
    flip = False
    passPawn = None
    check = None
    selectedPiece = None
    count = 0
    moves = {"W": 0, "B": 0}
    chessBoard = Board()
    chessBoard.createBoard()
    currentAlliance = "W"
    title = TitlePage("ChessA")
    mode = title.ModeSelect(screen,clock)
    ui_width, ui_height = 1000, 600
    screen = pygame.display.set_mode((ui_width, ui_height))
    startGame(mode)
    gO = False
    main()