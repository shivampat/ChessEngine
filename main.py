import pygame, sys, os
from pygame.locals import *
from board import Board

### Initialize Pygame
pygame.init()

### Pygame settings and constants
# Screen settings
FPS = 30
FramePerSec = pygame.time.Clock()

# Screen sizing 
GRID_SIZE = 100 
SCREEN_WIDTH = GRID_SIZE * 8 
SCREEN_HEIGHT = GRID_SIZE * 8 

# Screen constants
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill((255, 255, 255))
pygame.display.set_caption("Chess")

### Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SQUARE1 = (235, 236, 208)
SQUARE2 = (115, 149, 82)
HIGHLIGHT = (0, 0, 255)
CHECK_COLOR = (255, 0, 0)

### Load images
def loadImages():
    piecePics = {}
    # load white pieces
    for filename in os.listdir('pieces/white'):
        if filename.endswith('.png'):
            image = pygame.image.load('pieces/white/' + filename)
            image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
            piecePics[filename[:-4].upper()] = image
    for filename in os.listdir('pieces/black'):
        if filename.endswith('.png'):
            image = pygame.image.load('pieces/black/' + filename)
            image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
            piecePics[filename[:-4].lower()] = image
    return piecePics

def pixelsToChessCoords(x, y):
    rowNum = 8 - (y // GRID_SIZE)
    colLetter = list(BOARD.getBoardLayout().keys())[x // GRID_SIZE] 
    return colLetter + str(rowNum)

def chessToPixelsCoords(chessCoords):
    colLetter = chessCoords[0]
    rowNum = int(chessCoords[1])
    colNum = ord(colLetter) - 97
    x = colNum 
    y = (8 - rowNum) 
    return (x, y)

def drawBoard(pieceAtAttention=None):
    boardLayout = BOARD.getBoardLayout()
    letters = list(boardLayout.keys())
    legalMoves = []

    kingPosition = BOARD.getKingPosition(BOARD.getTurn())

    if pieceAtAttention:
        legalMoves = BOARD.getLegalMoves(pieceAtAttention)
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(DISPLAYSURF, SQUARE1, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, SQUARE2, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            piece = boardLayout[letters[i]][7 - j]
            if piece != '': 
                DISPLAYSURF.blit(piecePics[piece], (i * GRID_SIZE, j * GRID_SIZE))
            if (letters[i] + str(8-j)) == kingPosition and BOARD.isCheck(kingPosition):
                print(f"{BOARD.getTurn()} is in check!")
                pygame.draw.rect(DISPLAYSURF, CHECK_COLOR, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3) 
            if pieceAtAttention and (i, j) in [chessToPixelsCoords(move) for move in legalMoves]:
                pygame.draw.rect(DISPLAYSURF, HIGHLIGHT, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)
            
if __name__ == '__main__':
    BOARD = Board()
    piecePics = loadImages()

    pieceClicked = False
    pieceAtAttention = None

    while True:
        for event in pygame.event.get():
            # Quitting logic 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse click logic 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not pieceClicked and BOARD.getPieceAtPosition(pixelsToChessCoords(mouse_pos[0], mouse_pos[1])) != '':
                    pieceClicked = True
                    chessPosition = pixelsToChessCoords(mouse_pos[0], mouse_pos[1])
                    pieceAtAttention = chessPosition
                elif pieceClicked and pixelsToChessCoords(mouse_pos[0], mouse_pos[1]) in BOARD.getLegalMoves(pieceAtAttention):
                    BOARD.makeMove(pieceAtAttention, pixelsToChessCoords(mouse_pos[0], mouse_pos[1]))
                    pieceClicked = False
                    pieceAtAttention = None
                else:
                    pieceClicked = False
                    pieceAtAttention = None

        pygame.display.set_caption("Chess | " + BOARD.getTurn() + "'s turn")

        # Draw the board
        drawBoard(pieceAtAttention)
                
        pygame.display.update()
        FramePerSec.tick(FPS)