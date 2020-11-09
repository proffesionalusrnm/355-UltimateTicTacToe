import math
import numpy as np
class Board:
  def __init__(self):
    self.grid = np.empty(shape=(9,9),dtype='object')
    self.rows = 9
    self.WINDOW_HEIGHT = 700
    self.WINDOW_WIDTH = 600


  def displayBoard(self, pg, window):

    smallWidth= self.WINDOW_WIDTH / self.rows
    smallHeight=self.WINDOW_HEIGHT / self.rows

    #loop to make small tic tac toe boards
    for i in range(self.rows):
        #print to terminal for reference
        print(i,"|",self.grid[i])
        #print vertical lines
        pg.draw.line(window,(165,167,182),[smallWidth+smallWidth*i,0],[smallWidth+smallWidth*i,self.WINDOW_HEIGHT],2)
        #print horizontal lines
        pg.draw.line(window,(165,167,182),[0,smallHeight+smallHeight*i],[self.WINDOW_WIDTH,smallHeight+smallHeight*i],2)

    # Make large tic tac to board on top
    pg.draw.line(window,(0,0,0),[0,self.WINDOW_HEIGHT//3],[self.WINDOW_WIDTH,self.WINDOW_HEIGHT//3],3)
    pg.draw.line(window,(0,0,0),[self.WINDOW_WIDTH//3,0],[self.WINDOW_WIDTH//3,self.WINDOW_HEIGHT],3)
    pg.draw.line(window,(0,0,0),[0,self.WINDOW_HEIGHT*2//3],[self.WINDOW_WIDTH,self.WINDOW_HEIGHT*2//3],3)
    pg.draw.line(window,(0,0,0),[self.WINDOW_WIDTH*2//3,0],[self.WINDOW_WIDTH*2//3,self.WINDOW_HEIGHT],3)


#This function takes in an x,y position from user mouse click, and returns the grid location of move in the form of
# i, j , where i and j are int 0-9 with i representing the large board position and j representing the small board position
  def getPositionForGrid(self,x,y):
    #get small width for smallBoards
    smallWidth= self.WINDOW_WIDTH / 3
    smallHeight=self.WINDOW_HEIGHT / 3
    #define return variables
    finalLargeLocation= None
    finalSmallLocation = None
    #Get Large Board location
    largeBoardGridLocationX = math.floor(x/(self.WINDOW_WIDTH/3))+1
    largeBoardGridLocationY = math.floor(y/(self.WINDOW_HEIGHT/3))+1
    if largeBoardGridLocationY == 1:
        finalLargeLocation = largeBoardGridLocationX * largeBoardGridLocationY -1
    elif largeBoardGridLocationY == 2:
        finalLargeLocation = largeBoardGridLocationX + largeBoardGridLocationY +1 -1
    elif largeBoardGridLocationY == 3:
        finalLargeLocation = largeBoardGridLocationX + largeBoardGridLocationY +3 -1

    #get small Board Location
    smallBoardGridLocationX = math.floor(x/(smallWidth/3))+1
    smallBoardGridLocationY = math.floor(y/(smallHeight/3))+1

    if finalLargeLocation!=0 and finalLargeLocation !=3 and finalLargeLocation!=6:
        smallBoardGridLocationX %= 3
        if smallBoardGridLocationX==0:
            smallBoardGridLocationX+=3
    if finalLargeLocation >2:
        smallBoardGridLocationY%=3
        if smallBoardGridLocationY==0:
            smallBoardGridLocationY+=3
    if smallBoardGridLocationY == 1:
        finalSmallLocation = smallBoardGridLocationX * smallBoardGridLocationY -1
    elif smallBoardGridLocationY == 2:
        finalSmallLocation = smallBoardGridLocationX + smallBoardGridLocationY +1 -1
    elif smallBoardGridLocationY == 3:
        finalSmallLocation = smallBoardGridLocationX + smallBoardGridLocationY +3 -1

    return finalLargeLocation , finalSmallLocation

#this function displays the move on the board and in the grid
  def setPostionInGrid(self, i, j, player,pg,screen):

    self.grid[i][j] = player

    #set small width and small height
    smallWidth= self.WINDOW_WIDTH / 9
    smallHeight=self.WINDOW_HEIGHT / 9
    #get 0, 0 of x,y
    x = (smallWidth)
    y =(smallHeight)

    if j < 3:
        x += (x*j)
    elif 6>j>2:
        x+= x*(j-3)
        y+=y
    else:
        x+= x*(j-6)
        y+=(y*2)

    if i<3:
        x+=i*(self.WINDOW_WIDTH/3)
    elif 6>i>2:
        x+=(i-3)*(self.WINDOW_WIDTH/3)
        y+=(self.WINDOW_HEIGHT/3)
    else:
        x+=(i-6)*(self.WINDOW_WIDTH/3)
        y+=(2)*(self.WINDOW_HEIGHT/3)


    #center x, y
    x-=smallWidth/1.5
    y-=smallHeight/1.5


    font = pg.font.SysFont('Arial', 30)
    textsurface = font.render(player, False, (0, 0, 0))
    screen.blit(textsurface,(x,y))
