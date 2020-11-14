import numpy as np
import math
import random

class Solver:
    def __init__(self):
        print("Solver Initialized")

    def step(self, board, player, pygame, game_window):
        # TODO: Random Legal Move Selection
        # Simple solution: game is 9x9 grid = 81 spaces
        # Pick random number 0 - 80, tie it to a position
        # If it's a legal move, do it 
        # If not, increment by one and try again (looping to 0 once you hit 80)
        # If you return to your original number, break (board is filled)
        if (board.gameFinished):
            if (board.getWinner == 'D'):
                print("GAME OVER - DRAW");
            else:
                print(">> GAME OVER - WINNER: " + board.getWinner)
            return
        randpos = random.randint(0,80)
        for offset in range(81):
            currpos = ((randpos + offset) % 81)
            movex, movey = self.postomove(currpos)
            #print(f"{currpos} -> [{movex}, {movey}]")
            if board.isMoveLegal(movey, movex):
                board.playMove(movey, movex, player)
                board.displayMove(movex, movey, player, pygame, game_window)
                break

    def postomove(self, pos):
        return pos%9, math.floor(pos/9)