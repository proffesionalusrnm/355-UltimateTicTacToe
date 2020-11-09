#!/usr/bin/env python3
import pygame
import sys
from Objects import board
#initialize game window and board
pygame.init()
gameBoard = board.Board()



def main():
    # Create a game window
    game_window = pygame.display.set_mode((gameBoard.WINDOW_WIDTH, gameBoard.WINDOW_HEIGHT))
    game_window.fill((255,255,255))
    game_running = True
    pygame.display.set_caption("Ultimate Tic Tac Toe")

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
                    i,j = gameBoard.getPositionForGrid(x,y)
                    ##call check if move is legal here

                    #print move to terminal for reference
                    print("Current move:",i,j)
                    
                    ##if move is legal then place move
                    gameBoard.setPostionInGrid(i,j,"X",pygame,game_window)
                    ##call check if win here


        # Update our display
        pygame.display.update()



if __name__ == '__main__':
    main()
