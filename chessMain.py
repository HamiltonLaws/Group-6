from board.chessBoard import Board
import pygame, os, sys

pygame.init()

black, white = (222, 184, 135), (255, 255, 255)

ui_width, ui_height = 600, 600

selectedPiece = None

screen = pygame.display.set_mode((ui_width, ui_height))

pygame.display.set_caption("ChessA")

clock = pygame.time.Clock()

allTiles = []
allPieces = []

chessBoard = Board()
chessBoard.createBoard()

def square(x_coord, y_coord, width, height, color):
    pygame.draw.rect(screen, color, [x_coord, y_coord, width, height])
    allTiles.append([color, [x_coord, y_coord, width, height]])

def drawPieces():
    x_coord = 0
    y_coord = 0
    color = 0
    width = 75
    height = 75
    number = 0

    for rows in range(8):
        for cols in range(8):
            #print(rows, cols)
            if color % 2 == 0:
                square(x_coord, y_coord, width, height, white)
                if not chessBoard.board[rows][cols].pieceOccupy.toString() == "0":
                    img = pygame.image.load("./art/" 
                        + chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper()
                        + chessBoard.board[rows][cols].pieceOccupy.toString().upper()
                        + ".png")
                    img = pygame.transform.scale(img,(75, 75))
                    allPieces.append([img, [x_coord, y_coord]])
                x_coord += 75
            else:
                square(x_coord, y_coord, width, height, black)
                if not chessBoard.board[rows][cols].pieceOccupy.toString() == "0":
                    img = pygame.image.load("./art/" 
                        + chessBoard.board[rows][cols].pieceOccupy.alliance[0].upper()
                        + chessBoard.board[rows][cols].pieceOccupy.toString().upper()
                        + ".png")
                    img = pygame.transform.scale(img, (75, 75))
                    allPieces.append([img, [x_coord, y_coord]])
                x_coord += 75
            color += 1
            number += 1
        color += 1
        x_coord = 0
        y_coord += 75

gO = False

drawPieces()

print(allPieces)
chessBoard.printBoard()

for img in allPieces:
    screen.blit(img[0], img[1])

while not gO:
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            gO = True
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and selectedPiece == None:
            #get UI coordinate
            x, y = pygame.mouse.get_pos()
                
            if event.type == pygame.MOUSEMOTION and not selectedPiece == None:
                #get UI coordinate
                x, y = pygame.mouse.get_pos()
                    
        elif event.type == pygame.MOUSEBUTTONUP and not selectedPiece == None:
            #get UI coordinate
            x, y = pygame.mouse.get_pos()
            

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
