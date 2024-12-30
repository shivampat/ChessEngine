class Board:
    def __init__(self, pgn=None):
        if pgn:
            pass
        else:
            self.layout = {
                "a": ['R', 'P', '', '', '', '', 'p', 'r'],
                "b": ['N', 'P', '', '', '', '', 'p', 'n'],
                "c": ['B', 'P', '', '', '', '', 'p', 'b'],
                "d": ['Q', 'P', '', '', '', '', 'p', 'q'],
                "e": ['K', 'P', '', '', '', '', 'p', 'k'],
                "f": ['B', 'P', '', '', '', '', 'p', 'b'],
                "g": ['N', 'P', '', '', '', '', 'p', 'n'],
                "h": ['R', 'P', '', '', '', '', 'p', 'r'],
            }

        self.whiteTurn = True
        self.blackTurn = False

        self.whiteCaptured = []
        self.blackCaptured = []

        self.whiteIsChecked = False
        self.blackIsChecked = False 

        self.PGN = "" if pgn is None else pgn

    def isCheck(self, kingPosition):
        """
        kingPosition: position of king in algebraic notation. Ex: "e1"
        """
        # Horizontal and vertical checks 

        # if self.layout[kingPosition[0].lower()][int(kingPosition[1])-1] not in ['k', 'K']:
        #     print("Position given is not a king!")
        #     return False
        isWhite = self.layout[kingPosition[0].lower()][int(kingPosition[1])-1].isupper()

        if isWhite:
            knights = ['n']
            bishopAndQueen = ['b', 'q']
            rookAndQueen = ['r', 'q']
        else:
            knights = ['N']
            bishopAndQueen = ['B', 'Q']
            rookAndQueen = ['R', 'Q']

        keys = list(self.layout.keys())
        index = keys.index(kingPosition[0].lower())
        indexLeft = index - 1 if index - 1 >= 0 else None
        indexRight = index + 1 if index + 1 <= 7 else None
        # Check left
        while indexLeft is not None and indexLeft >= 0:
            if self.layout[keys[indexLeft]][int(kingPosition[1])-1] in rookAndQueen: 
                return True
            elif self.layout[keys[indexLeft]][int(kingPosition[1])-1] != '':
                break
            indexLeft -= 1
        # Check right 
        while indexRight is not None and indexRight <= 7:
            if self.layout[keys[indexLeft]][int(kingPosition[1])-1] in rookAndQueen: 
                return True
            elif self.layout[keys[indexLeft]][int(kingPosition[1])-1] != '':
                break
            indexRight += 1
        # Check up 
        vert_index = int(kingPosition[1]) - 1
        indexUp = vert_index + 1 if vert_index + 1 <= 7 else None
        indexDown = vert_index - 1 if vert_index - 1 >= 0 else None
        while indexUp is not None and indexUp <= 7:
            if self.layout[kingPosition[0].lower()][indexUp] in rookAndQueen: 
                return True
            elif self.layout[kingPosition[0].lower()][indexUp] != '':
                break
            indexUp += 1
        # Check down
        while indexDown is not None and indexDown >= 0:
            if self.layout[kingPosition[0].lower()][indexDown] in rookAndQueen: 
                return True
            elif self.layout[kingPosition[0].lower()][indexDown] != '':
                break
            indexDown -= 1
        
        # Diagonal checks
        # Upper left diagonal
        indxLeft = index - 1 if index - 1 >= 0 else None
        oneUp = int(kingPosition[1]) if int(kingPosition[1]) <= 7 else None

        # pawn check TODO

        while indxLeft is not None and indxLeft >= 0 and oneUp is not None and oneUp <= 7:
            if self.layout[keys[indxLeft]][oneUp] in bishopAndQueen: 
                return True
            elif self.layout[keys[indxLeft]][oneUp] != '':
                break
            indxLeft -= 1
            oneUp += 1
        # Upper right diagonal
        indxRight = index + 1 if index + 1 <= 7 else None
        oneUp = int(kingPosition[1]) if int(kingPosition[1]) <= 7 else None
        while indxRight is not None and indxRight <= 7 and oneUp is not None and oneUp <= 7:
            if self.layout[keys[indxRight]][oneUp] in bishopAndQueen: 
                return True
            elif self.layout[keys[indxRight]][oneUp] != '':
                break
            indxRight += 1
            oneUp += 1
        # Lower left diagonal
        indxLeft = index - 1 if index - 1 >= 0 else None
        oneDown = int(kingPosition[1]) - 2 if int(kingPosition[1]) - 2 >= 0 else None
        while indxLeft is not None and indxLeft >= 0 and oneDown is not None and oneDown >= 0:
            if self.layout[keys[indxLeft]][oneDown] in bishopAndQueen: 
                return True
            elif self.layout[keys[indxLeft]][oneDown] != '':
                break
            indxLeft -= 1
            oneDown -= 1
        # Lower right diagonal
        indxRight = index + 1 if index + 1 <= 7 else None
        oneDown = int(kingPosition[1]) - 2 if int(kingPosition[1]) - 2 >= 0 else None
        while indxRight is not None and indxRight <= 7 and oneDown is not None and oneDown >= 0:
            if self.layout[keys[indxRight]][oneDown] in bishopAndQueen: 
                return True
            elif self.layout[keys[indxRight]][oneDown] != '':
                break
            indxRight += 1
            oneDown -= 1
        
        # Knight checks
        twoUpIndx = int(kingPosition[1]) + 1 if int(kingPosition[1]) + 1 <= 7 else None
        twoDownIndx = int(kingPosition[1]) - 3 if int(kingPosition[1]) - 3 >= 0 else None
        oneLeft = index - 1 if index - 1 >= 0 else None
        oneRight = index + 1 if index + 1 <= 7 else None
        if twoUpIndx and oneLeft and self.layout[keys[oneLeft]][twoUpIndx] in knights:
            return True
        if twoUpIndx and oneRight and self.layout[keys[oneRight]][twoUpIndx] in knights:
            return True
        if twoDownIndx and oneLeft and self.layout[keys[oneLeft]][twoDownIndx] in knights:
            return True
        if twoDownIndx and oneRight and self.layout[keys[oneRight]][twoDownIndx] in knights:
            return True

        twoLeftIndx = index - 2 if index - 2 >= 0 else None
        twoRightIndx = index + 2 if index + 2 <= 7 else None
        oneUp = int(kingPosition[1]) if int(kingPosition[1]) <= 7 else None
        oneDown = int(kingPosition[1]) - 2 if int(kingPosition[1]) - 2 >= 0 else None
        if twoLeftIndx and oneUp and self.layout[keys[twoLeftIndx]][oneUp] in knights:
            return True
        if twoLeftIndx and oneDown and self.layout[keys[twoLeftIndx]][oneDown] in knights:
            return True
        if twoRightIndx and oneUp and self.layout[keys[twoRightIndx]][oneUp] in knights:
            return True
        if twoRightIndx and oneDown and self.layout[keys[twoRightIndx]][oneDown] in knights:
            return True
        
        return False
        
    def isNewMoveCheck(self, kingPosition, newPosition):
        """
        kingPosition: position of king in algebraic notation. Ex: "e1"
        newPosition: new position of king in algebraic notation. Ex: "e1"
        """
        # Horizontal and vertical checks 

        if self.layout[kingPosition[0].lower()][int(kingPosition[1])-1] not in ['k', 'K']:
            print("Position given is not a king!")
            return False
        isWhite = self.layout[kingPosition[0].lower()][int(kingPosition[1])-1].isupper()

        if isWhite:
            knights = ['n']
            bishopAndQueen = ['b', 'q']
            rookAndQueen = ['r', 'q']
        else:
            knights = ['N']
            bishopAndQueen = ['B', 'Q']
            rookAndQueen = ['R', 'Q']

        keys = list(self.layout.keys())
        index = keys.index(newPosition[0].lower())
        indexLeft = index - 1 if index - 1 >= 0 else None
        indexRight = index + 1 if index + 1 <= 7 else None
        # Check left
        while indexLeft is not None and indexLeft >= 0:
            if self.layout[keys[indexLeft]][int(newPosition[1])-1] in rookAndQueen: 
                return True
            elif self.layout[keys[indexLeft]][int(newPosition[1])-1] != '':
                break
            indexLeft -= 1
        # Check right 
        while indexRight is not None and indexRight <= 7:
            if self.layout[keys[indexLeft]][int(newPosition[1])-1] in rookAndQueen: 
                return True
            elif self.layout[keys[indexLeft]][int(newPosition[1])-1] != '':
                break
            indexRight += 1
        # Check up 
        vert_index = int(newPosition[1]) - 1
        indexUp = vert_index + 1 if vert_index + 1 <= 7 else None
        indexDown = vert_index - 1 if vert_index - 1 >= 0 else None
        while indexUp is not None and indexUp <= 7:
            if self.layout[newPosition[0].lower()][indexUp] in rookAndQueen: 
                return True
            elif self.layout[newPosition[0].lower()][indexUp] != '':
                break
            indexUp += 1
        # Check down
        while indexDown is not None and indexDown >= 0:
            if self.layout[newPosition[0].lower()][indexDown] in rookAndQueen: 
                return True
            elif self.layout[newPosition[0].lower()][indexDown] != '':
                break
            indexDown -= 1
        
        # Diagonal checks
        # Upper left diagonal
        indxLeft = index - 1 if index - 1 >= 0 else None
        oneUp = int(newPosition[1]) if int(newPosition[1]) <= 7 else None

        # pawn check TODO

        while indxLeft is not None and indxLeft >= 0 and oneUp is not None and oneUp <= 7:
            if self.layout[keys[indxLeft]][oneUp] in bishopAndQueen: 
                return True
            elif self.layout[keys[indxLeft]][oneUp] != '':
                break
            indxLeft -= 1
            oneUp += 1
        # Upper right diagonal
        indxRight = index + 1 if index + 1 <= 7 else None
        oneUp = int(newPosition[1]) if int(newPosition[1]) <= 7 else None
        while indxRight is not None and indxRight <= 7 and oneUp is not None and oneUp <= 7:
            if self.layout[keys[indxRight]][oneUp] in bishopAndQueen: 
                return True
            elif self.layout[keys[indxRight]][oneUp] != '':
                break
            indxRight += 1
            oneUp += 1
        # Lower left diagonal
        indxLeft = index - 1 if index - 1 >= 0 else None
        oneDown = int(newPosition[1]) - 2 if int(newPosition[1]) - 2 >= 0 else None
        while indxLeft is not None and indxLeft >= 0 and oneDown is not None and oneDown >= 0:
            if self.layout[keys[indxLeft]][oneDown] in bishopAndQueen: 
                return True
            elif self.layout[keys[indxLeft]][oneDown] != '':
                break
            indxLeft -= 1
            oneDown -= 1
        # Lower right diagonal
        indxRight = index + 1 if index + 1 <= 7 else None
        oneDown = int(newPosition[1]) - 2 if int(newPosition[1]) - 2 >= 0 else None
        while indxRight is not None and indxRight <= 7 and oneDown is not None and oneDown >= 0:
            if self.layout[keys[indxRight]][oneDown] in bishopAndQueen: 
                return True
            elif self.layout[keys[indxRight]][oneDown] != '':
                break
            indxRight += 1
            oneDown -= 1
        
        # Knight checks
        twoUpIndx = int(newPosition[1]) + 1 if int(newPosition[1]) + 1 <= 7 else None
        twoDownIndx = int(newPosition[1]) - 3 if int(newPosition[1]) - 3 >= 0 else None
        oneLeft = index - 1 if index - 1 >= 0 else None
        oneRight = index + 1 if index + 1 <= 7 else None
        if twoUpIndx and oneLeft and self.layout[keys[oneLeft]][twoUpIndx] in knights:
            return True
        if twoUpIndx and oneRight and self.layout[keys[oneRight]][twoUpIndx] in knights:
            return True
        if twoDownIndx and oneLeft and self.layout[keys[oneLeft]][twoDownIndx] in knights:
            return True
        if twoDownIndx and oneRight and self.layout[keys[oneRight]][twoDownIndx] in knights:
            return True

        twoLeftIndx = index - 2 if index - 2 >= 0 else None
        twoRightIndx = index + 2 if index + 2 <= 7 else None
        oneUp = int(newPosition[1]) if int(newPosition[1]) <= 7 else None
        oneDown = int(newPosition[1]) - 2 if int(newPosition[1]) - 2 >= 0 else None
        if twoLeftIndx and oneUp and self.layout[keys[twoLeftIndx]][oneUp] in knights:
            return True
        if twoLeftIndx and oneDown and self.layout[keys[twoLeftIndx]][oneDown] in knights:
            return True
        if twoRightIndx and oneUp and self.layout[keys[twoRightIndx]][oneUp] in knights:
            return True
        if twoRightIndx and oneDown and self.layout[keys[twoRightIndx]][oneDown] in knights:
            return True
        
        return False
    
    def doesMoveBlockCheck(self, piecePosition, newPosition):
        """
        piecePosition: position of piece in algebraic notation. Ex: "e1"
        newPosition: new position of piece in algebraic notation. Ex: "e1"
        """
        kingPosition = self.getKingPosition("White" if self.getPieceAtPosition(piecePosition).isupper() else "Black")

        isWhite = self.layout[kingPosition[0].lower()][int(kingPosition[1])-1].isupper()


        if isWhite:
            knights = ['n']
            bishopAndQueen = ['b', 'q']
            rookAndQueen = ['r', 'q']
        else:
            knights = ['N']
            bishopAndQueen = ['B', 'Q']
            rookAndQueen = ['R', 'Q']

        keys = list(self.layout.keys())
        index = keys.index(kingPosition[0].lower())

        newPosIndex = keys.index(newPosition[0].lower())
        newPosVert = int(newPosition[1]) - 1

        currPosIndex = keys.index(piecePosition[0].lower())
        currPosVert = int(piecePosition[1]) - 1

        indexLeft = index - 1 if index - 1 >= 0 else None
        indexRight = index + 1 if index + 1 <= 7 else None
        # Check left
        while indexLeft is not None and indexLeft >= 0:
            if indexLeft == newPosIndex and int(kingPosition[1]) - 1 == newPosVert:
                break 
            elif indexLeft == currPosIndex and int(kingPosition[1]) - 1 == currPosVert:
                indexLeft -= 1
                continue
            elif self.layout[keys[indexLeft]][int(kingPosition[1])-1] in rookAndQueen: 
                return False
            elif self.layout[keys[indexLeft]][int(kingPosition[1])-1] != '':
                break
            indexLeft -= 1
        # Check right 
        while indexRight is not None and indexRight <= 7:
            if indexRight == newPosIndex and int(kingPosition[1]) - 1 == newPosVert:
                break 
            elif indexRight == currPosIndex and int(kingPosition[1]) - 1 == currPosVert:   
                indexRight += 1
                continue
            elif self.layout[keys[indexLeft]][int(kingPosition[1])-1] in rookAndQueen: 
                return False
            elif self.layout[keys[indexLeft]][int(kingPosition[1])-1] != '':
                break
            indexRight += 1
        # Check up 
        vert_index = int(kingPosition[1]) - 1
        indexUp = vert_index + 1 if vert_index + 1 <= 7 else None
        indexDown = vert_index - 1 if vert_index - 1 >= 0 else None
        while indexUp is not None and indexUp <= 7:
            if indexUp == newPosVert and kingPosition[0].lower() == newPosIndex:
                break
            elif indexUp == currPosVert and kingPosition[0].lower() == currPosIndex:
                indexUp += 1
                continue
            elif self.layout[kingPosition[0].lower()][indexUp] in rookAndQueen: 
                return False
            elif self.layout[kingPosition[0].lower()][indexUp] != '':
                break
            indexUp += 1
        # Check down
        while indexDown is not None and indexDown >= 0:
            if indexDown == newPosVert and kingPosition[0].lower() == newPosIndex:
                break
            elif indexDown == currPosVert and kingPosition[0].lower() == currPosIndex:
                indexDown -= 1
                continue
            elif self.layout[kingPosition[0].lower()][indexDown] in rookAndQueen: 
                return False
            elif self.layout[kingPosition[0].lower()][indexDown] != '':
                break
            indexDown -= 1
        
        # Diagonal checks
        # Upper left diagonal
        indxLeft = index - 1 if index - 1 >= 0 else None
        oneUp = int(kingPosition[1]) if int(kingPosition[1]) <= 7 else None

        # pawn check TODO

        while indxLeft is not None and indxLeft >= 0 and oneUp is not None and oneUp <= 7:
            if indxLeft == newPosIndex and oneUp == newPosVert:
                break
            elif indxLeft == currPosIndex and oneUp == currPosVert:
                indxLeft -= 1
                oneUp += 1
                continue
            elif self.layout[keys[indxLeft]][oneUp] in bishopAndQueen: 
                return False
            elif self.layout[keys[indxLeft]][oneUp] != '':
                break
            indxLeft -= 1
            oneUp += 1
        # Upper right diagonal
        indxRight = index + 1 if index + 1 <= 7 else None
        oneUp = int(kingPosition[1]) if int(kingPosition[1]) <= 7 else None
        while indxRight is not None and indxRight <= 7 and oneUp is not None and oneUp <= 7:
            if indxRight == newPosIndex and oneUp == newPosVert:
                break
            elif indxRight == currPosIndex and oneUp == currPosVert:
                indxRight += 1
                oneUp += 1
                continue
            elif self.layout[keys[indxRight]][oneUp] in bishopAndQueen: 
                return False
            elif self.layout[keys[indxRight]][oneUp] != '':
                break
            indxRight += 1
            oneUp += 1
        # Lower left diagonal
        indxLeft = index - 1 if index - 1 >= 0 else None
        oneDown = int(kingPosition[1]) - 2 if int(kingPosition[1]) - 2 >= 0 else None
        while indxLeft is not None and indxLeft >= 0 and oneDown is not None and oneDown >= 0:
            if indxLeft == newPosIndex and oneDown == newPosVert:
                break
            elif indxLeft == currPosIndex and oneDown == currPosVert:
                indxLeft -= 1
                oneDown -= 1
                continue
            elif self.layout[keys[indxLeft]][oneDown] in bishopAndQueen: 
                return False
            elif self.layout[keys[indxLeft]][oneDown] != '':
                break
            indxLeft -= 1
            oneDown -= 1
        # Lower right diagonal
        indxRight = index + 1 if index + 1 <= 7 else None
        oneDown = int(kingPosition[1]) - 2 if int(kingPosition[1]) - 2 >= 0 else None
        while indxRight is not None and indxRight <= 7 and oneDown is not None and oneDown >= 0:
            if indxRight == newPosIndex and oneDown == newPosVert:
                break
            elif indxRight == currPosIndex and oneDown == currPosVert:
                indxRight += 1
                oneDown -= 1
                continue
            elif self.layout[keys[indxRight]][oneDown] in bishopAndQueen: 
                return False
            elif self.layout[keys[indxRight]][oneDown] != '':
                break
            indxRight += 1
            oneDown -= 1
        
        # Knight checks
        twoUpIndx = int(kingPosition[1]) + 1 if int(kingPosition[1]) + 1 <= 7 else None
        twoDownIndx = int(kingPosition[1]) - 3 if int(kingPosition[1]) - 3 >= 0 else None
        oneLeft = index - 1 if index - 1 >= 0 else None
        oneRight = index + 1 if index + 1 <= 7 else None
        if twoUpIndx and oneLeft and self.layout[keys[oneLeft]][twoUpIndx] in knights:
            return False
        if twoUpIndx and oneRight and self.layout[keys[oneRight]][twoUpIndx] in knights:
            return False
        if twoDownIndx and oneLeft and self.layout[keys[oneLeft]][twoDownIndx] in knights:
            return False
        if twoDownIndx and oneRight and self.layout[keys[oneRight]][twoDownIndx] in knights:
            return False
        
        twoLeftIndx = index - 2 if index - 2 >= 0 else None
        twoRightIndx = index + 2 if index + 2 <= 7 else None
        oneUp = int(kingPosition[1]) if int(kingPosition[1]) <= 7 else None
        oneDown = int(kingPosition[1]) - 2 if int(kingPosition[1]) - 2 >= 0 else None
        if twoLeftIndx and oneUp and self.layout[keys[twoLeftIndx]][oneUp] in knights:
            return False
        if twoLeftIndx and oneDown and self.layout[keys[twoLeftIndx]][oneDown] in knights:
            return False
        if twoRightIndx and oneUp and self.layout[keys[twoRightIndx]][oneUp] in knights:
            return False
        if twoRightIndx and oneDown and self.layout[keys[twoRightIndx]][oneDown] in knights:
            return False
        
        return True 
        


    def getLegalMoves(self, position):
        """
        Calculates legal moves for a piece given its position and piece type.
        Returns list of positions it can move to in algebraic notation.
        Position is a string in algebraic notation. Ex: "a1"
        """
        piece = self.layout[position[0].lower()][int(position[1])-1]
        WHITE_PIECES = ["P", "R","N", "B", "Q", "K"]
        BLACK_PIECES = ["p", "r", "n", "b", "q", "k"]
        finalPositions = []

        if piece.islower():
            # Black piece
            if piece == 'p':
                # Check if pawn can move two squares
                if position[1] == '7':
                    if self.layout[position[0].lower()][int(position[1])-2] == '':
                        finalPositions.append(position[0] + str(int(position[1])-1))
                        if self.layout[position[0].lower()][int(position[1])-3] == '':
                            finalPositions.append(position[0] + str(int(position[1])-2))
                else:
                    if self.layout[position[0].lower()][int(position[1])-2] == '':
                        finalPositions.append(position[0] + str(int(position[1])-1))
                    
                # Check if pawn can capture
                # finding the diagonal squares
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())
                indxLeft = index - 1 if index > 0 else None
                indxRight = index + 1 if index < 7 else None

                if indxLeft is not None and self.layout[keys[indxLeft]][int(position[1]) - 2] in WHITE_PIECES:
                    finalPositions.append(keys[indxLeft] + str(int(position[1]) - 2))
                if indxRight is not None and self.layout[keys[indxRight]][int(position[1]) - 2] in WHITE_PIECES:
                    finalPositions.append(keys[indxRight] + str(int(position[1]) - 2))
            elif piece == 'r':
                # Left/Right axis
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())
                indexLeft = index - 1
                indexRight = index + 1

                while indexLeft >= 0:
                    if self.layout[keys[indexLeft]][int(position[1])-1] == '':
                        finalPositions.append(keys[indexLeft] + str(int(position[1])))
                    elif self.layout[keys[indexLeft]][int(position[1])-1] in WHITE_PIECES:
                        finalPositions.append(keys[indexLeft] + str(int(position[1])))
                        break
                    else:
                        break
                    indexLeft -= 1
                while indexRight <= 7:
                    if self.layout[keys[indexRight]][int(position[1])-1] == '':
                        finalPositions.append(keys[indexRight] + str(int(position[1])))
                    elif self.layout[keys[indexRight]][int(position[1])-1] in WHITE_PIECES:
                        finalPositions.append(keys[indexRight] + str(int(position[1])))
                        break
                    else:
                        break
                    indexRight += 1

                # Up/Down axis
                index = int(position[1]) - 1
                indexUp = index + 1
                indexDown = index - 1

                while indexUp <= 7:
                    if self.layout[position[0].lower()][indexUp] == '':
                        finalPositions.append(position[0] + str(indexUp+1))
                    elif self.layout[position[0].lower()][indexUp] in WHITE_PIECES:
                        finalPositions.append(position[0] + str(indexUp+1))
                        break
                    else:
                        break
                    indexUp += 1
                while indexDown >= 0:
                    if self.layout[position[0].lower()][indexDown] == '':
                        finalPositions.append(position[0] + str(indexDown+1))
                    elif self.layout[position[0].lower()][indexDown] in WHITE_PIECES:
                        finalPositions.append(position[0] + str(indexDown+1))
                        break
                    else:
                        break
                    indexDown -= 1
            elif piece == 'n':
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())

                # 2 up 2 down 
                twoUpIndx = int(position[1]) + 1 if int(position[1]) + 1 <= 7 else None
                twoDownIndx = int(position[1]) - 3 if int(position[1]) - 3 >= 0 else None
                oneLeft = index - 1 if index - 1 >= 0 else None
                oneRight = index + 1 if index + 1 <= 7 else None
                if twoUpIndx:
                    if oneLeft and (self.layout[keys[oneLeft]][twoUpIndx] == '' \
                                    or self.layout[keys[oneLeft]][twoUpIndx] in WHITE_PIECES):
                        finalPositions.append(keys[oneLeft] + str(twoUpIndx+1))
                    if oneRight and (self.layout[keys[oneRight]][twoUpIndx] == '' \
                                    or self.layout[keys[oneRight]][twoUpIndx] in WHITE_PIECES):
                        finalPositions.append(keys[oneRight] + str(twoUpIndx+1))
                if twoDownIndx:
                    if oneLeft and (self.layout[keys[oneLeft]][twoDownIndx] == '' \
                                    or self.layout[keys[oneLeft]][twoDownIndx] in WHITE_PIECES):
                        finalPositions.append(keys[oneLeft] + str(twoDownIndx+1))
                    if oneRight and (self.layout[keys[oneRight]][twoDownIndx] == '' \
                                    or self.layout[keys[oneRight]][twoDownIndx] in WHITE_PIECES):
                        finalPositions.append(keys[oneRight] + str(twoDownIndx+1))

                # 2 left 2 right
                twoLeftIndx = index - 2 if index - 2 >= 0 else None
                twoRightIndx = index + 2 if index + 2 <= 7 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                if twoLeftIndx:
                    if oneUp and (self.layout[keys[twoLeftIndx]][oneUp] == '' \
                                    or self.layout[keys[twoLeftIndx]][oneUp] in WHITE_PIECES):
                        finalPositions.append(keys[twoLeftIndx] + str(oneUp+1))
                    if oneDown and (self.layout[keys[twoLeftIndx]][oneDown] == '' \
                                    or self.layout[keys[twoLeftIndx]][oneDown] in WHITE_PIECES):
                        finalPositions.append(keys[twoLeftIndx] + str(oneDown+1))
                if twoRightIndx:
                    if oneUp and (self.layout[keys[twoRightIndx]][oneUp] == '' \
                                    or self.layout[keys[twoRightIndx]][oneUp] in WHITE_PIECES):
                        finalPositions.append(keys[twoRightIndx] + str(oneUp+1))
                    if oneDown and (self.layout[keys[twoRightIndx]][oneDown] == '' \
                                    or self.layout[keys[twoRightIndx]][oneDown] in WHITE_PIECES):
                        finalPositions.append(keys[twoRightIndx] + str(oneDown+1))
            elif piece == 'b':
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())

                # Upper left diagonal 
                indxLeft = index - 1 if index - 1 >= 0 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                while indxLeft is not None and indxLeft >= 0 and oneUp is not None and oneUp <= 7: 
                    if self.layout[keys[indxLeft]][oneUp] in BLACK_PIECES: 
                        break
                    finalPositions.append(keys[indxLeft] + str(oneUp+1))
                    if self.layout[keys[indxLeft]][oneUp] in WHITE_PIECES:
                        break
                    indxLeft -= 1
                    oneUp += 1

                # Upper right diagonal 
                indxRight = index + 1 if index + 1 <= 7 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                while indxRight is not None and indxRight <= 7 and oneUp is not None and oneUp <= 7: 
                    if self.layout[keys[indxRight]][oneUp] in BLACK_PIECES: 
                        break
                    finalPositions.append(keys[indxRight] + str(oneUp+1))
                    if self.layout[keys[indxRight]][oneUp] in WHITE_PIECES:
                        break
                    indxRight += 1
                    oneUp += 1
                
                # Lower left diagonal 
                indxLeft = index - 1 if index - 1 >= 0 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                while indxLeft is not None and indxLeft >= 0 and oneDown is not None and oneDown >= 0: 
                    if self.layout[keys[indxLeft]][oneDown] in BLACK_PIECES: 
                        break
                    finalPositions.append(keys[indxLeft] + str(oneDown+1))
                    if self.layout[keys[indxLeft]][oneDown] in WHITE_PIECES:
                        break
                    indxLeft -= 1
                    oneDown -= 1

                # Lower right diagonal 
                indxRight = index + 1 if index + 1 <= 7 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                while indxRight is not None and indxRight <= 7 and oneDown is not None and oneDown >= 0: 
                    if self.layout[keys[indxRight]][oneDown] in BLACK_PIECES: 
                        break
                    finalPositions.append(keys[indxRight] + str(oneDown+1))
                    if self.layout[keys[indxRight]][oneDown] in WHITE_PIECES:
                        break
                    indxRight += 1
                    oneDown -= 1
            elif piece == 'q':
                # Left/Right axis
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())
                indexLeft = index - 1
                indexRight = index + 1

                while indexLeft >= 0:
                    if self.layout[keys[indexLeft]][int(position[1])-1] == '':
                        finalPositions.append(keys[indexLeft] + str(int(position[1])))
                    elif self.layout[keys[indexLeft]][int(position[1])-1] in WHITE_PIECES:
                        finalPositions.append(keys[indexLeft] + str(int(position[1])))
                        break
                    else:
                        break
                    indexLeft -= 1
                while indexRight <= 7:
                    if self.layout[keys[indexRight]][int(position[1])-1] == '':
                        finalPositions.append(keys[indexRight] + str(int(position[1])))
                    elif self.layout[keys[indexRight]][int(position[1])-1] in WHITE_PIECES:
                        finalPositions.append(keys[indexRight] + str(int(position[1])))
                        break
                    else:
                        break
                    indexRight += 1

                # Up/Down axis
                index = int(position[1]) - 1
                indexUp = index + 1
                indexDown = index - 1

                while indexUp <= 7:
                    if self.layout[position[0].lower()][indexUp] == '':
                        finalPositions.append(position[0] + str(indexUp+1))
                    elif self.layout[position[0].lower()][indexUp] in WHITE_PIECES:
                        finalPositions.append(position[0] + str(indexUp+1))
                        break
                    else:
                        break
                    indexUp += 1
                while indexDown >= 0:
                    if self.layout[position[0].lower()][indexDown] == '':
                        finalPositions.append(position[0] + str(indexDown+1))
                    elif self.layout[position[0].lower()][indexDown] in WHITE_PIECES:
                        finalPositions.append(position[0] + str(indexDown+1))
                        break
                    else:
                        break
                    indexDown -= 1
                
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())

                # Upper left diagonal 
                indxLeft = index - 1 if index - 1 >= 0 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                while indxLeft is not None and indxLeft >= 0 and oneUp is not None and oneUp <= 7: 
                    if self.layout[keys[indxLeft]][oneUp] in BLACK_PIECES: 
                        break
                    finalPositions.append(keys[indxLeft] + str(oneUp+1))
                    if self.layout[keys[indxLeft]][oneUp] in WHITE_PIECES:
                        break
                    indxLeft -= 1
                    oneUp += 1

                # Upper right diagonal 
                indxRight = index + 1 if index + 1 <= 7 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                while indxRight is not None and indxRight <= 7 and oneUp is not None and oneUp <= 7: 
                    if self.layout[keys[indxRight]][oneUp] in BLACK_PIECES: 
                        break
                    finalPositions.append(keys[indxRight] + str(oneUp+1))
                    if self.layout[keys[indxRight]][oneUp] in WHITE_PIECES:
                        break
                    indxRight += 1
                    oneUp += 1
                
                # Lower left diagonal 
                indxLeft = index - 1 if index - 1 >= 0 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                while indxLeft is not None and indxLeft >= 0 and oneDown is not None and oneDown >= 0: 
                    if self.layout[keys[indxLeft]][oneDown] in BLACK_PIECES: 
                        break
                    finalPositions.append(keys[indxLeft] + str(oneDown+1))
                    if self.layout[keys[indxLeft]][oneDown] in WHITE_PIECES:
                        break
                    indxLeft -= 1
                    oneDown -= 1

                # Lower right diagonal 
                indxRight = index + 1 if index + 1 <= 7 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                while indxRight is not None and indxRight <= 7 and oneDown is not None and oneDown >= 0: 
                    if self.layout[keys[indxRight]][oneDown] in BLACK_PIECES: 
                        break
                    finalPositions.append(keys[indxRight] + str(oneDown+1))
                    if self.layout[keys[indxRight]][oneDown] in WHITE_PIECES:
                        break
                    indxRight += 1
                    oneDown -= 1
            elif piece == 'k':
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())
                left = index - 1 if index - 1 >= 0 else None
                right = index + 1 if index + 1 <= 7 else None
                up = int(position[1]) if int(position[1]) <= 7 else None
                down = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None

                xAxis = [left, index, right]
                yAxis = [down, int(position[1])-1, up]

                finalPositions = [keys[x] + str(y+1) for x in xAxis for y in yAxis if x is not None and y is not None \
                                  and (self.layout[keys[x]][y] == '' or self.layout[keys[x]][y] in WHITE_PIECES) \
                                  and not self.isNewMoveCheck(position, keys[x] + str(y+1))]
                

                # if left and self.layout[keys[left]][int(position[1]) - 1] in WHITE_PIECES or \
                #     self.layout[keys[left]][int(position[1]) - 1] == '' and \
                #         not self.isNewMoveCheck(position, keys[left] + str(int(position[1]))):
                #     finalPositions.append(keys[left] + str(int(position[1])))
                # if right and self.layout[keys[right]][int(position[1]) - 1] in WHITE_PIECES or \
                #     self.layout[keys[right]][int(position[1]) - 1] == '' and \
                #         not self.isNewMoveCheck(position, keys[right] + str(int(position[1]))):
                #     finalPositions.append(keys[right] + str(int(position[1])))
                # if up and self.layout[position[0].lower()][up] in WHITE_PIECES or \
                #     self.layout[position[0].lower()][up] == '' and \
                #         not self.isNewMoveCheck(position, position[0] + str(up+1)):
                #     finalPositions.append(position[0] + str(up+1))
                # if down and self.layout[position[0].lower()][down] in WHITE_PIECES or \
                #     self.layout[position[0].lower()][down] == '' and \
                #         not self.isNewMoveCheck(position, position[0] + str(down+1)):
                #     finalPositions.append(position[0] + str(down+1))
                # Diagonal checks
                # Upper left diagonal
                # if left and up and self.layout[keys[left]][up] not in BLACK_PIECES and \
                #     not self.isNewMoveCheck(position, keys[left] + str(up+1)):
                #     finalPositions.append(keys[left] + str(up+1))
                # # Upper right diagonal
                # if right and up and self.layout[keys[right]][up] not in BLACK_PIECES and \
                #     not self.isNewMoveCheck(position, keys[right] + str(up+1)):
                #     finalPositions.append(keys[right] + str(up+1))
                # # Lower left diagonal
                # if left and down and self.layout[keys[left]][down] not in BLACK_PIECES and \
                #     not self.isNewMoveCheck(position, keys[left] + str(down+1)):
                #     finalPositions.append(keys[left] + str(down+1))
                # # Lower right diagonal
                # if right and down and self.layout[keys[right]][down] not in BLACK_PIECES and \
                #     not self.isNewMoveCheck(position, keys[right] + str(down+1)):
                #     finalPositions.append(keys[right] + str(down+1))
            else:
                pass
        else:  
            # White piece
            if piece == 'P':
                # Check if pawn can move two squares
                if position[1] == '2':
                    if self.layout[position[0].lower()][int(position[1])] == '':
                        finalPositions.append(position[0] + str(int(position[1])+1))
                        if self.layout[position[0].lower()][int(position[1])+1] == '':
                            finalPositions.append(position[0] + str(int(position[1])+2))
                else:
                    if self.layout[position[0].lower()][int(position[1])] == '':
                        finalPositions.append(position[0] + str(int(position[1])+1))
                    
                # Check if pawn can capture
                # finding the diagonal squares
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())
                indxLeft = index - 1 if index > 0 else None
                indxRight = index + 1 if index < 7 else None
                if indxLeft is not None and self.layout[keys[indxLeft]][int(position[1])] in BLACK_PIECES:
                    finalPositions.append(keys[indxLeft] + str(int(position[1]) + 1))
                if indxRight is not None and self.layout[keys[indxRight]][int(position[1])] in BLACK_PIECES:
                    finalPositions.append(keys[indxRight] + str(int(position[1]) + 1))
            elif piece == 'R':
                # Left/Right axis
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())
                indexLeft = index - 1
                indexRight = index + 1

                while indexLeft >= 0:
                    if self.layout[keys[indexLeft]][int(position[1])-1] == '':
                        finalPositions.append(keys[indexLeft] + str(int(position[1])))
                    elif self.layout[keys[indexLeft]][int(position[1])-1] in BLACK_PIECES:
                        finalPositions.append(keys[indexLeft] + str(int(position[1])))
                        break
                    else:
                        break
                    indexLeft -= 1
                while indexRight <= 7:
                    if self.layout[keys[indexRight]][int(position[1])-1] == '':
                        finalPositions.append(keys[indexRight] + str(int(position[1])))
                    elif self.layout[keys[indexRight]][int(position[1])-1] in BLACK_PIECES:
                        finalPositions.append(keys[indexRight] + str(int(position[1])))
                        break
                    else:
                        break
                    indexRight += 1

                # Up/Down axis
                index = int(position[1]) - 1
                indexUp = index + 1
                indexDown = index - 1

                while indexUp <= 7:
                    if self.layout[position[0].lower()][indexUp] == '':
                        finalPositions.append(position[0] + str(indexUp+1))
                    elif self.layout[position[0].lower()][indexUp] in BLACK_PIECES:
                        finalPositions.append(position[0] + str(indexUp+1))
                        break
                    else:
                        break
                    indexUp += 1
                while indexDown >= 0:
                    if self.layout[position[0].lower()][indexDown] == '':
                        finalPositions.append(position[0] + str(indexDown+1))
                    elif self.layout[position[0].lower()][indexDown] in BLACK_PIECES:
                        finalPositions.append(position[0] + str(indexDown+1))
                        break
                    else:
                        break
                    indexDown -= 1
            elif piece == 'N':
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())

                # 2 up 2 down 
                twoUpIndx = int(position[1]) + 1 if int(position[1]) + 1 <= 7 else None
                twoDownIndx = int(position[1]) - 3 if int(position[1]) - 3 >= 0 else None
                oneLeft = index - 1 if index - 1 >= 0 else None
                oneRight = index + 1 if index + 1 <= 7 else None
                if twoUpIndx:
                    if oneLeft and (self.layout[keys[oneLeft]][twoUpIndx] == '' \
                                    or self.layout[keys[oneLeft]][twoUpIndx] in BLACK_PIECES):
                        finalPositions.append(keys[oneLeft] + str(twoUpIndx+1))
                    if oneRight and (self.layout[keys[oneRight]][twoUpIndx] == '' \
                                    or self.layout[keys[oneRight]][twoUpIndx] in BLACK_PIECES):
                        finalPositions.append(keys[oneRight] + str(twoUpIndx+1))
                if twoDownIndx:
                    if oneLeft and (self.layout[keys[oneLeft]][twoDownIndx] == '' \
                                    or self.layout[keys[oneLeft]][twoDownIndx] in BLACK_PIECES):
                        finalPositions.append(keys[oneLeft] + str(twoDownIndx+1))
                    if oneRight and (self.layout[keys[oneRight]][twoDownIndx] == '' \
                                    or self.layout[keys[oneRight]][twoDownIndx] in BLACK_PIECES):
                        finalPositions.append(keys[oneRight] + str(twoDownIndx+1))

                # 2 left 2 right
                twoLeftIndx = index - 2 if index - 2 >= 0 else None
                twoRightIndx = index + 2 if index + 2 <= 7 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                if twoLeftIndx:
                    if oneUp and (self.layout[keys[twoLeftIndx]][oneUp] == '' \
                                    or self.layout[keys[twoLeftIndx]][oneUp] in BLACK_PIECES):
                        finalPositions.append(keys[twoLeftIndx] + str(oneUp+1))
                    if oneDown and (self.layout[keys[twoLeftIndx]][oneDown] == '' \
                                    or self.layout[keys[twoLeftIndx]][oneDown] in BLACK_PIECES):
                        finalPositions.append(keys[twoLeftIndx] + str(oneDown+1))
                if twoRightIndx:
                    if oneUp and (self.layout[keys[twoRightIndx]][oneUp] == '' \
                                    or self.layout[keys[twoRightIndx]][oneUp] in BLACK_PIECES):
                        finalPositions.append(keys[twoRightIndx] + str(oneUp+1))
                    if oneDown and (self.layout[keys[twoRightIndx]][oneDown] == '' \
                                    or self.layout[keys[twoRightIndx]][oneDown] in BLACK_PIECES):
                        finalPositions.append(keys[twoRightIndx] + str(oneDown+1))
            elif piece == 'B':
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())

                # Upper left diagonal 
                indxLeft = index - 1 if index - 1 >= 0 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                while indxLeft is not None and indxLeft >= 0 and oneUp is not None and oneUp <= 7: 
                    if self.layout[keys[indxLeft]][oneUp] in WHITE_PIECES: 
                        break
                    finalPositions.append(keys[indxLeft] + str(oneUp+1))
                    if self.layout[keys[indxLeft]][oneUp] in BLACK_PIECES:
                        break
                    indxLeft -= 1
                    oneUp += 1

                # Upper right diagonal 
                indxRight = index + 1 if index + 1 <= 7 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                while indxRight is not None and indxRight <= 7 and oneUp is not None and oneUp <= 7: 
                    if self.layout[keys[indxRight]][oneUp] in WHITE_PIECES: 
                        break
                    finalPositions.append(keys[indxRight] + str(oneUp+1))
                    if self.layout[keys[indxRight]][oneUp] in BLACK_PIECES:
                        break
                    indxRight += 1
                    oneUp += 1
                
                # Lower left diagonal 
                indxLeft = index - 1 if index - 1 >= 0 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                while indxLeft is not None and indxLeft >= 0 and oneDown is not None and oneDown >= 0: 
                    if self.layout[keys[indxLeft]][oneDown] in WHITE_PIECES: 
                        break
                    finalPositions.append(keys[indxLeft] + str(oneDown+1))
                    if self.layout[keys[indxLeft]][oneDown] in BLACK_PIECES:
                        break
                    indxLeft -= 1
                    oneDown -= 1

                # Lower right diagonal 
                indxRight = index + 1 if index + 1 <= 7 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                while indxRight is not None and indxRight <= 7 and oneDown is not None and oneDown >= 0: 
                    if self.layout[keys[indxRight]][oneDown] in WHITE_PIECES: 
                        break
                    finalPositions.append(keys[indxRight] + str(oneDown+1))
                    if self.layout[keys[indxRight]][oneDown] in BLACK_PIECES:
                        break
                    indxRight += 1
                    oneDown -= 1
            elif piece == 'Q':
                # Left/Right axis
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())
                indexLeft = index - 1
                indexRight = index + 1

                while indexLeft >= 0:
                    if self.layout[keys[indexLeft]][int(position[1])-1] == '':
                        finalPositions.append(keys[indexLeft] + str(int(position[1])))
                    elif self.layout[keys[indexLeft]][int(position[1])-1] in BLACK_PIECES:
                        finalPositions.append(keys[indexLeft] + str(int(position[1])))
                        break
                    else:
                        break
                    indexLeft -= 1
                while indexRight <= 7:
                    if self.layout[keys[indexRight]][int(position[1])-1] == '':
                        finalPositions.append(keys[indexRight] + str(int(position[1])))
                    elif self.layout[keys[indexRight]][int(position[1])-1] in BLACK_PIECES:
                        finalPositions.append(keys[indexRight] + str(int(position[1])))
                        break
                    else:
                        break
                    indexRight += 1

                # Up/Down axis
                index = int(position[1]) - 1
                indexUp = index + 1
                indexDown = index - 1

                while indexUp <= 7:
                    if self.layout[position[0].lower()][indexUp] == '':
                        finalPositions.append(position[0] + str(indexUp+1))
                    elif self.layout[position[0].lower()][indexUp] in BLACK_PIECES:
                        finalPositions.append(position[0] + str(indexUp+1))
                        break
                    else:
                        break
                    indexUp += 1
                while indexDown >= 0:
                    if self.layout[position[0].lower()][indexDown] == '':
                        finalPositions.append(position[0] + str(indexDown+1))
                    elif self.layout[position[0].lower()][indexDown] in BLACK_PIECES:
                        finalPositions.append(position[0] + str(indexDown+1))
                        break
                    else:
                        break
                    indexDown -= 1
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())

                # Upper left diagonal 
                indxLeft = index - 1 if index - 1 >= 0 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                while indxLeft is not None and indxLeft >= 0 and oneUp is not None and oneUp <= 7: 
                    if self.layout[keys[indxLeft]][oneUp] in WHITE_PIECES: 
                        break
                    finalPositions.append(keys[indxLeft] + str(oneUp+1))
                    if self.layout[keys[indxLeft]][oneUp] in BLACK_PIECES:
                        break
                    indxLeft -= 1
                    oneUp += 1

                # Upper right diagonal 
                indxRight = index + 1 if index + 1 <= 7 else None
                oneUp = int(position[1]) if int(position[1]) <= 7 else None
                while indxRight is not None and indxRight <= 7 and oneUp is not None and oneUp <= 7: 
                    if self.layout[keys[indxRight]][oneUp] in WHITE_PIECES: 
                        break
                    finalPositions.append(keys[indxRight] + str(oneUp+1))
                    if self.layout[keys[indxRight]][oneUp] in BLACK_PIECES:
                        break
                    indxRight += 1
                    oneUp += 1
                
                # Lower left diagonal 
                indxLeft = index - 1 if index - 1 >= 0 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                while indxLeft is not None and indxLeft >= 0 and oneDown is not None and oneDown >= 0: 
                    if self.layout[keys[indxLeft]][oneDown] in WHITE_PIECES: 
                        break
                    finalPositions.append(keys[indxLeft] + str(oneDown+1))
                    if self.layout[keys[indxLeft]][oneDown] in BLACK_PIECES:
                        break
                    indxLeft -= 1
                    oneDown -= 1

                # Lower right diagonal 
                indxRight = index + 1 if index + 1 <= 7 else None
                oneDown = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None
                while indxRight is not None and indxRight <= 7 and oneDown is not None and oneDown >= 0: 
                    if self.layout[keys[indxRight]][oneDown] in WHITE_PIECES: 
                        break
                    finalPositions.append(keys[indxRight] + str(oneDown+1))
                    if self.layout[keys[indxRight]][oneDown] in BLACK_PIECES:
                        break
                    indxRight += 1
                    oneDown -= 1
            elif piece == 'K':
                keys = list(self.layout.keys())
                index = keys.index(position[0].lower())
                left = index - 1 if index - 1 >= 0 else None
                right = index + 1 if index + 1 <= 7 else None
                up = int(position[1]) if int(position[1]) <= 7 else None
                down = int(position[1]) - 2 if int(position[1]) - 2 >= 0 else None

                xAxis = [left, index, right]
                yAxis = [down, int(position[1])-1, up]

                finalPositions = [keys[x] + str(y+1) for x in xAxis for y in yAxis if x is not None and y is not None \
                                  and (self.layout[keys[x]][y] == '' or self.layout[keys[x]][y] in BLACK_PIECES) \
                                  and not self.isNewMoveCheck(position, keys[x] + str(y+1))]
            else:
                print("An internal error occured!")
                return 

        for pos in finalPositions:
            if not self.doesMoveBlockCheck(position, pos):
                finalPositions.remove(pos)
        print(finalPositions) 
        return finalPositions
    
    def makeMove(self, pieceToMove, newPosition):
        """
        pieceToMove: position of piece to move in algebraic notation (ex: "a1") 
        newPosition: position to move piece to in algebraic notation

        The move will only be made if it is a legal move. If not, the move will not be made 
        and an error message will be printed to console.
        """
        if self.layout[pieceToMove[0].lower()][int(pieceToMove[1])-1] == '':
            print("No piece to move. Please try again.")
            return

        legalMoves = self.getLegalMoves(pieceToMove)
        newPosition = newPosition[0].lower() + str(newPosition[1])

        if newPosition not in legalMoves:
            print("Illegal move. Please try again.")
            return
        
        if self.layout[pieceToMove[0].lower()][int(pieceToMove[1])-1].islower() and self.blackTurn:
            self.blackTurn = False
            self.whiteTurn = True
        elif self.layout[pieceToMove[0].lower()][int(pieceToMove[1])-1].isupper() and self.whiteTurn:
            self.whiteTurn = False
            self.blackTurn = True
        else:
            print("Not your turn. Please try again.")
            return

        oldPiece = self.layout[newPosition[0].lower()][int(newPosition[1])-1]
        
        # Make move 
        self.layout[newPosition[0].lower()][int(newPosition[1])-1] = self.layout[pieceToMove[0].lower()][int(pieceToMove[1])-1]
        self.layout[pieceToMove[0].lower()][int(pieceToMove[1])-1] = ''

        pieceDict = {
            'p': 'Pawn',
            'r': 'Rook',
            'n': 'Knight',
            'b': 'Bishop',
            'q': 'Queen',
            'k': 'King',
        }

        if oldPiece != '':
            if oldPiece.islower():
                print(f"White captured a black {pieceDict[oldPiece]}!")
                self.whiteCaptured.append(oldPiece)
            else:
                print(f"Black captured a white {pieceDict[oldPiece.lower()]}!")
                self.blackCaptured.append(oldPiece)
    
    def restartGame(self):
        self.layout = {
            "a": ['R', 'P', '', '', '', '', 'p', 'r'],
            "b": ['N', 'P', '', '', '', '', 'p', 'n'],
            "c": ['B', 'P', '', '', '', '', 'p', 'b'],
            "d": ['Q', 'P', '', '', '', '', 'p', 'q'],
            "e": ['K', 'P', '', '', '', '', 'p', 'k'],
            "f": ['B', 'P', '', '', '', '', 'p', 'b'],
            "g": ['N', 'P', '', '', '', '', 'p', 'n'],
            "h": ['R', 'P', '', '', '', '', 'p', 'r'],
        }

        self.whiteTurn = True
        self.blackTurn = False

        self.whiteCaptured = []
        self.blackCaptured = []

    def getBoardLayout(self):
        return self.layout
    
    def getPieceAtPosition(self, position):
        return self.layout[position[0].lower()][int(position[1])-1]
    
    def getTurn(self):
        if self.whiteTurn:
            return "White"
        else:
            return "Black"
        
    def getKingPosition(self, color):
        for letter in self.layout.keys():
            for rank in range(8):
                if self.layout[letter][rank] == 'k' and color == 'Black':
                    return letter + str(rank+1)
                if self.layout[letter][rank] == 'K' and color == 'White':
                    return letter + str(rank+1) 
        return None

    def getKingCheckStatus(self, color):
        if color == 'Black':
            return self.blackIsChecked
        else:
            return self.whiteIsChecked

    def printGame(self):
        print("  a b c d e f g h")
        for i in range(7, -1, -1):
            print(f"{i+1}", end=" ")
            for key in self.layout.keys():
                if self.layout[key][i] == '':
                    print("  ", end="")
                else:
                    print(self.layout[key][i] + " ", end="")
            print()

        print(f"White captured: {self.whiteCaptured}")
        print(f"Black captured: {self.blackCaptured}")
        print("+-----------------+")