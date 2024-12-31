class Piece:
    def __init__(self, piece: str, pos: tuple, boardLayout: list[list[str]]):
        self.color = "white" if piece.isupper() else "black"
        self.piece = piece
        self.boardLayout = boardLayout
        self.x = pos[0]
        self.y = pos[1]

    def getAlgebraic(self):
        return chr(self.x + 97) + str(self.y + 1)
    
    def getHorizontals(self):
        horizontals = []
        # Left
        for i in range(self.x - 1, -1, -1):
            if self.boardLayout[i][self.y] == "":
                horizontals.append((i, self.y)) 
            elif self.boardLayout[i][self.y].islower() and self.color == "white":
                horizontals.append((i, self.y))
                break
            elif self.boardLayout[i][self.y].isupper() and self.color == "black":
                horizontals.append((i, self.y))
                break
            else:
                break
        
        # Right
        for i in range(self.x + 1, 8):
            if self.boardLayout[i][self.y] == "":
                horizontals.append((i, self.y))
            elif self.boardLayout[i][self.y].islower() and self.color == "white":
                horizontals.append((i, self.y))
                break
            elif self.boardLayout[i][self.y].isupper() and self.color == "black":
                horizontals.append((i, self.y))
                break
            else:
                break
        
        return horizontals

    def getVerticals(self):
        verticals = []
        # Up
        for i in range(self.y + 1, 8):
            if self.boardLayout[self.x][i] == "":
                verticals.append((self.x, i))
            elif self.boardLayout[self.x][i].islower() and self.color == "white":
                verticals.append((self.x, i))
                break
            elif self.boardLayout[self.x][i].isupper() and self.color == "black":
                verticals.append((self.x, i))
                break
            else:
                break

        # Down
        for i in range(self.y - 1, -1, -1):
            if self.boardLayout[self.x][i] == "":
                verticals.append((self.x, i))
            elif self.boardLayout[self.x][i].islower() and self.color == "white":
                verticals.append((self.x, i))
                break
            elif self.boardLayout[self.x][i].isupper() and self.color == "black":
                verticals.append((self.x, i))
                break
            else:
                break
        return verticals

    def getDiagonals(self):
        diags = []
        # Upper Left
        i = 0
        dx = range(self.x - 1, -1, -1)
        dy = range(self.y + 1, 8)
        while i < len(dx) and i < len(dy):
            if self.boardLayout[dx[i]][dy[i]] == "":
                diags.append((dx[i], dy[i]))
            elif self.boardLayout[dx[i]][dy[i]].islower() and self.color == "white":
                diags.append((dx[i], dy[i]))
                break
            elif self.boardLayout[dx[i]][dy[i]].isupper() and self.color == "black":
                diags.append((dx[i], dy[i]))
                break
            else:
                break
            i += 1
        # Upper Right
        i = 0
        dx = range(self.x + 1, 8)
        dy = range(self.y + 1, 8)
        while i < len(dx) and i < len(dy):
            if self.boardLayout[dx[i]][dy[i]] == "":
                diags.append((dx[i], dy[i]))
            elif self.boardLayout[dx[i]][dy[i]].islower() and self.color == "white":
                diags.append((dx[i], dy[i]))
                break
            elif self.boardLayout[dx[i]][dy[i]].isupper() and self.color == "black":
                diags.append((dx[i], dy[i]))
                break
            else:
                break
            i += 1
        # Lower Left
        i = 0
        dx = range(self.x - 1, -1, -1)
        dy = range(self.y - 1, -1, -1)
        while i < len(dx) and i < len(dy):
            if self.boardLayout[dx[i]][dy[i]] == "":
                diags.append((dx[i], dy[i]))
            elif self.boardLayout[dx[i]][dy[i]].islower() and self.color == "white":
                diags.append((dx[i], dy[i]))
                break
            elif self.boardLayout[dx[i]][dy[i]].isupper() and self.color == "black":
                diags.append((dx[i], dy[i]))
                break
            else:
                break
            i += 1
        # Lower Right
        i = 0
        dx = range(self.x + 1, 8)
        dy = range(self.y - 1, -1, -1)
        while i < len(dx) and i < len(dy):
            if self.boardLayout[dx[i]][dy[i]] == "":
                diags.append((dx[i], dy[i]))
            elif self.boardLayout[dx[i]][dy[i]].islower() and self.color == "white":
                diags.append((dx[i], dy[i]))
                break
            elif self.boardLayout[dx[i]][dy[i]].isupper() and self.color == "black":
                diags.append((dx[i], dy[i]))
                break
            else:
                break
            i += 1
        
        return diags

    def getPosition(self):
        return (self.x, self.y)
    
    def changePosition(self, newPos):
        self.x = newPos[0]
        self.y = newPos[1]
    
    def changeLayout(self, newLayout):
        self.boardLayout = newLayout

    def __str__(self):
        return f'{self.color} piece at {self.x}, {self.y}'

