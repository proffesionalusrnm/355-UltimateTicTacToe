#!/usr/bin/env python3
import pygame
import time
import sys
from Objects import board
from Objects import uttt_solver as solver
#initialize game window and board
pygame.init()
gameBoard = board.Board(False)
gameSolver = solver.Solver()

def main(usingSolver):
    # Create a game window
    game_window = pygame.display.set_mode((gameBoard.WINDOW_WIDTH, gameBoard.WINDOW_HEIGHT))
    game_window.fill((255,255,255))
    game_running = True
    pygame.display.set_caption("Ultimate Tic Tac Toe")
    #initialize player
    player = 'X'
    # Game loop
    gameBoard.displayBoard(pygame,game_window)
    while game_running:
        # Loop through all active events
        for event in pygame.event.get():
            # Close the program if the user presses the 'X'
            if event.type == pygame.QUIT:
                game_running = False
                # Uninitialize all pygame modules and quit the program
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = event.pos
                    newX,newY = gameBoard.getXYFromUser(x,y)
                    if gameBoard.fullPlay(newX,newY,player,pygame,game_window):
                        player = 'X' if player == 'O' else 'O'
                        if(usingSolver):
                            gameSolver.step(gameBoard, player, pygame, game_window)
                            player = 'X' if player == 'O' else 'O'
                    else:
                        print("Illegal move, try again")


        # Update our display
        pygame.display.update()

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        if arg=="t":
            main(True)
            print("You are playing against our solver")
        else:
            main(False)
            print("You are playing against another person")
