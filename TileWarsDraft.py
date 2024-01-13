from asyncio import Event
import pygame as pg
from random import randrange

currSpeed = 4

WINDOW = 750

screenX = 1920
screenY = 1020

winX: int = int((screenX - 750) / 2)
winY: int = int((screenY - 750) / 2)

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
POWER_UP = 9

# 25, 775, 50
RANGEX = ((TILE_SIZE // 2) + winX, (WINDOW - TILE_SIZE // 2) + winX + 2, TILE_SIZE) # The '//' function is division but rounds the number down as well (into int format)
RANGEY = ((TILE_SIZE // 2) + winY, (WINDOW - TILE_SIZE // 2) + winY + 2, TILE_SIZE)

# random.randrange(start, stop[, step]) The ", step" function specifies that within the range from start to stop, it will not get a random
# number where it does not equal (start + (step * n)), n is an element of integers. For example: For 25, 775, 50, the step is 50, so it will get
# random values in the list of 25, 75, 125, 175, 225, ..., 625, 675, 725, and 775. It will never get anything like 320 or 710. 
# These values represent the CENTER of the tile
get_random_position = lambda: [randrange(*RANGEX), randrange(*RANGEY)]

### Create grid | In order to exchange grid -> positioning, do formula y = 25 + 50x where x is the position of the tile in range (0, 14). For
### positioning -> grid, it will be x = (y - 25)/50 where y is the position number from range (25, 775). 
### Creating a border around grid with value -1 for BORDER
grid = [[BLANK for _ in range((WINDOW) // TILE_SIZE)] for _ in range((WINDOW) // TILE_SIZE)] # deep copy

prevRedGrid = 0
prevBlueGrid = 0

foodEaten = True

tile = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])

snakeRed = tile.copy()
snakeRed.center = (375 + winX, 675 + winY)
snakeBlue = tile.copy()
snakeBlue.center = (375 + winX, 75 + winY)

length = 1
snakeRed_dir = (0, 0)
snakeBlue_dir = (0, 0)
time, time_step = 0, 110*currSpeed

### Power used as Invincibility Blocks
power = snakeRed.copy()
power_iter = 0

powerCountRed = 0
powerCountBlue = 0

#food.center = get_random_position()

SCREEN = pg.display.set_mode((screenX, screenY), pg.RESIZABLE)

screenX = WINDOW
screenY = WINDOW

clock = pg.time.Clock()

dirsRed = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
dirsBlue = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
currRedDir = pg.K_0
currBlueDir = pg.K_1
prevSnakeRed = snakeRed.copy()
prevSnakeBlue = snakeBlue.copy()

idle = 0
### idle = 1

### Colors:
border = (0, 0, 0, 255)
blank = (0, 0, 0, 225)

red_base = (255, 0, 127, 255) #red_base = (51, 0, 0, 255)
blue_base = (127, 0, 255, 255) #blue_base = (0, 0, 51, 255)

red_player = (255, 0, 0, 255)
blue_player = (0, 0, 255, 255)

red_one = (255, 102, 102, 255)
blue_one = (102, 102, 255, 255)

red_two = (153, 0, 0, 255)
blue_two = (0, 0, 153, 255)

power_up = (255, 255, 255, 255)

colors = [blank, red_base, blue_base, red_one, blue_one, red_two, blue_two, red_player, blue_player, power_up]

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
            tile.center = (posX + winX, posY + winY)
            pg.draw.rect(SCREEN, colors[BLUE_BASE], tile)

            gridX = int((posX-25)/50)
            gridY = int((posY-25)/50)
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

def tileColors(player: str):
    global snakeRed
    global snakeBlue
    global prevRedGrid
    global prevBlueGrid
    global powerCountRed
    global powerCountBlue

    if player == "Red":

        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        gridRedX = int((snakeRedX-winX-25)/50)
        gridRedY = int((snakeRedY-winY-25)/50)

        colorRed = 0
        if prevRedGrid == 0:
            colorRed = 3
        elif prevRedGrid == 1:
            colorRed = 1
        elif prevRedGrid == 3 or prevRedGrid == 5:
            colorRed = 5
        elif prevRedGrid == 4:
            colorRed = 0
        elif prevRedGrid == 6:
            colorRed = 4
        elif prevRedGrid == 9:
            colorRed = 0
            powerCountRed += 1

        pg.draw.rect(SCREEN, colors[colorRed], prevSnakeRed)

        ### Get the pixel coords of tile and convert to grid coords and then put in grid
        prevSnakeRedX = prevSnakeRed.center[0]
        prevSnakeRedY = prevSnakeRed.center[1]

        prevRedGridX = int((prevSnakeRedX-winX-25)/50)
        prevRedGridY = int((prevSnakeRedY-winY-25)/50)

        grid[prevRedGridY][prevRedGridX] = colorRed ### Set the color of the PREVIOUS snakeRed

        
        prevRedGrid = grid[gridRedY][gridRedX] ### Get color of tile that snakeRed is now on

    ### Blue

    elif player == "Blue":

        snakeBlueX = snakeBlue.center[0]
        snakeBlueY = snakeBlue.center[1]

        gridBlueX = int((snakeBlueX-winX-25)/50)
        gridBlueY = int((snakeBlueY-winY-25)/50)

        colorBlue = 0
        if prevBlueGrid == 0:
            colorBlue = 4
        elif prevBlueGrid == 2:
            colorBlue = 2
        elif prevBlueGrid == 4 or prevBlueGrid == 6:
            colorBlue = 6
        elif prevBlueGrid == 3:
            colorBlue = 0
        elif prevBlueGrid == 5:
            colorBlue = 3
        elif prevBlueGrid == 9:
            colorBlue = 0
            powerCountBlue += 1

        pg.draw.rect(SCREEN, colors[colorBlue], prevSnakeBlue)

        ### Get the pixel coords of tile and convert to grid coords and then put in grid
        prevSnakeBlueX = prevSnakeBlue.center[0]
        prevSnakeBlueY = prevSnakeBlue.center[1]

        prevBlueGridX = int((prevSnakeBlueX-winX-25)/50)
        prevBlueGridY = int((prevSnakeBlueY-winY-25)/50)

        grid[prevBlueGridY][prevBlueGridX] = colorBlue ### Set the color of the PREVIOUS snakeRed

        
        prevBlueGrid = grid[gridBlueY][gridBlueX] ### Get color of tile that snakeBlue is now on



SCREEN.fill('black')
drawGrid()

### This while loop has full respect to RED PLAYER
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            for i in grid:
                print(i)
            print("powerCountRed:",powerCountRed)
            print("powerCountBlue:",powerCountBlue)
            print("left: " + str(snakeRed.left) + ", right: " + str(snakeRed.right) + ".")
            print("top: " + str(snakeRed.top) + ", bottom: " + str(snakeRed.bottom) + ".")

            ### Red Player
            if event.key == pg.K_w:
                if not (snakeRed.top - 2 < winY):
                    snakeRed_dir = (0, -TILE_SIZE)
                    currRedDir = event.key
                    idle = 0   

            elif event.key == pg.K_s:
                if not (snakeRed.bottom + 2 > WINDOW + winY):
                    snakeRed_dir = (0, TILE_SIZE)
                    currRedDir = event.key
                    idle = 0 

            elif event.key == pg.K_a:
                if not (snakeRed.left - 2 < winX):
                    snakeRed_dir = (-TILE_SIZE, 0)
                    currRedDir = event.key
                    idle = 0 

            elif event.key == pg.K_d:
                if not (snakeRed.right + 2 > WINDOW + winX):
                    snakeRed_dir = (TILE_SIZE, 0)
                    currRedDir = event.key
                    idle = 0 

            #elif snakeRed.left - 2 < 0 or snakeRed.right + 2 > WINDOW or snakeRed.top - 2 < 0 or snakeRed.bottom + 2 > WINDOW:
            #    idle = 1
            #    print("IDLE IS 1: " + str(idle))

            

            ### Blue Player:
            if event.key == pg.K_UP:
                if not (snakeBlue.top - 2 < winY):
                    snakeBlue_dir = (0, -TILE_SIZE)
                    currBlueDir = event.key
                    idle = 0   

            elif event.key == pg.K_DOWN:
                if not (snakeBlue.bottom + 2 > WINDOW + winY):
                    snakeBlue_dir = (0, TILE_SIZE)
                    currBlueDir = event.key
                    idle = 0 

            elif event.key == pg.K_LEFT:
                if not (snakeBlue.left - 2 < winX):
                    snakeBlue_dir = (-TILE_SIZE, 0)
                    currBlueDir = event.key
                    idle = 0 

            elif event.key == pg.K_RIGHT:
                if not (snakeBlue.right + 2 > WINDOW + winX):
                    snakeBlue_dir = (TILE_SIZE, 0)
                    currBlueDir = event.key
                    idle = 0 

            #elif snakeBlue.left - 2 < 0 or snakeBlue.right + 2 > WINDOW or snakeBlue.top - 2 < 0 or snakeBlue.bottom + 2 > WINDOW:
                #idle = 1
                #print("IDLE IS 1: " + str(idle))

        if event.type == pg.VIDEORESIZE:
            screenX = event.w
            screenY = event.h
            prevWinX = winX
            prevWinY = winY
            winX = int((event.w - 750) / 2)
            winY = int((event.h - 750) / 2)
            SCREEN = pg.display.set_mode((screenX, screenY), pg.RESIZABLE)
            snakeRed.move_ip(winX-prevWinX, winY-prevWinY)
            prevSnakeRed.move_ip(winX-prevWinX, winY-prevWinY)

            RANGEX = ((TILE_SIZE // 2) + winX, (WINDOW - TILE_SIZE // 2) + winX, TILE_SIZE) # The '//' function is division but rounds the number down as well (into int format)
            RANGEY = ((TILE_SIZE // 2) + winY, (WINDOW - TILE_SIZE // 2) + winY, TILE_SIZE)

            get_random_position = lambda: [randrange(*RANGEX), randrange(*RANGEY)]

            snakeBlue.move_ip(winX-prevWinX, winY-prevWinY)
            prevSnakeBlue.move_ip(winX-prevWinX, winY-prevWinY)
            power.move_ip(winX-prevWinX, winY-prevWinY)

            ### Make screen Black, call drawGrid, and redraw all tiles

            SCREEN.fill('black')
            drawTiles()

    

    ### Move snakeRed and Draw Tiles
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now

        #if foodEaten:
        power.center = get_random_position()
            #foodEaten = False

        ### Draw Previous snakeRed with color based on the grid tile the player went over:

        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        gridRedX = int((snakeRedX-winX-25)/50)
        gridRedY = int((snakeRedY-winY-25)/50)

        print("idle:",idle)

        if idle == 0:
            if currRedDir == pg.K_w:
                snakeRed_dir = (0, -TILE_SIZE)
                dirsRed = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if currRedDir == pg.K_s:
                snakeRed_dir = (0, TILE_SIZE)
                dirsRed = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if currRedDir == pg.K_a:
                snakeRed_dir = (-TILE_SIZE, 0)
                dirsRed = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if currRedDir == pg.K_d:
                snakeRed_dir = (TILE_SIZE, 0)
                dirsRed = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

        print("winX:",winX,"winX + WINDOW:",winX + WINDOW)
        print("winY:",winY,"winY + WINDOW:",winY + WINDOW)
        print(dirsRed)

        if (snakeRed.left - 2 < winX or grid[gridRedY][gridRedX - 1] == BLUE_BASE) and dirsRed[pg.K_d] == 0:
            print("Can no longer go left")
        elif (snakeRed.right + 2 > WINDOW + winX or grid[gridRedY][gridRedX + 1] == BLUE_BASE) and dirsRed[pg.K_a] == 0:
            print("Can no longer go right")
        elif (snakeRed.top - 2 < winY or grid[gridRedY - 1][gridRedX] == BLUE_BASE) and dirsRed[pg.K_s] == 0:
            print("Can no longer go up")
        elif (snakeRed.bottom + 2 > WINDOW + winY or grid[gridRedY + 1][gridRedX] == BLUE_BASE) and dirsRed[pg.K_w] == 0:
            print("Can no longer go down")
        else:
            prevSnakeRed = snakeRed.copy()
            snakeRed.move_ip(snakeRed_dir)
            tileColors("Red")

        tuple_add = [snakeRed.center, snakeRed_dir]


        ### Draw Previous snakeBlue with color based on the grid tile the player went over:

        snakeBlueX = snakeBlue.center[0]
        snakeBlueY = snakeBlue.center[1]

        gridBlueX = int((snakeBlueX-winX-25)/50)
        gridBlueY = int((snakeBlueY-winY-25)/50)

        if idle == 0:
            if currBlueDir == pg.K_UP:
                snakeBlue_dir = (0, -TILE_SIZE)
                dirsBlue = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if currBlueDir == pg.K_DOWN:
                snakeBlue_dir = (0, TILE_SIZE)
                dirsBlue = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if currBlueDir == pg.K_LEFT:
                snakeBlue_dir = (-TILE_SIZE, 0)
                dirsBlue = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
            if currBlueDir == pg.K_RIGHT:
                snakeBlue_dir = (TILE_SIZE, 0)
                dirsBlue = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

        if (snakeBlue.left - 2 < winX or grid[gridBlueY][gridBlueX - 1] == RED_BASE) and dirsBlue[pg.K_RIGHT] == 0:
            print("Can no longer go left")
        elif (snakeBlue.right + 2 > WINDOW + winX or grid[gridBlueY][gridBlueX + 1] == RED_BASE) and dirsBlue[pg.K_LEFT] == 0:
            print("Can no longer go right")
        elif (snakeBlue.top - 2 < winY or grid[gridBlueY - 1][gridBlueX] == RED_BASE) and dirsBlue[pg.K_DOWN] == 0:
            print("Can no longer go up")
        elif (snakeBlue.bottom + 2 > WINDOW + winY or grid[gridBlueY + 1][gridBlueX] == RED_BASE) and dirsBlue[pg.K_UP] == 0:
            print("Can no longer go down")
        else:
            prevSnakeBlue = snakeBlue.copy()
            snakeBlue.move_ip(snakeBlue_dir)
            tileColors("Blue")

        tuple_add = [snakeBlue.center, snakeBlue_dir]


        ### Draw Grid
        drawGrid()
        
        ### Make 'base' tiles static where the first layer disappears but the player tile does not
        homeBases()

        ### Draw Character Tile
        pg.draw.rect(SCREEN, colors[RED_PLAYER], snakeRed)
        pg.draw.rect(SCREEN, colors[BLUE_PLAYER], snakeBlue)

        power_iter += 1
        ### Start with every 10 seconds and go up from there:
        if power_iter >= 10:
            pg.draw.rect(SCREEN, colors[POWER_UP], power)
            ### Add power_up to grid
            powerX = power.center[0]
            powerY = power.center[1]

            powerGridX = int((powerX-winX-25)/50)
            powerGridY = int((powerY-winY-25)/50)

            grid[powerGridY][powerGridX] = POWER_UP ### Set the color to white for POWER_UP

            power_iter = 0

        print()

    pg.display.flip()
    clock.tick(60) 