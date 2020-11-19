import numpy as np
import math
import random

class Solver:
    def __init__(self):
        print("Solver Initialized")
    
    def step(self, board, player, pygame, game_window):
        if (board.gameFinished):
            if (board.getWinner == 'D'):
                print(">> GAME OVER - DRAW");
            else:
                print(">> GAME OVER - WINNER: " + board.getWinner)
            return
        self.randMove(board, player, pygame, game_window)
    
    # Random Legal move selection
    def randMove(self, board, player, pygame, game_window):
        if (board.nextPlay == 9): # Play anywhere
            randpos = random.randint(0,80)
            for offset in range(81):
                currpos = ((randpos + offset) % 81)
                movex, movey = self.valToMove(currpos, board, False)
                # print(f"ANY CELL: {currpos} -> [{movex}, {movey}]")
                if board.fullPlay(movex, movey, player, pygame, game_window):
                    return
        else: # Play within allowed cell
            randpos = random.randint(0,8)
            for offset in range(9):
                currpos = ((randpos + offset) % 9)
                movex, movey = self.valToMove(currpos, board, True)
                # print(f"CELL {board.nextPlay}: {currpos} -> [{movex}, {movey}]")
                if board.fullPlay(movex, movey, player, pygame, game_window):
                    return
        print("Failed to find")

    def valToMove(self, pos, board, inner):
        if (inner):
            return (pos%3 + 3*(board.nextPlay%3)), (math.floor(pos/3) + 3*(math.floor(board.nextPlay/3)))
        else:
            return pos%9, math.floor(pos/9)
        
    def ABminimax(self, depth, board, player, move, a, b):
        # Need some temporary representations of the board object
        return