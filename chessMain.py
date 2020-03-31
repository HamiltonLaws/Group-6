from board.chessBoard import Board
from pieces.nullPiece import nullPiece
from rule.basicRule import Check
import pygame, os, sys, time, random

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
            return (0, 0, 0)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

class Title:
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
        self.rend = title_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 0, 0)
        else:
            return (0, 0, 0)
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
### Promoting part ###
menu_font = pygame.font.Font("C:\Windows\Fonts\Ebrima.ttf", 30)
options = [Option("QUEEN", (140, 50-7)), Option("BISHOP", (140, 100-7)),
           Option("ROOK", (140, 150-7)), Option("KNIGHT", (140, 200-7))]

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

        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
            pygame.display.update()
        clock.tick(15)
### End Promoting part ###

### Title part ###
title_font = pygame.font.Font(None, 120)
def ModeSelect():
    black, white = (0, 0, 0), (255, 255, 255)
    box_length = 240
    box_height = 35
    box1_x = 50
    box1_y = 415
    box2_x = 50
    box2_y = 465
    box3_x = 320
    box3_y = 415
    box4_x = 320
    box4_y = 465
    box5_x = 180
    box5_y = 515
    # background initial
    img = pygame.image.load("./art/background.png")
    img = pygame.transform.scale(img, (600, 600))
    screen.blit(img, (0, 0))
    Title("ChessA",(140,50))

    #selection box
    #pygame.draw.rect(screen, black, [125, 35, 145, 210])
    pygame.draw.rect(screen, black, [box1_x, box1_y, box_length, box_height])
    pygame.draw.rect(screen, white, [box1_x+1, box1_y+1, box_length-2, box_height-2])

    pygame.draw.rect(screen, black, [box2_x, box2_y, box_length, box_height])
    pygame.draw.rect(screen, white, [box2_x+1, box2_y+1, box_length-2, box_height-2])

    pygame.draw.rect(screen, black, [box3_x, box3_y, box_length, box_height])
    pygame.draw.rect(screen, white, [box3_x+1, box3_y+1, box_length-2, box_height-2])

    pygame.draw.rect(screen, black, [box4_x, box4_y, box_length, box_height])
    pygame.draw.rect(screen, white, [box4_x+1, box4_y+1, box_length-2, box_height-2])

    pygame.draw.rect(screen, black, [box5_x, box5_y, box_length, box_height])
    pygame.draw.rect(screen, white, [box5_x + 1, box5_y + 1, box_length - 2, box_height - 2])

    gameTypes = [Option("Vs. P2 (Flip)", (box1_x+40, box1_y-5)), Option("Vs. P2 (No Flip)", (box2_x+20, box2_y-5)),
                 Option("Vs. DumbBot", (box3_x+30, box3_y-5)), Option(" Vs. ComplexBot", ( box4_x+10,  box4_y-5)),
                 Option("Exit", ( box5_x+95,  box5_y-5))]
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get UI coordinate
                cols, rows = pygame.mouse.get_pos()
                #print(cols, rows)
                if box1_x < cols < box1_x+240 and box1_y < rows < box1_y+30:
                    return "P2F"
                if box2_x < cols < box2_x + 240 and box2_y < rows < box2_y + 30:
                    return "P2"
                if box3_x < cols < box3_x + 240 and box3_y < rows < box3_y + 30:
                    return "DB"
                if box4_x < cols < box4_x + 240 and box4_y < rows < box4_y + 30:
                    return "CB"
                if box5_x < cols < box5_x + 240 and box5_y < rows < box5_y + 30:
                    return "Quit"

        # gameDisplay.fill(white)

        for gameType in gameTypes:
            if gameType.rect.collidepoint(pygame.mouse.get_pos()):
                gameType.hovered = True
            else:
                gameType.hovered = False
            gameType.draw()
            pygame.display.update()
        #pygame.display.update()
        clock.tick(15)
### End Title part ###

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

mode = ModeSelect()
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
                                promoteTo = promoteCheck()
                                chessBoard.promote(selectedPiece.x_coord, selectedPiece.y_coord, "W", promoteTo)

                            if selectedPiece.alliance == "B" and selectedPiece.x_coord == 7:
                                promoteTo = promoteCheck()
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