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

        self.PGN = "" if pgn is None else pgn

    
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
                pass
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
                pass
            else:
                pass
        
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

        if oldPiece != '':
            if oldPiece.islower():
                self.whiteCaptured.append(oldPiece)
            else:
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
