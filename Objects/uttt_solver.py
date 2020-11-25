import numpy as np
import math
import random

class Solver:
    def __init__(self):
        print("Random Solver Initialized")
    
    def step(self, board, player):
        if (board.gameFinished):
            if (board.getWinner == 'D'):
                print(">> GAME OVER - DRAW");
            else:
                print(">> GAME OVER - WINNER: " + board.getWinner)
        return self.randMove(board)
        
    # Random Legal move selection
    def randMove(self, board):
        if (board.nextPlay == 9): # Play anywhere
            randpos = random.randint(0,80)
            for offset in range(81):
                currpos = ((randpos + offset) % 81)
                movex, movey = self.valToMove(currpos, board, False)
                # print(f"ANY CELL: {currpos} -> [{movex}, {movey}]")
                if board.isMoveLegal(movey, movex):
                    return movex,movey
        else: # Play within allowed cell
            randpos = random.randint(0,8)
            for offset in range(9):
                currpos = ((randpos + offset) % 9)
                movex, movey = self.valToMove(currpos, board, True)
                # print(f"CELL {board.nextPlay}: {currpos} -> [{movex}, {movey}]")
                if board.isMoveLegal(movey, movex):
                    return movex, movey
        print("Failed to find")
        return

    def valToMove(self, pos, board, inner):
        if (inner):
            return (pos%3 + 3*(board.nextPlay%3)), (math.floor(pos/3) + 3*(math.floor(board.nextPlay/3)))
        else:
            return pos%9, math.floor(pos/9)

