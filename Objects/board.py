import numpy as np
import math

class Board:
    """A single board of Tic-Tac-Toe

    Each tile is either another SingleBoard instance or a single character value.
    Single values can be '' for empty, 'D' for draw, 'O' for player 1, 'X' for player 2.
    This class must be initialized with argument False.

    Example:
        myboard = SingleBoard(False)
        if (myboard.isMoveLegal(0, 0)):
            myboard.playMove(0, 0, 'X')

        # Play some more

        if (myboard.gameFinished):
            winner = myboard.getWinner
            if (winner = 'D'):
                print("Game was drawed :(")
            else:
                print(winner, "won!")

    Args:
        innerGrid (bool): Whether the board is a single tic-tac-toe board or the Ultimate
            board. This class must always be initialized with the False argument

    Attributes:
        isInnerGrid (bool): True if board tiles are single values, false otherwise
        gameFinished (bool): True if game has ended as either a win, lose or draw
        getWinner (str): '' if the game has not yet ended, 'D' if the game has drawed,
            'O' or 'X' otherwise
    """


    def __init__(self, innerGrid, shouldPrint=True):
        self.isInnerGrid = innerGrid
        self.gameFinished = False
        self.getWinner = ''
        self.rows = 9
        self.WINDOW_HEIGHT = 700
        self.WINDOW_WIDTH = 600
        self.shouldPrint = shouldPrint
        if innerGrid:
            self.grid = np.full((3, 3), '') # Initialize board with empty value
        else:
            self.grid = np.array([[Board(True) for i in range(3)] for j in range(3)])  # Initialize board with empty boards
            self.nextPlay = 9

    def displayBoard(self, pg, window):
        for row in self.grid:
           gridToPrint =str(row[0].grid)+str(row[1].grid)+str(row[2].grid)
           print(gridToPrint.replace("\n",""))

        smallWidth= self.WINDOW_WIDTH / self.rows
        smallHeight=self.WINDOW_HEIGHT / self.rows


        #loop to make small tic tac toe boards
        for i in range(self.rows):
           #print vertical lines
           pg.draw.line(window,(165,167,182),[smallWidth+smallWidth*i,0],[smallWidth+smallWidth*i,self.WINDOW_HEIGHT],2)
           #print horizontal lines
           pg.draw.line(window,(165,167,182),[0,smallHeight+smallHeight*i],[self.WINDOW_WIDTH,smallHeight+smallHeight*i],2)

        # Make large tic tac to board on top
        self.drawEdges(pg, window)

    # function to draw the edges of the big board
    # input: pygame and the game window
    def drawEdges(self, pg, window):
        pg.draw.line(window,(0,0,0),[0,0],[self.WINDOW_WIDTH,0],5) # top edge
        pg.draw.line(window,(0,0,0),[0,self.WINDOW_HEIGHT],[self.WINDOW_WIDTH,self.WINDOW_HEIGHT],5) # bottom edge
        pg.draw.line(window,(0,0,0),[0,0],[0,self.WINDOW_HEIGHT],5) # right edge
        pg.draw.line(window,(0,0,0),[self.WINDOW_WIDTH, 0],[self.WINDOW_WIDTH,self.WINDOW_HEIGHT],5) # left edge
        pg.draw.line(window,(0,0,0),[0,self.WINDOW_HEIGHT//3],[self.WINDOW_WIDTH,self.WINDOW_HEIGHT//3],3)
        pg.draw.line(window,(0,0,0),[self.WINDOW_WIDTH//3,0],[self.WINDOW_WIDTH//3,self.WINDOW_HEIGHT],3)
        pg.draw.line(window,(0,0,0),[0,self.WINDOW_HEIGHT*2//3],[self.WINDOW_WIDTH,self.WINDOW_HEIGHT*2//3],3)
        pg.draw.line(window,(0,0,0),[self.WINDOW_WIDTH*2//3,0],[self.WINDOW_WIDTH*2//3,self.WINDOW_HEIGHT],3)

    def fullPlay(self, x, y, player, pygame, screen):
        # Checks if the move is legal, if it is, play and display it
        if (self.isMoveLegal(y, x)):
            self.playMove(y, x, player)
            self.displayMove(x, y, player, pygame, screen)
            return True
        else: 
            return False

    def isMoveLegal(self, i, j):
        """Whether the given move is legal or not

        Note: For the Ultimate Tic Tac Toe board (UTTT), i and j must be
            between 0 and 8 inclusive. For the normal board, i and j must be
            between 0 and 2 inclusive.

        Args:
            i (int): y-value from top left corner of board
            j (int): x-value from top left corner of board

        Returns:
            True if move is legal, False otherwise
        """
        if self.gameFinished:
            return False    # Move illegal if board is complete
        if self.isInnerGrid:
            # Check if cell is unoccupied
            if self.grid[i, j] != '':
                return False    # Cell occupied
            else:
                return True     # Empty cell
        else:
            # Compute i, j values for child board and call isMoveLegal
            parentI = int(i / 3)    # i, j values to access this board
            parentJ = int(j / 3)
            if (self.nextPlay != 9 and self.nextPlay != parentI * 3 + parentJ):
                return False
            innerI = i % 3    # i, j values to access child board
            innerJ = j % 3
            return self.grid[parentI, parentJ].isMoveLegal(innerI, innerJ)

    def playMove(self, i, j, player):
        """Plays the move on the board

        Plays the move on the board and sets the gameFinished and getWinner
        attributes of the class appropriately.

        Note: For the Ultimate Tic Tac Toe board (UTTT), i and j must be
            between 0 and 8 inclusive. For the normal board, i and j must be
            between 0 and 2 inclusive.

        Args:
            i (int): y-value from top left corner of board
            j (int): x-value from top left corner of board
            player (str): 'O' or 'X' for the player to move
        """
        if self.isInnerGrid:
            self.grid[i, j] = player
        else:
            parentI = int(i / 3)    # i, j values to access this board
            parentJ = int(j / 3)
            innerI = i % 3    # i, j values to access child board
            innerJ = j % 3
            self.grid[parentI, parentJ].playMove(innerI, innerJ, player)
            if (self.grid[innerI, innerJ].gameFinished):
                self.nextPlay = 9
            else:
                self.nextPlay = innerI * 3 + innerJ
            if self.shouldPrint: print(f"{'X' if player == 'O' else 'O'} to play {f'in cell {self.nextPlay}' if (self.nextPlay < 9) else 'anywhere'}")

        self.gameFinished, self.getWinner = self.hasGameFinished()

    def hasGameFinished(self):
        """Checks if this board is complete

        Returns:
            A tuple of (bool, str) is always returned. If the board is complete (win,
                lose or draw), the bool value is True and the str value has the winning
                player value or 'D' if the game is drawed. Otherwise, the bool value is
                False and the str value is empty ('')
        """
        if self.isInnerGrid:
            board = self.grid
        else:
            board = np.array([[j.getWinner for j in i] for i in self.grid])
        # Compare board with winning permutations
        # https://stackoverflow.com/a/33159908
        for player in ['O', 'X']:
            if (board == [player] * 3).all(axis=1).any(): # Check horizontally
                return True, player
            if (board == [player] * 3).all(axis=0).any(): # Check vertically
                return True, player
            # Check both diagonals
            if board[0, 0] == player and board[1,1] == player and board[2,2] == player:
                return True, player
            if board[0, 2] == player and board[1,1] == player and board[2,0] == player:
                return True, player
        # Check if game can continue (board has empty cells)
        if '' in board:
            return False, ''
        else:
            return True, 'D' # D for draw

    # input: xy pixel location of user mouse click example: (100px,100px)
    # outputs: xy integer grid location on board example: (5,5)
    def getXYFromUser(self,x,y):
        #get small width for smallBoards
        smallWidth= self.WINDOW_WIDTH / 9
        smallHeight=self.WINDOW_HEIGHT / 9
        #Get Large Board location
        gridX = math.floor(x/(smallWidth))
        gridY = math.floor(y/(smallHeight))
        return gridX, gridY




    #this function displays the move on the board and in the grid
    #input: ij as xy grid location, taken from getXYFromUser
    def displayMove(self, i, j, player, pg, screen):
        boardi = int(i / 3)   # Use large board dimensions [0,1,2]x[0,1,2]
        boardj = int(j / 3)
        winner = self.grid[boardj, boardi].getWinner
        if winner != '':
            if winner == 'D':
                winner = ''
            font = pg.font.SysFont('Arial', 100)
            width, height = font.size(player)
            
            smallWidth = self.WINDOW_WIDTH / 3
            smallHeight = self.WINDOW_HEIGHT / 3
            
            x = boardi * smallWidth + (smallWidth - width) / 2
            y = boardj * smallHeight + (smallHeight - height + 20) / 2
            
            rectLeft = boardi * smallWidth
            rectTop = boardj * smallHeight
            screen.fill((255,255,255), pg.Rect(rectLeft, rectTop, smallWidth, smallHeight))
            pg.draw.line(screen,(0,0,0),[0,self.WINDOW_HEIGHT//3],[self.WINDOW_WIDTH,self.WINDOW_HEIGHT//3],3)
            pg.draw.line(screen,(0,0,0),[self.WINDOW_WIDTH//3,0],[self.WINDOW_WIDTH//3,self.WINDOW_HEIGHT],3)
            pg.draw.line(screen,(0,0,0),[0,self.WINDOW_HEIGHT*2//3],[self.WINDOW_WIDTH,self.WINDOW_HEIGHT*2//3],3)
            pg.draw.line(screen,(0,0,0),[self.WINDOW_WIDTH*2//3,0],[self.WINDOW_WIDTH*2//3,self.WINDOW_HEIGHT],3)
            textsurface = font.render(winner, False, (0, 0, 0))
            screen.blit(textsurface,(x,y))
            return
            
        #set small width and small height
        smallWidth= self.WINDOW_WIDTH / 9
        smallHeight=self.WINDOW_HEIGHT / 9
        #get 0, 0 of x,y
        x = (i+1)*(smallWidth)
        y =(j+1)*(smallHeight)
        #center x, y
        x-=smallWidth/1.5
        y-=smallHeight/1.5
        font = pg.font.SysFont('Arial', 30)
        textsurface = font.render(player, False, (0, 0, 0))
        screen.blit(textsurface,(x,y))
    
