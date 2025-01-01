from piece import * 

class Board:
    """
    TODO:
    - Implement en passant
    - Implement promotion (pawn to queen is done, need to add pawn to rook, bishop, knight)
    """
    def __init__(self, fen=None):
        self.fen = "" if fen is None else fen
        self.isWhiteTurn = True 
        self.whiteKingPos = (4, 0)
        self.blackKingPos = (4, 7)
        self.isWhiteChecked = False
        self.isBlackChecked = False
        self.gameEnded = False
        if fen:
            self.layout = self.__fenToBoardLayout(fen)
            self.__populatePiecesFromLayout()
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

        print("Board initialized.")
        print("White king at", self.whiteKingPos)
        print("Black king at", self.blackKingPos)
        print("White checked?", self.isWhiteChecked)
        print("Black checked?", self.isBlackChecked)

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

            # Used for castline, calculating rook positions
            if self.layout[start[0]][start[1]] == 'K':
                castleKingPositions = [(2, 0), (6, 0)]
                castleRookPositions = [(3, 0), (5, 0)]
                originalRookPositions = [(0, 0), (7, 0)]
                self.whiteKingPos = end
            elif self.layout[start[0]][start[1]] == 'k':
                castleKingPositions = [(2, 7), (6, 7)]
                castleRookPositions = [(3, 7), (5, 7)]
                originalRookPositions = [(0, 7), (7, 7)]
                self.blackKingPos = end

            # Moving rook in castling
            if self.layout[start[0]][start[1]].lower() == 'k' and end in castleKingPositions:
                rook = self.pieces[originalRookPositions[castleKingPositions.index(end)][0]][originalRookPositions[castleKingPositions.index(end)][1]]
                self.layout[castleRookPositions[castleKingPositions.index(end)][0]][castleRookPositions[castleKingPositions.index(end)][1]] = rook.piece
                self.layout[originalRookPositions[castleKingPositions.index(end)][0]][originalRookPositions[castleKingPositions.index(end)][1]] = ''
                self.pieces[castleRookPositions[castleKingPositions.index(end)][0]][castleRookPositions[castleKingPositions.index(end)][1]] = rook
                self.pieces[originalRookPositions[castleKingPositions.index(end)][0]][originalRookPositions[castleKingPositions.index(end)][1]] = None
                rook.changePosition(castleRookPositions[castleKingPositions.index(end)])

            # Move the piece in layout grid
            self.layout[end[0]][end[1]] = self.layout[start[0]][start[1]]
            self.layout[start[0]][start[1]] = ''

            # Update piece object in piece grid
            self.pieces[end[0]][end[1]] = self.pieces[start[0]][start[1]]
            self.pieces[start[0]][start[1]] = None
            self.pieces[end[0]][end[1]].changePosition(end)

            # Pawn promotion
            if self.layout[end[0]][end[1]].lower() == 'p' and (end[1] == 0 or end[1] == 7):
                self.layout[end[0]][end[1]] = 'Q' if self.layout[end[0]][end[1]].isupper() else 'q'
                self.pieces[end[0]][end[1]] = Queen(self.layout[end[0]][end[1]], end, self.getBoardLayout())
                print("Pawn promoted to queen!")

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
        
        self.printBoard()
        if self.isCheckmate():
            self.gameEnded = True
            print("Checkmate!")
            print("Black wins!" if self.isWhiteTurn else "White wins!")
        elif self.isStalemate():
            print("Stalemate!")
            print("It's a draw!")

    def getLegalMoves(self, pos):
        """
        Get the legal moves of a piece
        pos: tuple of coords to piece being checked
        """
        piece = self.getPieceType(pos)
        if piece is None:
            print("Empty square.")
            return 

        # Remove moves that cause check
        kingPos = self.whiteKingPos if piece.color == 'white' else self.blackKingPos
        allMoves = piece.getLegalMoves()
        legalMoves = []
        for move in allMoves:
            if not doesMoveCauseCheck(self.getBoardLayout(), pos, move, kingPos):
                legalMoves.append(move)

        # Add castling moves
        if piece.color == 'white':
            rookCoords = [(0, 0), (7, 0)]
            inBetweenCoords1 = [(1, 0), (2, 0), (3, 0)]
            inBetweenCoords2 = [(5, 0), (6, 0)]
            castleCoords = [(2, 0), (6, 0)]
        else:
            rookCoords = [(0, 7), (7, 7)]
            inBetweenCoords1 = [(1, 7), (2, 7), (3, 7)]
            inBetweenCoords2 = [(5, 7), (6, 7)]
            castleCoords = [(2, 7), (6, 7)]
        
        if piece.pieceName == 'king' and not piece.didPieceMove():
            rook1 = self.pieces[rookCoords[0][0]][rookCoords[0][1]]
            rook2 = self.pieces[rookCoords[1][0]][rookCoords[1][1]]
            if rook1 is not None and rook1.pieceName == 'rook' and not rook1.didPieceMove():
                for coord in inBetweenCoords1:
                    if self.layout[coord[0]][coord[1]] != '' or doesMoveCauseCheck(self.getBoardLayout(), pos, coord, kingPos):
                        break
                    elif coord == inBetweenCoords1[-1]:
                        legalMoves.append(castleCoords[0])
            if rook2 is not None and rook2.pieceName == 'rook' and not rook2.didPieceMove():
                for coord in inBetweenCoords2:
                    if self.layout[coord[0]][coord[1]] != '' or doesMoveCauseCheck(self.getBoardLayout(), pos, coord, kingPos):
                        break
                    elif coord == inBetweenCoords2[-1]:
                        legalMoves.append(castleCoords[1])

        return legalMoves 
    
    def isCheckmate(self):
        king = self.pieces[self.whiteKingPos[0]][self.whiteKingPos[1]] if self.isWhiteTurn else self.pieces[self.blackKingPos[0]][self.blackKingPos[1]]
        if king.isChecked():
            for i in range(8):
                for j in range(8):
                    if self.layout[i][j] != '' and self.layout[i][j].isupper() == self.isWhiteTurn:
                        if self.getLegalMoves((i, j)):
                            return False
            return True
        return False

    def isStalemate(self):
        king = self.pieces[self.whiteKingPos[0]][self.whiteKingPos[1]] if self.isWhiteTurn else self.pieces[self.blackKingPos[0]][self.blackKingPos[1]]
        if not king.isChecked():
            for i in range(8):
                for j in range(8):
                    if self.layout[i][j] != '' and self.layout[i][j].isupper() == self.isWhiteTurn:
                        if self.getLegalMoves((i, j)):
                            return False
            return True
        return False 

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

    def __fenToBoardLayout(self, fen):
        """
        Convert a FEN string to a board layout
        fen: string of FEN
        """
        board_layout = fen.split()[0]
        self.isWhiteTurn = fen.split()[1] == 'w'
        layout = [[] for _ in range(8)]
        ranks = board_layout.split('/')[::-1]
        for rank in ranks:
            column_index = 0
            for char in rank:
                if char.isdigit():
                    for _ in range(int(char)):
                        layout[column_index].append('')
                        column_index += 1
                else:
                    layout[column_index].append(char)
                    column_index += 1
        return layout

    def __populatePiecesFromLayout(self):
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        pieceDict = {
            'p': Pawn,
            'r': Rook,
            'n': Knight,
            'b': Bishop,
            'q': Queen,
            'k': King,
        }
        for i in range(8):
            for j in range(8):
                if self.layout[i][j] != '':
                    self.pieces[i][j] = pieceDict[self.layout[i][j].lower()](self.layout[i][j], (i, j), self.getBoardLayout())
                if self.layout[i][j] == 'K':
                    self.whiteKingPos = (i, j)
                    self.isWhiteChecked = self.pieces[i][j].isChecked()
                elif self.layout[i][j] == 'k':
                    self.blackKingPos = (i, j)
                    self.isBlackChecked = self.pieces[i][j].isChecked()
        pass

def coordsToAlgebraic(coords):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return letters[coords[0]] + str(coords[1] + 1)