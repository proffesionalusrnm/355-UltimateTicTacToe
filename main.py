#!/usr/bin/env python3
import pygame
import time
import sys
from Objects import board
from Objects.heuristic_solver import Solver
from Objects.uttt_solver import Solver as RandomSolver


# constants
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 600

# initialize game window and board
pygame.init()
gameBoard = board.Board(False)
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

# function to handle display action
def displayController(x, y, player, finished):
    if (not finished):
        displayGuide(player)
        displayNextMove(x, y)
    else:
        displayResult()

def main(mode):
    if mode == 'solver' or mode == 'solvers':
        gameSolver = Solver()
    if mode == 'random' or mode == 'solvers':
        randomSolver = RandomSolver()
    
    game_running = True
    lastToPlay = 'random'

    #initialize player
    player = 'X'

    gameBoard.displayBoard(pygame,game_window) # display the board
    displayGuide(player)

    # Game loop
    while game_running:
        # Play the two solvers against each other
        if mode == 'solvers':
            for event in pygame.event.get():
                # Close the program if the user presses the 'X'
                if event.type == pygame.QUIT:
                    game_running = False
                    # Uninitialize all pygame modules and quit the program
                    pygame.quit()
                    sys.exit()
            pygame.time.wait(800)
            if lastToPlay == 'random':
                moveX, moveY = gameSolver.step(gameBoard, player)
            else:
                moveX, moveY = randomSolver.step(gameBoard, player)
            gameBoard.fullPlay(moveX,moveY,player,pygame,game_window)
            player = 'X' if player == 'O' else 'O'
            displayController(moveX, moveY, player, gameBoard.gameFinished)
            pygame.display.update()
            lastToPlay = 'solver' if lastToPlay == 'random' else 'random'
            game_running = not gameBoard.gameFinished
            continue
            
        # Play against solver or random solver or another player
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
                        displayController(newX, newY, player, gameBoard.gameFinished)
                        pygame.display.update()
                        if gameBoard.gameFinished:
                            game_running = False
                            break
                        if(mode != 'player'):
                            pygame.time.wait(800)
                            if mode == 'random':
                                moveX, moveY = randomSolver.step(gameBoard, player)
                            else:
                                moveX, moveY = gameSolver.step(gameBoard, player)
                            gameBoard.fullPlay(moveX,moveY,player,pygame,game_window)
                            player = 'X' if player == 'O' else 'O'
                            displayController(moveX, moveY, player, gameBoard.gameFinished)
                            pygame.display.update()
                            if gameBoard.gameFinished:
                                game_running = False
                                break
                    else:
                        print("Illegal move, try again")


        # update display
        pygame.display.update()
    
    # Wait for user to end the program
    waitingForExit = True
    while waitingForExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                # Uninitialize all pygame modules and quit the program
                pygame.quit()
                sys.exit() 



if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'player':
            main('player')
        elif sys.argv[1] == 'random':
            main('random')
        elif sys.argv[1] == 'solvers':
            main('solvers')
        else:
            print("Correct arguments: player, random, solvers")
    else:
        main('solver')
