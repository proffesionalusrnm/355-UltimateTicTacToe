#!/usr/bin/env python3
import pygame
import time
import sys
import time
from Objects import board
from Objects import uttt_solver as solver


# constants
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 600

#initialize game window and board
pygame.init()
gameBoard = board.Board(False)
gameSolver = solver.Solver()
font = pygame.font.SysFont('comicsansms', 25)

# Create a game window
game_window = pygame.display.set_mode((gameBoard.WINDOW_WIDTH, gameBoard.WINDOW_HEIGHT + 50))
game_window.fill((255,255,255))
pygame.display.set_caption("Ultimate Tic Tac Toe")

# function to highlight the next move to play
def displayNextMove(X, Y):
    gameBoard.drawEdges(pygame,game_window)
    if (gameBoard.nextPlay != 9):
        rect = pygame.Rect((X % 3) * (WINDOW_WIDTH/3) , (Y % 3) * (WINDOW_HEIGHT/3), WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3)
        pygame.draw.rect(game_window, (0,255,255), rect, 2)

# function to display the guide for the player
def displayGuide(player):
    game_window.fill((255,255,255), (0, WINDOW_HEIGHT+10, WINDOW_WIDTH, 50))

    if (gameBoard.nextPlay != 9):
        guide = font.render("Player " + player + " can play in the highlighted board!", True, (0,0,0), (255,255,255))
        game_window.blit(guide, (70, WINDOW_HEIGHT + 10))

    else:
        guide = font.render("Player " + player + " can play anywhere!", True, (0,0,0), (255,255,255)) 
        game_window.blit(guide, (150, WINDOW_HEIGHT + 10))


# function to display the result after the game is finished
def displayResult():
    gameBoard.drawEdges(pygame,game_window)
    game_window.fill((255,255,255), (0, WINDOW_HEIGHT+10, WINDOW_WIDTH, 50))

    if (gameBoard.getWinner != 'D'):
        winner = font.render("Congratulation, Player " + gameBoard.getWinner + " wins the game!", True, (0,0,0))
        game_window.blit(winner, (70, WINDOW_HEIGHT + 10))
    else:
        winner = font.render("This game is a draw!", True, (0,0,0))
        game_window.blit(winner, (175, WINDOW_HEIGHT + 10))

def main(usingSolver):

    game_running = True

    #initialize player
    player = 'X'

    gameBoard.displayBoard(pygame,game_window) # display the board

    # Game loop
    while game_running:
        BigBoardFinished = gameBoard.gameFinished
        if (BigBoardFinished):
            displayResult()
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
                        if (not gameBoard.gameFinished):
                            displayGuide(player)
                            displayNextMove(newX, newY)
                        pygame.display.update()
                        if(usingSolver):
                            try:
                                pygame.time.wait(800)
                                moveX, moveY = gameSolver.step(gameBoard, player, pygame, game_window)
                                player = 'X' if player == 'O' else 'O'
                                if (not gameBoard.gameFinished):
                                    displayGuide(player)
                                    displayNextMove(moveX, moveY)
                                pygame.display.update()
                            except Exception:
                                continue
                    else:
                        print("Illegal move, try again")


        # update display
        pygame.display.update()



if __name__ == '__main__':

        if len(sys.argv) > 1:
            print("You are playing against another person")
            main(False)
        elif not len(sys.argv) > 1:
            print("You are playing against our solver")
            main(True)
        else:
            print("You are playing against our solver")
            main(True)
