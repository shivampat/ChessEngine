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
HIGHLIGHT = (0, 255, 255)
CHECK_COLOR = (255, 0, 0)
SELECTION = (217, 242, 170) 

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
    return (x // GRID_SIZE, 7 - y // GRID_SIZE)

def drawGrid(pieceAtAttention=None):
    for i in range(8):
        for j in range(7, -1, -1):
            if (i + j) % 2 == 0:
                pygame.draw.rect(DISPLAYSURF, SQUARE1, (i * GRID_SIZE, (7-j) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, SQUARE2, (i * GRID_SIZE, (7-j) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            if pieceAtAttention is not None and BOARD.getLegalMoves(pieceAtAttention) is not None and (i, j) in BOARD.getLegalMoves(pieceAtAttention):
                # print(i * GRID_SIZE, j * GRID_SIZE)
                # pygame.draw.rect(DISPLAYSURF, HIGHLIGHT, (i * GRID_SIZE, (7-j) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.circle(DISPLAYSURF, HIGHLIGHT, (i * GRID_SIZE + GRID_SIZE // 2, (7-j) * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 4)
            if pieceAtAttention is not None and (i, j) == pieceAtAttention:
                pygame.draw.rect(DISPLAYSURF, SELECTION, (i * GRID_SIZE, (7-j) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            if BOARD.isBlackChecked and (i, j) == BOARD.blackKingPos:
                pygame.draw.rect(DISPLAYSURF, CHECK_COLOR, (i * GRID_SIZE, (7-j) * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def drawPieces(boardLayout):
    for i in range(8):
        for j in range(8):
            piece = boardLayout[i][j]
            if piece != '':
                DISPLAYSURF.blit(piecePics[piece], (i * GRID_SIZE, (7-j) * GRID_SIZE))

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
                chess_pos = pixelsToChessCoords(mouse_pos[0], mouse_pos[1])
                boardLayout = BOARD.getBoardLayout()
                if not pieceClicked and boardLayout[chess_pos[0]][chess_pos[1]] != '':
                    pieceAtAttention = chess_pos 
                    pieceClicked = True
                elif pieceClicked and chess_pos in BOARD.getLegalMoves(pieceAtAttention):
                    BOARD.makeMove(pieceAtAttention, chess_pos)
                    pieceClicked = False
                    pieceAtAttention = None
                else:
                    pieceClicked = False
                    pieceAtAttention = None
        # print(pygame.mouse.get_pos())
        pygame.display.set_caption("Chess | " + BOARD.getTurn() + "'s turn")

        # Draw the board
        drawGrid(pieceAtAttention)
        drawPieces(BOARD.getBoardLayout())
                
        pygame.display.update()
        FramePerSec.tick(FPS)