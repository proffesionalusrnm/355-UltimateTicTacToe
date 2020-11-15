#!/usr/bin/env python3
import pygame
import sys
from Objects import board
from Objects import uttt_solver as solver
#initialize game window and board
pygame.init()
gameBoard = board.Board(False)
gameSolver = solver.Solver()

def main():
    # Create a game window
    game_window = pygame.display.set_mode((gameBoard.WINDOW_WIDTH, gameBoard.WINDOW_HEIGHT))
    game_window.fill((255,255,255))
    game_running = True
    pygame.display.set_caption("Ultimate Tic Tac Toe")
    
    #initialize player
    player = 'X'
    freeMove = True # can move anywhere on the board

    gameBoard.displayBoard(pygame,game_window) # display the board

    # Game loop
    while game_running:
        BigBoardFinished = gameBoard.gameFinished
        if (BigBoardFinished):
            game_running = False
            print("Congratulation, Player " + gameBoard.getWinner + " wins the game!")
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
                    currentBoard = gameBoard.checkCurentPos(newX,newY) # current position of the player
                    InnerBoardFinished = gameBoard.grid[int(newY/3), int(newX/3)].gameFinished # status of the inner board
                    if freeMove: # can move anywhere on the board
                        # play the game 
                        if (gameBoard.isMoveLegal(newY,newX) and not InnerBoardFinished):
                            gameBoard.playMove(newY,newX,player)
                            gameBoard.displayMove(newX,newY,player,pygame,game_window)
                            finished = gameBoard.gameFinished
                            if player=='X':
                                player ='O'
                            elif player=='O':
                                player ='X'
                            freeMove = False
                            # store next board position to play next turn
                            nextBoard = gameBoard.checkPreviousMove(newX, newY)
                        elif (not gameBoard.isMoveLegal(newY,newX) and not InnerBoardFinished):
                            print("Illegal move, try again")
                        elif (not gameBoard.isMoveLegal(newY,newX) and InnerBoardFinished):
                            print("This board is finished, please play at another board")
                            freeMove = True

                    else: # must move according to the rule
                        # check for validity
                        if (currentBoard != nextBoard):
                            print("You are not playing in the correct board, try again")
                        elif (currentBoard == nextBoard and not InnerBoardFinished):
                            # play the game
                            if (gameBoard.isMoveLegal(newY, newX)):
                                gameBoard.playMove(newY,newX,player)
                                gameBoard.displayMove(newX,newY,player,pygame,game_window)
                                if player=='X':
                                    player ='O'
                                elif player=='O':
                                    player ='X'
                                # store next board position to play next turn
                                nextBoard = gameBoard.checkPreviousMove(newX, newY)
                            elif (not gameBoard.isMoveLegal(newY, newX) and not InnerBoardFinished):
                                print("Illegal move, try again")
                        elif (currentBoard == nextBoard and InnerBoardFinished):
                            print("This board is finished, please play at another board")
                            freeMove = True

                elif event.button == 3: #right mouse button
                    gameSolver.step(gameBoard, player, pygame, game_window)
                    player = 'X' if player == 'O' else 'O'

        # Update our display
        pygame.display.update()



if __name__ == '__main__':
    main()
