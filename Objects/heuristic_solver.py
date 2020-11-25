import numpy as np
import math
import random
from copy import deepcopy


class Solver:
    """Minimax with fixed depth solver for UTTT
    
    This solver implements minimax on the Ultimate Tic Tac Toe
    board. However, since the state space is too large for UTTT,
    we use minimax for 2 depths or iterations and then use a
    heuristic value for future depths. This idea is from the following
    source:
    https://www.cs.huji.ac.il/~ai/projects/2013/UlitmateTic-Tac-Toe/
    The heuristic used is h1 from the above source
    
    Attributes:
        maxDepth (int): Maximum depth of minimax (default 2)
        DEBUG (bool): If True, prints debug log to console 
    """
    def __init__(self):
        self.maxDepth = 2
        self.DEBUG = False
        print("Minimax Solver Initialized. Max depth: ", self.maxDepth)
        
    def step(self, board, player):
        """Get the next best move for this player
        
        Args:
            board: Board object from Objects.board
            player: Player to get the best move for
        
        Returns: Tuple of (moveX, moveY) that represents
            the next best move
        """
        sc, mv = self.minimax(board, player)
        return mv
    
    def minimax(self, board, player, maxim=True, depth=0):
        """Get minimax value
        
        Args:
            board: Board object from Objects.board
            player: Player to get the best move for
            maxim: Whether we are maximizing or minimizing
            depth: Minimax tree depth
        
        Returns: Tuple of (score, move) that represents
            the best score and best move. Move is the
            tuple (moveX, moveY) described above
        """
        if maxim:
            currPlayer = player
        else:
            currPlayer = 'X' if player == 'O' else 'O'
        if depth >= self.maxDepth:
            return self._heuristic(board, player), None
        legalMoves = self._getLegalMoves(board)
        if (legalMoves == []):
            return self._heuristic(board, player), None
        bestMoves = None
        if maxim:
            bestScore = float('-inf')
        else:
            bestScore = float('inf')
        if self.DEBUG: print("Legal moves: ", legalMoves)
        for move in legalMoves:
            if self.DEBUG: print("Playing in cell: ", move, " at depth: ", depth)
            copyBoard = deepcopy(board)
            copyBoard.shouldPrint = False
            copyBoard.playMove(move[1], move[0], currPlayer)
            sc, _ = self.minimax(copyBoard, player, not maxim, depth + 1)
            if self.DEBUG: print("Score in that cell: ", sc)
            if maxim:
                if sc > bestScore:
                    bestScore = sc
                    bestMoves = [move]
                elif sc == bestScore:
                    bestMoves.append(move)
            else:
                if sc < bestScore:
                    bestScore = sc
                    bestMoves = [move]
                elif sc == bestScore:
                    bestMoves.append(move)
        if self.DEBUG: print("Best Moves: ", bestMoves, "\nBestScore", bestScore)
        return bestScore, bestMoves[np.random.randint(len(bestMoves))]
    
    def _getLegalMoves(self, board):
        legalMoves = []
        for i in range(9):
            for j in range(9):
                if board.isMoveLegal(j, i):
                    legalMoves.append((i, j))
        return legalMoves

    def _heuristic(self, board, player):
        if board.getWinner == player:
            return 10000
        elif board.getWinner == 'O' or board.getWinner == 'X':
            return -10000
        
        score = 0
        for i in range(3):
            for j in range(3):
                if board.grid[i][j].getWinner == player:
                    score = score + 1
                elif board.grid[i][j].getWinner == 'O' or board.getWinner == 'X':
                    score = score - 1
        return score

