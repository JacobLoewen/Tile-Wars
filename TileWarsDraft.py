from asyncio import Event
import pygame as pg
from random import randrange

currSpeed = 4

WINDOW = 750

screenX = 1920
screenY = 1020

winX: int = int((screenX - 750) / 2)
winY: int = int((screenY - 750) / 2)

tempS = 0
tempW = 0
tempD = 0
tempA = 0

TILE_SIZE = 50

### GRID PLACEHOLDERS:
#BORDER = -1
BLANK = 0
RED_BASE = 1
BLUE_BASE = 2
RED_ONE = 3
BLUE_ONE = 4
RED_TWO = 5
BLUE_TWO = 6
RED_PLAYER = 7
BLUE_PLAYER = 8

# 25, 775, 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) # The '//' function is division but rounds the number down as well (into int format)

# random.randrange(start, stop[, step]) The ", step" function specifies that within the range from start to stop, it will not get a random
# number where it does not equal (start + (step * n)), n is an element of integers. For example: For 25, 775, 50, the step is 50, so it will get
# random values in the list of 25, 75, 125, 175, 225, ..., 625, 675, 725, and 775. It will never get anything like 320 or 710. 
# These values represent the CENTER of the tile
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

### Create grid | In order to exchange grid -> positioning, do formula y = 25 + 50x where x is the position of the tile in range (0, 14). For
### positioning -> grid, it will be x = (y - 25)/50 where y is the position number from range (25, 775). 
### Creating a border around grid with value -1 for BORDER
grid = [[BLANK for _ in range((WINDOW) // TILE_SIZE)] for _ in range((WINDOW) // TILE_SIZE)] # deep copy

prevGrid = 0
# for x in range(len(grid[0])):
#     for y in range(len(grid[1])):
#         if (x == 0 or y == 0) or (x == 15 or y == 15):
#             grid[y][x] = -1

tile = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake = tile.copy()
#snake.center = get_random_position()
snake.center = (375 + winX, 675 + winY)
length = 1
snake_dir = (0, 0)
time, time_step = 0, 110*currSpeed
food = snake.copy()
food.center = get_random_position()

SCREEN = pg.display.set_mode((screenX, screenY), pg.RESIZABLE)

screenX = WINDOW
screenY = WINDOW

clock = pg.time.Clock()

dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
currDir = pg.K_0
prevSnake = snake.copy()

idle = 1

### Colors:
border = (0, 0, 0, 255)
blank = (0, 0, 0, 225)

red_base = (51, 0, 0, 255)
blue_base = (0, 0, 51, 255)

red_player = (255, 0, 0, 255)
blue_player = (0, 0, 255, 255)

red_one = (255, 102, 102, 255)
blue_one = (102, 102, 255, 255)

red_two = (153, 0, 0, 255)
blue_two = (0, 0, 153, 255)

colors = [blank, red_base, blue_base, red_one, blue_one, red_two, blue_two, red_player, blue_player]

def homeBases():
    ### Setup Blue home base:
    global SCREEN
    global tile
    global winX
    global winY

    for posX in range(25, 775, 50):
        h = 25
        if posX >= 225 and posX < 275:
            h = 75
        elif posX >= 275 and posX < 325:
            h = 125
        elif posX >= 325 and posX < 475:
            h = 175
        elif posX >= 475 and posX < 525:
            h = 125
        elif posX >= 525 and posX < 575:
            h = 75
        for posY in range(25, h, 50):
            #print(str(posX) + ", " + str(h))
            tile.center = (posX + winX, posY + winY)
            pg.draw.rect(SCREEN, colors[BLUE_BASE], tile)

            gridX = int((posX-25)/50)
            gridY = int((posY-25)/50)
            #print("Grid Values:",gridX,gridY)
            grid[gridY][gridX] = BLUE_BASE
    
    ### Setup Red home base:
    for posX in range(25, 775, 50):
        h = 775
        if posX >= 225 and posX < 275:
            h = 725
        elif posX >= 275 and posX < 325:
            h = 675
        elif posX >= 325 and posX < 475:
            h = 625
        elif posX >= 475 and posX < 525:
            h = 675
        elif posX >= 525 and posX < 575:
            h = 725
        for posY in range(h, 775, 50):
            tile.center = (posX + winX, posY + winY)
            pg.draw.rect(SCREEN, colors[RED_BASE], tile)

            gridX = int((posX-25)/50)
            gridY = int((posY-25)/50)
            
            #print("Grid Values:",gridX,gridY)
            grid[gridY][gridX] = RED_BASE

def drawGrid():
    global TILE_SIZE
    global WINDOW
    global SCREEN
    global winX
    global winY
    WINDOW_WIDTH = WINDOW + winX
    WINDOW_HEIGHT = WINDOW + winY
    for x in range(winX, WINDOW_WIDTH, TILE_SIZE):
        for y in range(winY, WINDOW_HEIGHT, TILE_SIZE):
            rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)

            #gridX = int((posX-25)/50)
            #gridY = int((posY-25)/50)

            pg.draw.rect(SCREEN, 'white', rect, 1)

def drawTiles():
    global SCREEN
    global colors
    global grid

    for x in range(len(grid[0])):
        for y in range(len(grid[1])):

            pixelX = int((50*x)+winX)
            pixelY = int((50*y)+winY)

            rect = pg.Rect(pixelX, pixelY, TILE_SIZE, TILE_SIZE)
            pg.draw.rect(SCREEN, colors[grid[y][x]], rect)

# def setMove() -> Event:
#     global tempS
#     global tempW
#     global tempD
#     global tempA

#     if tempS == 1:
#         dirs[pg.K_s] = 1
#     elif tempW == 1:
#         dirs[pg.K_w] = 1
#     elif tempD == 1:
#         dirs[pg.K_d] = 1
#     elif tempA == 1:
#         dirs[pg.K_a] = 1


# def tempMove(c:str):
#     global tempS
#     global tempW
#     global tempD
#     global tempA

#     tempS = 0
#     tempW = 0
#     tempD = 0
#     tempA = 0

#     if c == 's':
#         tempS = 1
#     elif c == 'w':
#         tempW = 1
#     elif c == 'd':
#         tempD = 1
#     elif c == 'a':
#         tempA = 1


#def opposingTile() -> bool:


    #return True

def tileColors():
    global snake
    global prevGrid


    snakeX = snake.center[0]
    snakeY = snake.center[1]

    gridX = int((snakeX-winX-25)/50)
    gridY = int((snakeY-winY-25)/50)

    color = 0
    if prevGrid == 0:
        color = 3
    elif prevGrid == 1:
        color = 1
    elif prevGrid == 3 or prevGrid == 5:
        color = 5
    elif prevGrid == 4:
        color = 0
    elif prevGrid == 6:
        color = 4

    pg.draw.rect(SCREEN, colors[color], prevSnake)

    ### Get the pixel coords of tile and convert to grid coords and then put in grid
    prevSnakeX = prevSnake.center[0]
    prevSnakeY = prevSnake.center[1]

    prevGridX = int((prevSnakeX-winX-25)/50)
    prevGridY = int((prevSnakeY-winY-25)/50)

    grid[prevGridY][prevGridX] = color ### Set the color of the PREVIOUS snake

    
    prevGrid = grid[gridY][gridX] ### Get color of tile that snake is now on

SCREEN.fill('black')
drawGrid()

### This while loop has full respect to RED PLAYER
while True:
    #tile = pg.rect.Rect([snake.left + winX, snake.top + winY, TILE_SIZE - 2, TILE_SIZE - 2])
    #snake = tile.copy()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            for i in grid:
                print(i)
            print("left: " + str(snake.left) + ", right: " + str(snake.right) + ".")
            print("top: " + str(snake.top) + ", bottom: " + str(snake.bottom) + ".")

            # snakeX = snake.center[0]
            # snakeY = snake.center[1]

            # gridX = int((snakeX-winX-25)/50)
            # gridY = int((snakeY-winY-25)/50)
            # print("BLUE BASE: ",BLUE_BASE)
            # print("GRID: ",grid[gridY][gridX - 1])

            ### Key is Top; Previous motion was NOT downwards; Tile is NOT currently at a place where it can not be.
            if event.key == pg.K_w: #and dirs[pg.K_w]:
                if not (snake.top - 2 < winY):
                    snake_dir = (0, -TILE_SIZE)
                    #tempMove('w')
                    currDir = event.key
                    idle = 0   

            elif event.key == pg.K_s:  #and dirs[pg.K_s]:
                if not (snake.bottom + 2 > WINDOW + winY):
                    snake_dir = (0, TILE_SIZE)
                    #tempMove('s')
                    currDir = event.key
                    idle = 0 

            elif event.key == pg.K_a: #and dirs[pg.K_a]:
                if not (snake.left - 2 < winX):
                    snake_dir = (-TILE_SIZE, 0)
                    #tempMove('a')
                    currDir = event.key
                    idle = 0 

            elif event.key == pg.K_d: #and dirs[pg.K_d]:
                if not (snake.right + 2 > WINDOW + winX):
                    snake_dir = (TILE_SIZE, 0)
                    #tempMove('d') 
                    currDir = event.key
                    idle = 0 

            elif snake.left - 2 < 0 or snake.right + 2 > WINDOW or snake.top - 2 < 0 or snake.bottom + 2 > WINDOW:
                idle = 1
                print("IDLE IS 1: " + str(idle))

        if event.type == pg.VIDEORESIZE:
            screenX = event.w
            screenY = event.h
            prevWinX = winX
            prevWinY = winY
            winX = int((event.w - 750) / 2)
            winY = int((event.h - 750) / 2)
            SCREEN = pg.display.set_mode((screenX, screenY), pg.RESIZABLE)
            snake.move_ip(winX-prevWinX, winY-prevWinY)
            prevSnake.move_ip(winX-prevWinX, winY-prevWinY)

            ### Make screen Black, call drawGrid, and redraw all tiles

            SCREEN.fill('black')
            drawTiles()


    ### Move Snake and Draw Tiles
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
    
        #for i in grid:
            #print(i)

        #if not(snake.left - 2 < 0 or snake.right + 2 > WINDOW or snake.top - 2 < 0 or snake.bottom + 2 > WINDOW):
        #    snake.move_ip(snake_dir)


        ### do not move in place if the direction will go out of bounds

        # if grid[gridY][gridX - 1] == BLUE_BASE:
        #     ### Can not go Left
        #     dirs[pg.K_d] = 0
        # if grid[gridY][gridX + 1] == BLUE_BASE:
        #     ### Can not go Right
        #     dirs[pg.K_a] = 0
        # if grid[gridY - 1][gridX] == BLUE_BASE:
        #     ### Can not go Up
        #     dirs[pg.K_s] = 0
        # if grid[gridY + 1][gridX] == BLUE_BASE:
        #     ### Can not go Down
        #     dirs[pg.K_w] = 0

        #print(tuple_add)

        #tuple_sum_0 = sum(t[0] for t in tuple_add)
        #tuple_sum_1 = sum(t[1] for t in tuple_add)

        #print("GRID: ",grid[gridY][gridX])
        #print("gridY:", gridY, "GridX:", gridX)

        #print("DIRS (w, s, a, d): ",dirs)
        

        #move in place

        #if not (snake.left - 2 < 0 or snake.right + 2 > WINDOW or snake.top - 2 < 0 or snake.bottom + 2 > WINDOW):
        #    snake.move_ip(snake_dir)
        #print("left: " + str(snake.left) + ", right: " + str(snake.right) + ".")


        # Get tile in snake_dir

        #print(snake.center)

        #snake_dir_color

        #lightYellow = (255, 153, 153, 127)
        #try:
            #print(SCREEN.get_at(snake.center))
        #except:
            #print("No color at this point!")
        
        #print("CurrentGrid:",prevGrid)

        ### Draw Previous Snake with color based on the grid tile the player went over:


        snakeX = snake.center[0]
        snakeY = snake.center[1]

        gridX = int((snakeX-winX-25)/50)
        gridY = int((snakeY-winY-25)/50)

        if idle == 0:
            if currDir == pg.K_w:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if currDir == pg.K_s:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if currDir == pg.K_a:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if currDir == pg.K_d:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

        if (snake.left - 2 < winX or grid[gridY][gridX - 1] == BLUE_BASE) and dirs[pg.K_d] == 0:
            print("Can no longer go left")
        elif (snake.right + 2 > WINDOW + winX or grid[gridY][gridX + 1] == BLUE_BASE) and dirs[pg.K_a] == 0:
            print("Can no longer go right")
        elif (snake.top - 2 < winY or grid[gridY - 1][gridX] == BLUE_BASE) and dirs[pg.K_s] == 0:
            print("Can no longer go up")
        elif (snake.bottom + 2 > WINDOW + winY or grid[gridY + 1][gridX] == BLUE_BASE) and dirs[pg.K_w] == 0:
            print("Can no longer go down")
        else:
            prevSnake = snake.copy()
            snake.move_ip(snake_dir)
            tileColors()
            #setMove()

        tuple_add = [snake.center, snake_dir]

        #print("gridY:", gridY, "GridX:", gridX)

        #print("ChangedGrid:",prevGrid)
        #prevGrid = RED_ONE

        ### Draw Grid
        drawGrid()
        

        ### Make 'base' tiles static where the first layer disappears but the player tile does not
        homeBases()

        ### Draw Character Tile
        pg.draw.rect(SCREEN, colors[RED_PLAYER], snake)

        print()

    pg.display.flip()
    clock.tick(60) 