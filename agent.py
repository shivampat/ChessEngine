from board import Board, coordsToAlgebraic

class MinimaxAgent:
    def __init__(self, depth, board, whichPlayer, heuristic):
        self.depth = depth
        self.board = board 
        self.player = "white" if whichPlayer == 1 else "black"
        self.enemy = "black" if whichPlayer == 1 else "white"
        self.heuristic = heuristic
        self.pieceValue = {
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 9,
            "K": 100
        }
    
    # def getBestMove(self):
    #     bestMove = None
    #     bestEval = float('-inf')
    #     for start in self.board.getAllLegalMoves(self.player):
    #         for move in self.board.getAllLegalMoves(self.player)[start]:
    #             newBoard = self.board.copy()
    #             newBoard.makeMove(start, move)
    #             eval = self.minimax(newBoard, self.depth - 1, False)
    #             if eval > bestEval:
    #                 bestEval = eval
    #                 bestMove = (start, move)
    #     return bestMove
    
    def getBestMove(self):
        """
        Best move
        (TEST): Only depth of 1
        """
        if self.player != self.board.getTurn().lower():
            print("Not your turn.")
            return None
        
        bestMove = None 
        bestHeuristicValue = float('-inf')
        for start in self.board.getAllLegalMoves(self.player):
            for move in self.board.getAllLegalMoves(self.player)[start]:
                newBoard = self.board.copy()
                newBoard.makeMove(start, move)
                newBoard.printBoard()
                # currentHeuristicValue = self.heuristic(newBoard, self.player, self.pieceValue)
                currentHeuristicValue = self.minimax(newBoard, self.depth - 1, False)
                if currentHeuristicValue > bestHeuristicValue:
                    bestHeuristicValue = currentHeuristicValue
                    bestMove = (start, move)
        
        print(bestMove, bestHeuristicValue)
        return bestMove
                
    def minimax(self, board, depth, maximizingPlayer):
        # if depth == 0 or board.isCheckmate("white") or board.isCheckmate("black") or board.isStalemate("white") or board.isStalemate("black"):
        if depth == 0:
            return self.heuristic(board, self.player, self.pieceValue)
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for start in board.getAllLegalMoves(self.player):
                for move in board.getAllLegalMoves(self.player)[start]:
                    newBoard = board.copy()
                    newBoard.makeMove(start, move)
                    minimax_eval = self.minimax(newBoard, depth - 1, False)
                    maxEval = max(maxEval, minimax_eval)
            return maxEval
        else:
            minEval = float('inf')
            for start in board.getAllLegalMoves(self.enemy):
                for move in board.getAllLegalMoves(self.enemy)[start]:
                    newBoard = board.copy()
                    newBoard.makeMove(start, move)
                    minimax_eval = self.minimax(newBoard, depth - 1, False)
                    minEval = min(minEval, minimax_eval)
            return minEval 

def underAttackHeuristic(board, agentColor, pieceValue):
    """
    This heuristic will return a score based on how many pieces are under attack. 
    """
    # Enemy piece lists
    enemyColor = 'black' if agentColor == 'white' else 'white'
    enemyRookAndQueen = ['r', 'q'] if agentColor == 'white' else ['R', 'Q']
    enemyBishopAndQueen = ['b', 'q'] if agentColor == 'white' else ['B', 'Q']
    enemyKnight = 'n' if agentColor == 'white' else 'N'
    enemyKing = 'k' if agentColor == 'white' else 'K'
    enemyPawn = 'p' if agentColor == 'white' else 'P'
    enemyPawnMoves = [(1, 1), (-1, 1)] if agentColor == 'black' else [(1, -1), (-1, -1)]
    
    score = 0
    
    if board.getTurn().lower() == agentColor and board.isCheckmate() or board.isStalemate():
        return float('-inf')
    elif board.getTurn().lower() == enemyColor and board.isCheckmate():
        return float('inf')
     
    for col in board.pieces:
        for piece in col:
            if piece is not None and piece.color == agentColor:
                horizAndVertMoves = piece.getHorizontals() + piece.getVerticals()
                for pos in horizAndVertMoves:
                    if board.getPieceType(pos) is not None and board.getPieceType(pos).color != agentColor \
                        and board.getPieceType(pos).piece in enemyRookAndQueen:
                        score -= pieceValue[piece.piece.upper()]*100
                for pos in piece.getDiagonals():
                    if board.getPieceType(pos) is not None and board.getPieceType(pos).color != agentColor \
                        and board.getPieceType(pos).piece in enemyBishopAndQueen:
                        score -= pieceValue[piece.piece.upper()]*100
                for pos in piece.getKnightMoves():
                    if board.getPieceType(pos) is not None and board.getPieceType(pos).color != agentColor \
                        and board.getPieceType(pos).piece == enemyKnight:
                        score -= pieceValue[piece.piece.upper()]*100
                for pos in piece.getKingMoves():
                    if board.getPieceType(pos) is not None and board.getPieceType(pos).color != agentColor \
                        and board.getPieceType(pos).piece == enemyKing:
                        score -= pieceValue[piece.piece.upper()]*100
                for move in enemyPawnMoves:
                    if piece.x + move[0] >= 0 and piece.x + move[0] < 8 and piece.y + move[1] >= 0 and piece.y + move[1] < 8:
                        if board.getPieceType((piece.x + move[0], piece.y + move[1])) is not None and board.getPieceType((piece.x + move[0], piece.y + move[1])).color != agentColor \
                            and board.getPieceType((piece.x + move[0], piece.y + move[1])).piece == enemyPawn:
                            score -= pieceValue[piece.piece.upper()]*100
    
    return score             

fen = "r1bqk2r/pppp1ppp/5n2/2b5/2Bp1B2/2N1P3/PPP2PPP/R2QK2R b KQkq - 2 7"
board = Board(fen=fen)
board.printBoard()
agent = MinimaxAgent(2, board, 2, underAttackHeuristic)
# print(agent.heuristic(board, "black", agent.pieceValue))
move = agent.getBestMove()
for pos in move: 
    print(coordsToAlgebraic(pos), end=" -> ")
print()