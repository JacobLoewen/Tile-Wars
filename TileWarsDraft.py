from asyncio import Event
import pygame as pg
from random import randrange
from random import randint

pg.init() #May be able to delete

WINDOW = 750

screenX = 1920
screenY = 1080

#585
winX: int = int((screenX - 750) / 2)

#165
winY: int = int((screenY - 750) / 2)

TILE_SIZE = 50

### GRID PLACEHOLDERS:
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
ULTRA_POWER_UP = 10

# 25, 775, 50
RANGEX = ((TILE_SIZE // 2) + winX, (WINDOW - TILE_SIZE // 2) + winX + 2, TILE_SIZE) # The '//' function is division but rounds the number down as well (into int format)
RANGEY = ((TILE_SIZE // 2) + winY, (WINDOW - TILE_SIZE // 2) + winY + 2, TILE_SIZE)
RANGEYRed = ((TILE_SIZE // 2) + winY + (WINDOW // 2) - 25, (WINDOW - TILE_SIZE // 2) + winY + 2, TILE_SIZE)
RANGEYBlue = ((TILE_SIZE // 2) + winY, (WINDOW - TILE_SIZE // 2) - (WINDOW // 2) + 25 + winY + 2, TILE_SIZE)

# random.randrange(start, stop[, step]) The ", step" function specifies that within the range from start to stop, it will not get a random
# number where it does not equal (start + (step * n)), n is an eletment of integers. For example: For 25, 775, 50, the step is 50, so it will get
# random values in the list of 25, 75, 125, 175, 225, ..., 625, 675, 725, and 775. It will never get anything like 320 or 710. 
# These values represent the CENTER of the tile

get_random_position = lambda: [randrange(*RANGEX), randrange(*RANGEY)]
get_random_position_red = lambda: [randrange(*RANGEX), randrange(*RANGEYRed)]
get_random_position_blue = lambda: [randrange(*RANGEX), randrange(*RANGEYBlue)]

### Create grid | In order to exchange grid -> positioning, do formula y = 25 + 50x where x is the position of the tile in range (0, 14). For
### positioning -> grid, it will be x = (y - 25)/50 where y is the position number from range (25, 775). 
### Creating a border around grid with value -1 for BORDER
grid = [[BLANK for _ in range((WINDOW) // TILE_SIZE)] for _ in range((WINDOW) // TILE_SIZE)] # deep copy

redPowerToggle = False
bluePowerToggle = False

redPointsCounter = 0
bluePointsCounter = 0

prevRedGrid = 0
prevBlueGrid = 0

redMoveCounter = 0
blueMoveCounter = 0

### Increments before loop in move counters, so set default as 1
redSpeed = 2
blueSpeed = 2

foodEaten = True

tile = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])

snakeRed = tile.copy()
snakeRed.center = (375 + winX, 675 + winY)
snakeBlue = tile.copy()
snakeBlue.center = (375 + winX, 75 + winY)

length = 1
snakeRed_dir = (0, 0)
snakeBlue_dir = (0, 0)

### Main function for speed:
time, time_step = 0, 125 ### 1/8 of a second

### Power used as Invincibility Blocks
power = snakeRed.copy()
ultraPower = snakeRed.copy()
power_iter = 0

powerCountRed = 0
powerCountBlue = 0

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

idle = 0 #May be able to delete
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
ultra_power_up = (225, 215, 0, 255)


### Oli's color codes
# border = (0, 0, 0, 255)
# blank = (0, 0, 0, 225)

# red_base = (244, 151, 122, 255) #red_base = (51, 0, 0, 255)
# blue_base = (114, 182, 198, 255) #blue_base = (0, 0, 51, 255)

# red_player = (212, 55, 39, 255)
# blue_player = (38, 70, 137, 255)

# red_one = (254, 196, 96, 255)
# blue_one = (140, 168, 68, 255)

# red_two = (245, 157, 66, 255)
# blue_two = (13, 70, 36, 255)

# power_up = (255, 255, 255, 255)

colors = [blank, red_base, blue_base, red_one, blue_one, red_two, blue_two, red_player, blue_player, power_up, ultra_power_up]

def frontEnd():
    global snakeRed
    global snakeBlue
    global colors
    global power_iter
    
    SCREEN.fill('black') ### Blanks
    drawTiles() ### Paths

    #sideFeatures()

    power_iter += 1
    ### Start with every 10 seconds and go up from there:
    if power_iter >= 90: ### 45 seconds * 2 1/2 seconds of time iteration equals 60 half seconds
    #if power_iter >= 10: ### TEMPORARY
        invincibilityBlockBlue()
        invincibilityBlockRed()
        invincibilityBlockGeneral()
        power_iter = 0

    ### Make 'base' tiles static where the first layer disappears but the player tile does not
    homeBases() ### Bases
    sideFeatures()

    ### Draw Character Tile
    pg.draw.rect(SCREEN, colors[RED_PLAYER], snakeRed) ### Red Player
    pg.draw.rect(SCREEN, colors[BLUE_PLAYER], snakeBlue) ### Blue Player

    #Could make it be a 'draw character tile' function which takes the parameter of the tile in front and then decides whether it draws it or not

    # power_iter += 1
    # ### Start with every 10 seconds and go up from there:
    # if power_iter >= 60: ### 30 seconds * 2 1/2 seconds of time iteration equals 60 half seconds
    # #if power_iter >= 10: ### TEMPORARY
    #     invincibilityBlockBlue()
    #     invincibilityBlockRed()
    
    ### Draw Grid
    drawGrid()

def sideFeatures():
    global snakeRed
    global powerCountRed
    global powerCountBlue

    redPowerCounterTile = snakeRed.copy()
    bluePowerCounterTile = snakeRed.copy()
    redPowerCounterTile.center = (winX - 250, winY + 100)
    bluePowerCounterTile.center = (winX + WINDOW + 150, 100 + winY)
    pg.draw.rect(SCREEN, colors[POWER_UP], redPowerCounterTile)
    pg.draw.rect(SCREEN, colors[POWER_UP], bluePowerCounterTile)


    ### Draw player score areas:

    ### Starting with Red:

    pg.draw.line(SCREEN, colors[RED_TWO], ((winX - 350), (winY + 750)),((winX - 350), (winY)), 15)
    pg.draw.line(SCREEN, colors[RED_TWO], ((winX - 50), (winY + 750)),((winX - 50), (winY)), 15)
    pg.draw.line(SCREEN, colors[RED_TWO], ((winX - 350), (winY)),((winX - 50), (winY)), 15)
    pg.draw.line(SCREEN, colors[RED_TWO], ((winX - 350), (winY + 750)),((winX - 50), (winY + 750)), 15)

    countPoints()

    ### Create the font:
    font = pg.font.Font('Questrial-Regular.ttf', 65)
    text_render = font.render("x ", True, (255, 255, 255))
    #text_position = (376, 228)
    text_position = (winX - 209, winY + 63)
    SCREEN.blit(text_render, text_position)

    text_render = font.render(str(powerCountRed), True, (255, 255, 255))
    #text_position = (420, 232)
    text_position = (winX - 165, winY + 67)
    SCREEN.blit(text_render, text_position)

    text_render = font.render(str(redPointsCounter), True, (255, 255, 255))
    text_position = (winX - 209, winY + 128)
    SCREEN.blit(text_render, text_position)

    ### Starting with Blue:

    pg.draw.line(SCREEN, colors[BLUE_TWO], ((winX + 350 + WINDOW), (winY + 750)),((winX + 350 + WINDOW), (winY)), 15)
    pg.draw.line(SCREEN, colors[BLUE_TWO], ((winX + 50 + WINDOW), (winY + 750)),((winX + 50 + WINDOW), (winY)), 15)
    pg.draw.line(SCREEN, colors[BLUE_TWO], ((winX + 350 + WINDOW), (winY)),((winX + 50 + WINDOW), (winY)), 15)
    pg.draw.line(SCREEN, colors[BLUE_TWO], ((winX + 350 + WINDOW), (winY + 750)),((winX + 50 + WINDOW), (winY + 750)), 15)

    ### Create the font:
    font = pg.font.Font('Questrial-Regular.ttf', 65)
    text_render = font.render("x ", True, (255, 255, 255))
    #text_position = (1526,228)
    text_position = (winX + 941, winY + 63)
    SCREEN.blit(text_render, text_position)

    text_render = font.render(str(powerCountBlue), True, (255, 255, 255))
    #text_position = (1570,232)
    text_position = (winX + 985, winY + 67)
    SCREEN.blit(text_render, text_position)

    text_render = font.render(str(bluePointsCounter), True, (255, 255, 255))
    #text_position = (1570,232)
    text_position = (winX + 985, winY + 132)
    SCREEN.blit(text_render, text_position)



def invincibilityBlockRed():
    global power 
    global colors
    global power_iter

    power.center = get_random_position_red()
    pg.draw.rect(SCREEN, colors[POWER_UP], power)

    ### Add power_up to grid
    powerX = power.center[0]
    powerY = power.center[1]

    powerGridX = int((powerX-winX-25)/50)
    powerGridY = int((powerY-winY-25)/50)

    if grid[powerGridY][powerGridX] == 1:
        invincibilityBlockRed()
    else:
        grid[powerGridY][powerGridX] = POWER_UP ### Set the color to white for POWER_UP

def invincibilityBlockBlue():
    global power
    global colors
    global power_iter

    power.center = get_random_position_blue()
    pg.draw.rect(SCREEN, colors[POWER_UP], power)

    ### Add power_up to grid
    powerX = power.center[0]
    powerY = power.center[1]

    powerGridX = int((powerX-winX-25)/50)
    powerGridY = int((powerY-winY-25)/50)

    if grid[powerGridY][powerGridX] == 2:
        invincibilityBlockBlue()
    else:
        grid[powerGridY][powerGridX] = POWER_UP ### Set the color to white for POWER_UP

    power_iter = 0

def invincibilityBlockGeneral():
    global power
    global colors
    global power_iter
    global ultraPower


    randomNum = randint(1, 2)
    if randomNum == 1:
        ultraPower.center = get_random_position()
        pg.draw.rect(SCREEN, colors[ULTRA_POWER_UP], ultraPower)

        ### Add power_up to grid
        powerX = ultraPower.center[0]
        powerY = ultraPower.center[1]

        powerGridX = int((powerX-winX-25)/50)
        powerGridY = int((powerY-winY-25)/50)

        if grid[powerGridY][powerGridX] == 1 or grid[powerGridY][powerGridX] == 2:
            invincibilityBlockGeneral()
        else:
            grid[powerGridY][powerGridX] = ULTRA_POWER_UP ### Set the color to white for POWER_UP

    else:
        power.center = get_random_position()
        pg.draw.rect(SCREEN, colors[POWER_UP], power)

        ### Add power_up to grid
        powerX = power.center[0]
        powerY = power.center[1]

        powerGridX = int((powerX-winX-25)/50)
        powerGridY = int((powerY-winY-25)/50)

        if grid[powerGridY][powerGridX] == 1 or grid[powerGridY][powerGridX] == 2:
            invincibilityBlockGeneral()
        else:
            grid[powerGridY][powerGridX] = POWER_UP ### Set the color to white for POWER_UP

    power_iter = 0

def countPoints():
    global redPointsCounter
    global bluePointsCounter

    redPointsCounter = 0
    bluePointsCounter = 0

    for line in grid:
        for x in line:
            if x == 3:
                redPointsCounter += 1
            elif x == 5:
                redPointsCounter += 2
            elif x == 4:
                bluePointsCounter += 1
            elif x == 6:
                bluePointsCounter += 2

def homeBases():
    global SCREEN
    global tile
    global winX
    global winY

    ### Setup Blue home base:
    for posX in range(25, 775, 50):
        h = 25
        if posX >= 225 and posX < 275:
            h = 175
        elif posX >= 275 and posX < 325:
            h = 125
        elif posX >= 325 and posX < 375:
            h = 175
        elif posX >= 375 and posX < 425:
            h = 125
        elif posX >= 425 and posX < 475:
            h = 175
        elif posX >= 475 and posX < 525:
            h = 125
        elif posX >= 525 and posX < 575:
            h = 175
        for posY in range(25, h, 50):
            tile.center = (posX + winX, posY + winY)

            gridX = int((posX-25)/50)
            gridY = int((posY-25)/50)
            
            currTile = grid[gridY][gridX] 
        
            if currTile == POWER_UP: ### If not invincibility block, then put base
                #grid[gridY][gridX] = POWER_UP
                print("WARNING!!!")
                print("WARNING!!!")
                print("WARNING!!!")
                #invincibilityBlockBlue()
            
            grid[gridY][gridX] = BLUE_BASE
            
            pg.draw.rect(SCREEN, colors[grid[gridY][gridX]], tile)
    
    ### Setup Red home base:
    for posX in range(25, 775, 50):
        h = 775
        if posX >= 225 and posX < 275:
            h = 625
        elif posX >= 275 and posX < 325:
            h = 675
        elif posX >= 325 and posX < 375: 
            h = 625
        elif posX >= 375 and posX < 425: 
            h = 675
        elif posX >= 425 and posX < 475: 
            h = 625
        elif posX >= 475 and posX < 525: 
            h = 675
        elif posX >= 525 and posX < 575:
            h = 625
        for posY in range(h, 775, 50):
            tile.center = (posX + winX, posY + winY)

            gridX = int((posX-25)/50)
            gridY = int((posY-25)/50)
            
            currTile = grid[gridY][gridX]
            if currTile == POWER_UP: ### If not invincibility block, then put base
                #grid[gridY][gridX] = POWER_UP 
                ### Instead of replacing as power_up, replace as grid and place invincibility block someplace else
                print("WARNING!!!")
                print("WARNING!!!")
                print("WARNING!!!")
                #invincibilityBlockRed()
               
            grid[gridY][gridX] = RED_BASE

            pg.draw.rect(SCREEN, colors[grid[gridY][gridX]], tile)

def playerCollision():
    ### Runs if the players are on the
    ### Same tile
    
    global powerCountRed
    global powerCountBlue
    global redSpeed
    global blueSpeed
    global redMoveCounter
    global blueMoveCounter

    ### OLD Collision Method
    #     
    # if powerCountRed > powerCountBlue:
    #     ### Blue respawns after 3 seconds
    #     ### And Red's count decreases by
    #     ### 1 (for now)
    #     snakeBlue.center = (375 + winX, 75 + winY)
    #     blueSpeed = 40 ### Wait for 5 seconds
    #     blueMoveCounter = 0
    #     powerCountRed -= 2
    # elif powerCountRed < powerCountBlue:
    #     ### Red respawns after 3 seconds
    #     ### And Blue's count decreases
    #     ### by 1 (for now)
    #     snakeRed.center = (375 + winX, 675 + winY)
    #     redSpeed = 40
    #     redMoveCounter = 0
    #     powerCountBlue -= 2
    # elif powerCountRed == powerCountBlue:
    #     ### BOTH respawn after 3 seconds
    #     snakeRed.center = (375 + winX, 675 + winY)
    #     redSpeed = 40
    #     redMoveCounter = 0
    #     snakeBlue.center = (375 + winX, 75 + winY)
    #     blueSpeed = 40
    #     blueMoveCounter = 0

    ### New Collision Method
    # Winner will respawn upon collision
    if redPointsCounter < bluePointsCounter:
        ### Blue respawns after 3 seconds
        ### And Red's count decreases by
        ### 1 (for now)
        snakeBlue.center = (375 + winX, 75 + winY)
        blueSpeed = 40 ### Wait for 5 seconds
        blueMoveCounter = 0
        powerCountRed -= 2
    elif redPointsCounter > bluePointsCounter:
        ### Red respawns after 3 seconds
        ### And Blue's count decreases
        ### by 1 (for now)
        snakeRed.center = (375 + winX, 675 + winY)
        redSpeed = 40
        redMoveCounter = 0
        powerCountBlue -= 2
    elif redPointsCounter == bluePointsCounter:
        ### BOTH respawn after 3 seconds
        snakeRed.center = (375 + winX, 675 + winY)
        redSpeed = 40
        redMoveCounter = 0
        snakeBlue.center = (375 + winX, 75 + winY)
        blueSpeed = 40
        blueMoveCounter = 0
    

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

def speedAlter(player: str):
    global snakeRed
    global snakeBlue
    global redSpeed
    global blueSpeed

    if player == "Red":

        ### Get grid of snakeRed currently and then respectively 
        ### increment to wherever shows the next tile
        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        ### Grid may go out of bounds. If this is the case, return
        ### 1 as the speed.
        try:
            # gridRedX = int((snakeRedX-winX-25 + snakeRed_dir[0])/50)
            # gridRedY = int((snakeRedY-winY-25 + snakeRed_dir[1])/50)
            gridRedX = int((snakeRedX-winX-25)/50)
            gridRedY = int((snakeRedY-winY-25)/50)
            currGrid = grid[gridRedY][gridRedX]

            colorRed = 0
            if currGrid == 0:
                redSpeed = 6
            elif currGrid == 1:
                redSpeed = 2
            elif currGrid == 3:
                redSpeed = 4
            elif currGrid == 5:
                redSpeed = 2
            elif currGrid == 4:
                redSpeed = 6
            elif currGrid == 6:
                redSpeed = 8
            elif currGrid == 9:
                redSpeed = 6
        except Exception:
            redSpeed = 2

    if player == "Blue":
        ### Get grid of snakeRed currently and then respectively 
        ### increment to wherever shows the next tile
        snakeBlueX = snakeBlue.center[0]
        snakeBlueY = snakeBlue.center[1]

        ### Grid may go out of bounds. If this is the case, return
        ### 1 as the speed.
        try:
            # gridRedX = int((snakeRedX-winX-25 + snakeRed_dir[0])/50)
            # gridRedY = int((snakeRedY-winY-25 + snakeRed_dir[1])/50)
            gridBlueX = int((snakeBlueX-winX-25)/50)
            gridBlueY = int((snakeBlueY-winY-25)/50)
            currGrid = grid[gridBlueY][gridBlueX]

            colorBlue = 0
            if currGrid == 0:
                blueSpeed = 6
            elif currGrid == 2:
                blueSpeed = 2
            elif currGrid == 4:
                blueSpeed = 4
            elif currGrid == 6:
                blueSpeed = 2
            elif currGrid == 3:
                blueSpeed = 6
            elif currGrid == 5:
                blueSpeed = 8
            elif currGrid == 9:
                blueSpeed = 6
        except Exception:
            blueSpeed = 2

def tileColors(player: str):
    global snakeRed
    global snakeBlue
    global prevRedGrid
    global prevBlueGrid
    global powerCountRed
    global powerCountBlue
    global redSpeed
    global blueSpeed

    if player == "Red":

        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        gridRedX = int((snakeRedX-winX-25)/50)
        gridRedY = int((snakeRedY-winY-25)/50)

        speedAlter(player)

        colorRed = 0
        if prevRedGrid == 0:
            colorRed = 3
        elif prevRedGrid == 1:
            colorRed = 1
        elif prevRedGrid == 3:
            colorRed = 5
        elif prevRedGrid == 5:
            colorRed = 5
        elif prevRedGrid == 4:
            colorRed = 0
        elif prevRedGrid == 6:
            colorRed = 0
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

        speedAlter(player)

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
            colorBlue = 0
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



#SCREEN.fill('black')
#drawGrid()

### This while loop has full respect to RED PLAYER
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYUP:
            if event.key == pg.K_c:
                redPowerToggle = True
        elif event.type == pg.KEYDOWN:
            #for i in grid:
            #    print(i)
            #print("powerCountRed:",powerCountRed)
            #print("powerCountBlue:",powerCountBlue)
            #print("left: " + str(snakeRed.left) + ", right: " + str(snakeRed.right) + ".")
            #print("top: " + str(snakeRed.top) + ", bottom: " + str(snakeRed.bottom) + ".")

            ### Red Player

            ### Power-Up Usage
            if event.key == pg.K_c:
                redPowerToggle = False

            ### Movement
            if event.key == pg.K_w:
                if redPowerToggle:

                elif not (snakeRed.top - 2 < winY):
                    snakeRed_dir = (0, -TILE_SIZE)
                    currRedDir = event.key
                    idle = 0   

            elif event.key == pg.K_s:
                if redPowerToggle:

                elif not (snakeRed.bottom + 2 > WINDOW + winY):
                    snakeRed_dir = (0, TILE_SIZE)
                    currRedDir = event.key
                    idle = 0 

            elif event.key == pg.K_a:
                if redPowerToggle:

                elif not (snakeRed.left - 2 < winX):
                    snakeRed_dir = (-TILE_SIZE, 0)
                    currRedDir = event.key
                    idle = 0 

            elif event.key == pg.K_d:
                if redPowerToggle:

                elif not (snakeRed.right + 2 > WINDOW + winX):
                    snakeRed_dir = (TILE_SIZE, 0)
                    currRedDir = event.key
                    idle = 0 

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

            RANGEX = ((TILE_SIZE // 2) + winX, (WINDOW - TILE_SIZE // 2) + winX + 2, TILE_SIZE) # The '//' function is division but rounds the number down as well (into int format)
            RANGEY = ((TILE_SIZE // 2) + winY, (WINDOW - TILE_SIZE // 2) + winY + 2, TILE_SIZE)
            RANGEYRed = ((TILE_SIZE // 2) + winY + (WINDOW // 2) - 25, (WINDOW - TILE_SIZE // 2) + winY + 2, TILE_SIZE)
            RANGEYBlue = ((TILE_SIZE // 2) + winY, (WINDOW - TILE_SIZE // 2) - (WINDOW // 2) + 25 + winY + 2, TILE_SIZE)

            get_random_position = lambda: [randrange(*RANGEX), randrange(*RANGEY)]
            get_random_position_red = lambda: [randrange(*RANGEX), randrange(*RANGEYRed)]
            get_random_position_blue = lambda: [randrange(*RANGEX), randrange(*RANGEYBlue)]

            snakeBlue.move_ip(winX-prevWinX, winY-prevWinY)
            prevSnakeBlue.move_ip(winX-prevWinX, winY-prevWinY)
            power.move_ip(winX-prevWinX, winY-prevWinY)

            ### Make screen Black, call drawGrid, and redraw all tiles

            #SCREEN.fill('black')
            #drawTiles()

    

    ### Move snakeRed and Draw Tiles
    ### Beginning of time steps
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now

        ### Draw Previous snakeRed with color based on the grid tile the player went over:

        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        gridRedX = int((snakeRedX-winX-25)/50)
        gridRedY = int((snakeRedY-winY-25)/50)

        #print("idle:",idle)

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

        #print("winX:",winX,"winX + WINDOW:",winX + WINDOW)
        #print("winY:",winY,"winY + WINDOW:",winY + WINDOW)
        #print(dirsRed)

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
            redMoveCounter += 1
            
            if redMoveCounter == redSpeed:
                snakeRed.move_ip(snakeRed_dir)
                redMoveCounter = 0
                tileColors("Red")
                ### Problem (TO DO): Must have redSpeed be with
                ### respect to next tile instead of current tile.
                ### Create function to get next tile in direction

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
            blueMoveCounter += 1
            if blueMoveCounter == blueSpeed:
                snakeBlue.move_ip(snakeBlue_dir)
                blueMoveCounter = 0
                tileColors("Blue")

        tuple_add = [snakeBlue.center, snakeBlue_dir]

        ### Compare the two player
        ### Positions. If they are
        ### Equal, run playerCollision()

        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        snakeBlueX = snakeBlue.center[0]
        snakeBlueY = snakeBlue.center[1]

        gridRedX = int((snakeRedX-winX-25)/50)
        gridRedY = int((snakeRedY-winY-25)/50)

        #gridRed = grid[gridRedY][gridRedX]


        gridBlueX = int((snakeBlueX-winX-25)/50)
        gridBlueY = int((snakeBlueY-winY-25)/50)

        #gridBlue = grid[gridBlueY][gridBlueX]

        #print("gridRedY:",gridRedY,"girdBlueY",gridBlueY)
        #print("gridRedX:",gridRedX,"gridBlueX",gridBlueX)
        if gridRedY == gridBlueY and gridRedX == gridBlueX:
            playerCollision()
            print("Player Collision!!!")

        ### And then set variable for
        ### halting movement of defeated
        ### player for 3 seconds

        ### Draw all Front-End components:
        frontEnd()

        print()

    pg.display.flip()
    clock.tick(60) 