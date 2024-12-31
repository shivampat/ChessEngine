from piece import * 

class Board:
    """
    TODO:
    - Implement the makeMove method
    - Implement the getLegalMoves method
    - Implement checking feature and checkmate
    - Implement castling
    - Implement en passant
    - Implement promotion
    - Implement stalemate

    Methods required: 
    - makeMove(start, end)
    - getLegalMoves(piece)
        * required submethods for diagonals, horizontals, and verticals
    """
    def __init__(self, pgn=None):
        if pgn:
            pass
        else:
            self.layout = [
                ['R', 'P', '', '', '', '', 'p', 'r'],
                ['N', 'P', '', '', '', '', 'p', 'n'],
                ['B', 'P', '', '', '', '', 'p', 'b'],
                ['Q', 'P', '', '', '', '', 'p', 'q'],
                ['K', 'P', '', '', '', '', 'p', 'k'],
                ['B', 'P', '', '', '', '', 'p', 'b'],
                ['N', 'P', '', '', '', '', 'p', 'n'],
                ['R', 'P', '', '', '', '', 'p', 'r'],
            ]
            self.pieces = [
                [Rook('R', (0, 0), self.layout), Pawn('P', (0, 1), self.layout), None, None, None, None, Pawn('p', (0, 6), self.layout), Rook('r', (0, 7), self.layout)],
                [Knight('N', (1, 0), self.layout), Pawn('P', (1, 1), self.layout), None, None, None, None, Pawn('p', (1, 6), self.layout), Knight('n', (1, 7), self.layout)],
                [Bishop('B', (2, 0), self.layout), Pawn('P', (2, 1), self.layout), None, None, None, None, Pawn('p', (2, 6), self.layout), Bishop('b', (2, 7), self.layout)],
                [Queen('Q', (3, 0), self.layout), Pawn('P', (3, 1), self.layout), None, None, None, None, Pawn('p', (3, 6), self.layout), Queen('q', (3, 7), self.layout)],
                [King('K', (4, 0), self.layout), Pawn('P', (4, 1), self.layout), None, None, None, None, Pawn('p', (4, 6), self.layout), King('k', (4, 7), self.layout)],
                [Bishop('B', (5, 0), self.layout), Pawn('P', (5, 1), self.layout), None, None, None, None, Pawn('p', (5, 6), self.layout), Bishop('b', (5, 7), self.layout)],
                [Knight('N', (6, 0), self.layout), Pawn('P', (6, 1), self.layout), None, None, None, None, Pawn('p', (6, 6), self.layout), Knight('n', (6, 7), self.layout)],
                [Rook('R', (7, 0), self.layout), Pawn('P', (7, 1), self.layout), None, None, None, None, Pawn('p', (7, 6), self.layout), Rook('r', (7, 7), self.layout)],
            ]
            
        self.PGN = "" if pgn is None else pgn
        self.isWhiteTurn = True 
        self.whiteKingPos = (4, 0)
        self.blackKingPos = (4, 7)
        self.isWhiteChecked = False
        self.isBlackChecked = False

    def makeMove(self, start, end):
        """
        Make a move on the board
        start: tuple of coords to start position 
        end: tuple of coords to end position 
        """
        if self.isWhiteTurn != self.layout[start[0]][start[1]].isupper(): 
            print("It is not your turn!")
            return

        if end in self.getLegalMoves(start):
            oldLayoutPiece = self.layout[end[0]][end[1]]
            oldPiece = self.pieces[end[0]][end[1]]

            if oldPiece:
                print(f"{"White" if oldLayoutPiece.isupper() else "Black"} {oldPiece.pieceName} at {coordsToAlgebraic(end)} captured" + \
                      f" by {"White" if self.layout[start[0]][start[1]].isupper() else "Black"} {self.getPieceType(start).pieceName} at {coordsToAlgebraic(start)}.")

            if self.layout[start[0]][start[1]] == 'K':
                self.whiteKingPos = end
            elif self.layout[start[0]][start[1]] == 'k':
                self.blackKingPos = end

            self.layout[end[0]][end[1]] = self.layout[start[0]][start[1]]
            self.layout[start[0]][start[1]] = ''

            self.pieces[end[0]][end[1]] = self.pieces[start[0]][start[1]]
            self.pieces[start[0]][start[1]] = None
            self.pieces[end[0]][end[1]].changePosition(end)

            self.isWhiteTurn = not self.isWhiteTurn
        else:
            print("Illegal move. Please try again.")
        
        # Update check statuses
        if self.isWhiteTurn and self.pieces[self.whiteKingPos[0]][self.whiteKingPos[1]].isChecked():
            print("White king is checked!")
            self.isWhiteChecked = True
        elif not self.isWhiteTurn and self.pieces[self.blackKingPos[0]][self.blackKingPos[1]].isChecked():
            print("Black king is checked!")
            self.isBlackChecked = True
        else:
            self.isBlackChecked = False
            self.isWhiteChecked = False 

    def getLegalMoves(self, pos):
        """
        Get the legal moves of a piece
        pos: tuple of coords to piece being checked
        """
        piece = self.getPieceType(pos)
        if piece is None:
            print("Empty square.")
            return 
        return piece.getLegalMoves()

    def getBoardLayout(self):
        return self.layout
    
    def printBoard(self):
        print("  a b c d e f g h")
        for i in range(7, -1, -1):
            print(f"{i+1}", end=" ")
            for j in range(len(self.layout)):
                if self.layout[j][i] == '':
                    print("  ", end="")
                else:
                    print(self.layout[j][i] + " ", end="")
            print()

    def getPieceType(self, pos):
        """
        Get the type of piece
        piece: string of piece
        pos: tuple of position
        """
        return self.pieces[pos[0]][pos[1]]
    
    def getPieceAtPosition(self, pos):
        return self.layout[pos[0]][pos[1]]
    
    def getTurn(self):
        return "White" if self.isWhiteTurn else "Black"

def coordsToAlgebraic(coords):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return letters[coords[0]] + str(coords[1] + 1)