class Pawn(Piece):
    def __init__(self, piece: str, pos: tuple, boardLayout: list[list[str]]):
        super().__init__(piece, pos, boardLayout)
        self.pieceName = "pawn"

    def getLegalMoves(self):
        legalMoves = []
        if self.color == "white":
            if self.boardLayout[self.x][self.y + 1] == "":
                legalMoves.append((self.x, self.y + 1))
                if self.y == 1 and self.boardLayout[self.x][self.y + 2] == "":
                    legalMoves.append((self.x, self.y + 2))
            if self.x > 0 and self.boardLayout[self.x - 1][self.y + 1].islower():
                legalMoves.append((self.x - 1, self.y + 1))
            if self.x < 7 and self.boardLayout[self.x + 1][self.y + 1].islower():
                legalMoves.append((self.x + 1, self.y + 1))
        else:
            if self.boardLayout[self.x][self.y - 1] == "":
                legalMoves.append((self.x, self.y - 1))
                if self.y == 6 and self.boardLayout[self.x][self.y - 2] == "":
                    legalMoves.append((self.x, self.y - 2))
            if self.x > 0 and self.boardLayout[self.x - 1][self.y - 1].isupper():
                legalMoves.append((self.x - 1, self.y - 1))
            if self.x < 7 and self.boardLayout[self.x + 1][self.y - 1].isupper():
                legalMoves.append((self.x + 1, self.y - 1))

        return legalMoves

    def __str__(self):
        return f'{self.color} pawn at {self.x}, {self.y}'
    
class Rook(Piece):
    def __init__(self, piece: str, pos: tuple, boardLayout: list[list[str]]):
        super().__init__(piece, pos, boardLayout)
        self.pieceName = "rook"

    def getLegalMoves(self):
        return self.getHorizontals() + self.getVerticals()

    def __str__(self):
        return f'{self.color} rook at {self.x}, {self.y}'

class Knight(Piece):
    def __init__(self, piece: str, pos: tuple, boardLayout: list[list[str]]):
        super().__init__(piece, pos, boardLayout)
        self.pieceName = "knight"

    def getLegalMoves(self):
        legalMoves = []
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for move in moves:
            x = self.x + move[0]
            y = self.y + move[1]
            if x >= 0 and x < 8 and y >= 0 and y < 8:
                if self.boardLayout[x][y] == "" or \
                      (self.boardLayout[x][y].islower() and self.color == "white") or \
                          (self.boardLayout[x][y].isupper() and self.color == "black"):
                    legalMoves.append((x, y))
        return legalMoves

    def __str__(self):
        return f'{self.color} knight at {self.x}, {self.y}'

class Bishop(Piece):
    def __init__(self, piece: str, pos: tuple, boardLayout: list[list[str]]):
        super().__init__(piece, pos, boardLayout)
        self.pieceName = "bishop"

    def getLegalMoves(self):
        return self.getDiagonals()

    def __str__(self):
        return f'{self.color} bishop at {self.x}, {self.y}'

class Queen(Piece):
    def __init__(self, piece: str, pos: tuple, boardLayout: list[list[str]]):
        super().__init__(piece, pos, boardLayout)
        self.pieceName = "queen"

    def getLegalMoves(self):
        return self.getHorizontals() + self.getVerticals() + self.getDiagonals() 

    def __str__(self):
        return f'{self.color} queen at {self.x}, {self.y}'

class King(Piece):
    def __init__(self, piece: str, pos: tuple, boardLayout: list[list[str]]):
        super().__init__(piece, pos, boardLayout)
        self.pieceName = "king"

    def getLegalMoves(self):
        legalMoves = []
        moves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        for move in moves:
            x = self.x + move[0]
            y = self.y + move[1]
            if x >= 0 and x < 8 and y >= 0 and y < 8:
                if self.boardLayout[x][y] == "" or \
                      (self.boardLayout[x][y].islower() and self.color == "white") or \
                          (self.boardLayout[x][y].isupper() and self.color == "black"):
                    legalMoves.append((x, y))
        return legalMoves
    
    def isChecked(self):
        diagonals = self.getDiagonals()
        horizontals = self.getHorizontals()
        verticals = self.getVerticals()

        if self.color == "white":
            for diag in diagonals:
                if self.boardLayout[diag[0]][diag[1]].lower() in ["b", "q"]:
                    return True
            for hor in horizontals:
                if self.boardLayout[hor[0]][hor[1]].lower() in ["r", "q"]:
                    return True
            for vert in verticals:
                if self.boardLayout[vert[0]][vert[1]].lower() in ["r", "q"]:
                    return True
        else:
            for diag in diagonals:
                if self.boardLayout[diag[0]][diag[1]].upper() in ["B", "Q"]:
                    return True
            for hor in horizontals:
                if self.boardLayout[hor[0]][hor[1]].upper() in ["R", "Q"]:
                    return True
            for vert in verticals:
                if self.boardLayout[vert[0]][vert[1]].upper() in ["R", "Q"]:
                    return True
                
        # Pawn checks
        if self.color == "white":
            moves = [(1, 1), (-1, 1)]
            for move in moves:
                x = self.x + move[0]
                y = self.y + move[1]
                if x >= 0 and x < 8 and y >= 0 and y < 8:
                    if self.boardLayout[x][y] == "p":
                        return True
        else:
            moves = [(1, -1), (-1, -1)]
            for move in moves:
                x = self.x + move[0]
                y = self.y + move[1]
                if x >= 0 and x < 8 and y >= 0 and y < 8:
                    if self.boardLayout[x][y] == "P":
                        return True
        
        # Knight checks
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for move in moves:
            x = self.x + move[0]
            y = self.y + move[1]
            if x >= 0 and x < 8 and y >= 0 and y < 8:
                if self.boardLayout[x][y] == "n" and self.color == "white":
                    return True
                elif self.boardLayout[x][y] == "N" and self.color == "black":
                    return True


    def __str__(self):
        return f'{self.color} king at {self.x}, {self.y}'
    