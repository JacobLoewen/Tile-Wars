from asyncio import Event
import pygame as pg
from random import randrange
from random import randint

pg.init() # Do NOT Delete

WINDOW = 750

screenX = 1920
screenY = 1080

#585
winX: int = int((screenX - 750) / 2)

#165
winY: int = int((screenY - 750) / 2)

TILE_SIZE = 50

POWER_MAX = 5

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

### Instance Variables
redPowerToggle = False
bluePowerToggle = False

redPointsCounter = 0
bluePointsCounter = 0

prevRedGrid = 0
prevBlueGrid = 0

redMoveCounter = 0
blueMoveCounter = 0

### Increments before loop in move counters, so set default as 2
redSpeed = 2
blueSpeed = 2

redSpeedDivider  = 1
blueSpeedDivider  = 1

redSpeedDividerIter = 0
blueSpeedDividerIter = 0

### Initializations for Randomization Power-Up
redRandomizer = False
blueRandomizer = False

redRandomizerIter = 0
blueRandomizerIter = 0

# dirArray = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]


i1 = 5
j1 = 0

#Default Timer:
gameTimer = 179 ### 3 Minutes (-1 second as 'GO' replaces '3:00')

#Testing Timer (Shorter for testing purposes)
# gameTimer = 29 ### 1/2 of a  Minute (-1 second as 'GO' replaces '0:30')

gameTimerText = "GO!"
eighths = 0
fourths = 0

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

colors = [blank, red_base, blue_base, red_one, blue_one, red_two, blue_two, red_player, blue_player, power_up, ultra_power_up]

### Custom Art:
blank_art = pg.image.load('tile_art/BLANK.png')
blank_art = pg.transform.scale(blank_art,(48,48))
blank_art_rect = blank_art.get_rect()

red_base_art = pg.image.load('tile_art/RED_BASE.png')
red_base_art = pg.transform.scale(red_base_art,(48,48))
red_base_art_rect = red_base_art.get_rect()

blue_base_art = pg.image.load('tile_art/BLUE_BASE.png')
blue_base_art = pg.transform.scale(blue_base_art,(48,48))
blue_base_art_rect = blue_base_art.get_rect()

red_player_art = pg.image.load('tile_art/RED_PLAYER.png')
red_player_art = pg.transform.scale(red_player_art,(48,48))
red_player_art_rect = red_player_art.get_rect()

blue_player_art = pg.image.load('tile_art/BLUE_PLAYER.png')
blue_player_art = pg.transform.scale(blue_player_art,(48,48))
blue_player_art_rect = blue_player_art.get_rect()

red_one_art = pg.image.load('tile_art/RED_ONE.png')
red_one_art = pg.transform.scale(red_one_art,(48,48))
red_one_art_rect = red_one_art.get_rect()

blue_one_art = pg.image.load('tile_art/BLUE_ONE.png')
blue_one_art = pg.transform.scale(blue_one_art,(48,48))
blue_one_art_rect = blue_one_art.get_rect()

red_two_art = pg.image.load('tile_art/RED_TWO.png')
red_two_art = pg.transform.scale(red_two_art,(48,48))
red_two_art_rect = red_two_art.get_rect()

blue_two_art = pg.image.load('tile_art/BLUE_TWO.png')
blue_two_art = pg.transform.scale(blue_two_art,(48,48))
blue_two_art_rect = blue_two_art.get_rect()

power_up_art = pg.image.load('tile_art/POWER_UP.png')
power_up_art = pg.transform.scale(power_up_art,(48,48))
power_up_art_rect = power_up_art.get_rect()

ultra_power_up_art = pg.image.load('tile_art/ULTRA_POWER_UP.png')
ultra_power_up_art = pg.transform.scale(ultra_power_up_art,(48,48))
ultra_power_up_art_rect = ultra_power_up_art.get_rect()

art = [blank_art, red_base_art, blue_base_art, red_one_art, blue_one_art, red_two_art, blue_two_art, red_player_art, blue_player_art, power_up_art, ultra_power_up_art]
art_rect = [blank_art_rect, red_base_art_rect, blue_base_art_rect, red_one_art_rect, blue_one_art_rect, red_two_art_rect, blue_two_art_rect, red_player_art_rect, blue_player_art_rect, power_up_art_rect, ultra_power_up_art_rect]


def frontEnd():
    global snakeRed
    global snakeBlue
    global colors
    global power_iter
    #global testImage
    #global testImageRect
    
    SCREEN.fill('black') ### Blanks
    drawTiles() ### Paths

    power_iter += 1
    ### Start with every 10 seconds and go up from there:
    if power_iter >= 90: ### 45 seconds * 2 half-seconds of time iteration equals 60 half seconds
    # if power_iter >= 10: ### TEMPORARY
        eraseInvincibilityBlocks()
        invincibilityBlockBlue()
        invincibilityBlockRed()
        invincibilityBlockGeneral()
        power_iter = 0

    ### Make 'base' tiles static where the first layer disappears but the player tile does not
    homeBases() ### Bases
    sideFeatures()

    ### Draw Character Tile (Colors)
    #pg.draw.rect(SCREEN, colors[RED_PLAYER], snakeRed) ### Red Player
    #pg.draw.rect(SCREEN, colors[BLUE_PLAYER], snakeBlue) ### Blue Player

    ### Draw Character Tile (Custom Art)
    red_player_art_rect.center = (snakeRed[0] + 24, snakeRed[1] + 24)
    SCREEN.blit(red_player_art, red_player_art_rect)
    blue_player_art_rect.center = (snakeBlue[0] + 24, snakeBlue[1] + 24)
    SCREEN.blit(blue_player_art, blue_player_art_rect)

    #Could make it be a 'draw character tile' function which takes the parameter of the tile in front and then decides whether it draws it or not
    # ^ is this done?

    # power_iter += 1
    # ### Start with every 10 seconds and go up from there:
    # if power_iter >= 60: ### 30 seconds * 2 half-seconds of time iteration equals 60 half seconds
    # #if power_iter >= 10: ### TEMPORARY
    #     invincibilityBlockBlue()
    #     invincibilityBlockRed()
    
    ### Draw Grid
    drawGrid()

def sideFeatures():
    global snakeRed
    global powerCountRed
    global powerCountBlue
    global POWER_MAX

    redPowerCounterTile = snakeRed.copy()
    bluePowerCounterTile = snakeRed.copy()
    redPowerCounterTile.center = (winX - 250, winY + 100)
    bluePowerCounterTile.center = (winX + WINDOW + 150, 100 + winY)
    pg.draw.rect(SCREEN, colors[POWER_UP], redPowerCounterTile)
    pg.draw.rect(SCREEN, colors[POWER_UP], bluePowerCounterTile)


    ### DRAW PLAYER SCORE AREAS:

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

    if powerCountRed > POWER_MAX:
        powerCountRed = POWER_MAX

    text_render = font.render(str(powerCountRed), True, (255, 255, 255))
    text_position = (winX - 165, winY + 67)
    SCREEN.blit(text_render, text_position)

    text_render = font.render(str(redPointsCounter), True, (255, 255, 255))
    text_position = (winX - 165, winY + 128)
    SCREEN.blit(text_render, text_position)

    ### Starting for Timer Counter:
    if i1 > 0:
        text_render = font.render(str(i1), True, (255, 255, 255))
        text_position = (winX + 355, winY - 65)
        SCREEN.blit(text_render, text_position)
    elif gameTimer != -1:
        text_render = font.render(gameTimerText, True, (255, 255, 255))
        text_position = (winX + 320, winY - 65)
        SCREEN.blit(text_render, text_position)

        

    ### Starting with Blue:

    pg.draw.line(SCREEN, colors[BLUE_TWO], ((winX + 350 + WINDOW), (winY + 750)),((winX + 350 + WINDOW), (winY)), 15)
    pg.draw.line(SCREEN, colors[BLUE_TWO], ((winX + 50 + WINDOW), (winY + 750)),((winX + 50 + WINDOW), (winY)), 15)
    pg.draw.line(SCREEN, colors[BLUE_TWO], ((winX + 350 + WINDOW), (winY)),((winX + 50 + WINDOW), (winY)), 15)
    pg.draw.line(SCREEN, colors[BLUE_TWO], ((winX + 350 + WINDOW), (winY + 750)),((winX + 50 + WINDOW), (winY + 750)), 15)

    ### Create the font:
    font = pg.font.Font('Questrial-Regular.ttf', 65)
    text_render = font.render("x ", True, (255, 255, 255))
    text_position = (winX + 941, winY + 63)
    SCREEN.blit(text_render, text_position)

    if powerCountBlue > POWER_MAX:
        powerCountBlue = POWER_MAX

    text_render = font.render(str(powerCountBlue), True, (255, 255, 255))
    text_position = (winX + 985, winY + 67)
    SCREEN.blit(text_render, text_position)

    text_render = font.render(str(bluePointsCounter), True, (255, 255, 255))
    text_position = (winX + 985, winY + 132)
    SCREEN.blit(text_render, text_position)

def drawWinLose(winner: str, draw: bool):
    global redPointsCounter
    global bluePointsCounter

    SCREEN.fill('black') ### Blanks
    drawTiles() ### Paths
        ### Make 'base' tiles static where the first layer disappears but the player tile does not
    homeBases() ### Bases
    sideFeatures()

    ### Draw Character Tile
    pg.draw.rect(SCREEN, colors[RED_PLAYER], snakeRed) ### Red Player
    pg.draw.rect(SCREEN, colors[BLUE_PLAYER], snakeBlue) ### Blue Player

    drawGrid()


    font = pg.font.Font('Questrial-Regular.ttf', 65)

    ### Draw Win and Lose
    if draw:
        if winner == "Red":
            text_render = font.render("YOU", True, (255, 0, 0))
            text_position = (winX - 265, winY + 300)
            SCREEN.blit(text_render, text_position)

            text_render = font.render("WIN!", True, (255, 0, 0))
            text_position = (winX - 262, winY + 380)
            SCREEN.blit(text_render, text_position)

            text_render = font.render("YOU", True, (0, 0, 255))
            text_position = (winX + 880, winY + 300)
            SCREEN.blit(text_render, text_position)

            text_render = font.render("LOSE!", True, (0, 0, 255))
            text_position = (winX + 860, winY + 380)
            SCREEN.blit(text_render, text_position)
            
        elif winner == "Blue":
            text_render = font.render("YOU", True, (255, 0, 0))
            text_position = (winX - 265, winY + 300)
            SCREEN.blit(text_render, text_position)

            text_render = font.render("LOSE!", True, (255, 0, 0))
            text_position = (winX - 285, winY + 380)
            SCREEN.blit(text_render, text_position)

            text_render = font.render("YOU", True, (0, 0, 255))
            text_position = (winX + 880, winY + 300)
            SCREEN.blit(text_render, text_position)

            text_render = font.render("WIN!", True, (0, 0, 255))
            text_position = (winX + 883, winY + 380)
            SCREEN.blit(text_render, text_position)
        
        elif winner == "Tie":
            text_render = font.render("TIE!", True, (255, 0, 0))
            text_position = (winX - 255, winY + 300)
            SCREEN.blit(text_render, text_position)

            text_render = font.render("TIE!", True, (0, 0, 255))
            text_position = (winX + 900, winY + 300)
            SCREEN.blit(text_render, text_position)

    elif not draw:
        text_render = font.render("", True, (255, 255, 255))
        text_position = (winX + 941, winY + 63)
        SCREEN.blit(text_render, text_position)

### TO DO: In order to remove old invincibility blocks, quick way would be to go through the entire map and remove all
### tiles with numbers 9 (power-up) or 10 (ultra-power-up). Can make a more efficient method for this another time.
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
        invincibilityBlockRed() ### Repeat function if not able to place item there
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

    ### Randomized Chance of Ultra Power-Up
    randomNum = randint(1, 3)
    if randomNum == 1:
        ultraPower.center = get_random_position()
        pg.draw.rect(SCREEN, colors[ULTRA_POWER_UP], ultraPower)

        ### Add power_up to grid
        powerX = ultraPower.center[0]
        powerY = ultraPower.center[1]

        powerGridX = int((powerX-winX-25)/50)
        powerGridY = int((powerY-winY-25)/50)

        if grid[powerGridY][powerGridX] == 1 or grid[powerGridY][powerGridX] == 2: ### Redo method if spawned on a base
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

def eraseInvincibilityBlocks():
    for posX in range(25, 775, 50):
        for posY in range (25, 775, 50):
            gridX = int((posX-25)/50)
            gridY = int((posY-25)/50)
            if grid[gridY][gridX] == 9 or grid[gridY][gridX] == 10:
                grid[gridY][gridX] = BLANK

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
            
            grid[gridY][gridX] = BLUE_BASE
            
            art_rect[grid[gridY][gridX]].center = (tile[0], tile[1])
            SCREEN.blit(art[grid[gridY][gridX]], art_rect[grid[gridY][gridX]].center)
    
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
               
            grid[gridY][gridX] = RED_BASE

            art_rect[grid[gridY][gridX]].center = (tile[0], tile[1])
            SCREEN.blit(art[grid[gridY][gridX]], art_rect[grid[gridY][gridX]].center)

def playerCollision():
    ### Runs if the players are on the same tile
    
    global powerCountRed
    global powerCountBlue
    global redSpeed
    global blueSpeed
    global redMoveCounter
    global blueMoveCounter
    global redSpeedDivider 
    global blueSpeedDivider 

    ### Winner will respawn upon collision
    if redPointsCounter < bluePointsCounter:
        ### Blue respawns after 3 seconds and Red's count decreases by 1 (for now)
        snakeBlue.center = (375 + winX, 75 + winY)
        blueSpeed = 40 ### Wait for 5 seconds
        blueMoveCounter = 0
    elif redPointsCounter > bluePointsCounter:
        ### Red respawns after 5 seconds and Blue's count decreases by 1 (for now)
        snakeRed.center = (375 + winX, 675 + winY)
        redSpeed = 40
        redMoveCounter = 0
    elif redPointsCounter == bluePointsCounter:
        ### BOTH respawn after 5 seconds
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

            art_rect[grid[y][x]].center = (pixelX, pixelY)

            SCREEN.blit(art[grid[y][x]], art_rect[grid[y][x]].center)

def speedAlter(player: str):
    global snakeRed
    global snakeBlue
    global redSpeed
    global blueSpeed
    global redSpeedDivider 
    global blueSpeedDivider 

    if player == "Red":

        ### Get grid of snakeRed currently and then respectively 
        ### increment to wherever shows the next tile
        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        ### Grid may go out of bounds. If this is the case, return
        ### 1 as the speed.
        try:
            gridRedX = int((snakeRedX-winX-25)/50)
            gridRedY = int((snakeRedY-winY-25)/50)
            currGrid = grid[gridRedY][gridRedX]

            colorRed = 0
            if currGrid == 0:
                redSpeed = 6 / redSpeedDivider 
            elif currGrid == 1:
                redSpeed = 2 / redSpeedDivider 
            elif currGrid == 3:
                redSpeed = 4 / redSpeedDivider 
            elif currGrid == 5:
                redSpeed = 2 / redSpeedDivider 
            elif currGrid == 4:
                redSpeed = 6 / redSpeedDivider 
            elif currGrid == 6:
                redSpeed = 8 / redSpeedDivider 
            elif currGrid == 9:
                redSpeed = 6 / redSpeedDivider 
            elif currGrid == 10:
                redSpeed = 10 / redSpeedDivider
        except Exception:
            redSpeed = 2 / redSpeedDivider 

    if player == "Blue":
        ### Get grid of snakeRed currently and then respectively 
        ### increment to wherever shows the next tile
        snakeBlueX = snakeBlue.center[0]
        snakeBlueY = snakeBlue.center[1]

        ### Grid may go out of bounds. If this is the case, return
        ### 1 as the speed.
        try:
            gridBlueX = int((snakeBlueX-winX-25)/50)
            gridBlueY = int((snakeBlueY-winY-25)/50)
            currGrid = grid[gridBlueY][gridBlueX]

            colorBlue = 0
            if currGrid == 0:
                blueSpeed = 6 / blueSpeedDivider 
            elif currGrid == 2:
                blueSpeed = 2 / blueSpeedDivider 
            elif currGrid == 4:
                blueSpeed = 4 / blueSpeedDivider 
            elif currGrid == 6:
                blueSpeed = 2 / blueSpeedDivider 
            elif currGrid == 3:
                blueSpeed = 6 / blueSpeedDivider 
            elif currGrid == 5:
                blueSpeed = 8 / blueSpeedDivider 
            elif currGrid == 9:
                blueSpeed = 6 / blueSpeedDivider 
            elif currGrid == 10:
                blueSpeed = 10 / blueSpeedDivider
        except Exception:
            blueSpeed = 2 / blueSpeedDivider 

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
        elif prevRedGrid == 10:
            colorRed = 0
            powerCountRed += 3

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
        elif prevBlueGrid == 10:
            colorBlue = 0
            powerCountBlue += 3

        pg.draw.rect(SCREEN, colors[colorBlue], prevSnakeBlue)

        ### Get the pixel coords of tile and convert to grid coords and then put in grid
        prevSnakeBlueX = prevSnakeBlue.center[0]
        prevSnakeBlueY = prevSnakeBlue.center[1]

        prevBlueGridX = int((prevSnakeBlueX-winX-25)/50)
        prevBlueGridY = int((prevSnakeBlueY-winY-25)/50)

        grid[prevBlueGridY][prevBlueGridX] = colorBlue ### Set the color of the PREVIOUS snakeRed
        
        prevBlueGrid = grid[gridBlueY][gridBlueX] ### Get color of tile that snakeBlue is now on
    
### This while loop is solely for 5 second countdown
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYUP:
            if event.key == pg.K_c:
                redPowerToggle = False
            elif event.key == pg.K_m:
                bluePowerToggle = False
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
                redPowerToggle = True
            if event.key == pg.K_m:
                bluePowerToggle = True

            ### Movement
            if event.key == pg.K_w:
                if redPowerToggle:
                    if powerCountRed >= 3:
                        redSpeedDivider = 2
                        powerCountRed -= 3
                        print("W Power-Up")
                elif not (snakeRed.top - 2 < winY):
                    snakeRed_dir = (0, -TILE_SIZE)
                    currRedDir = event.key

            elif event.key == pg.K_s:
                if redPowerToggle:
                    if powerCountRed >= 4:
                        blueRandomizer = True
                        blueRandomizerIter = 32 ### 32 one-eighth seconds = 4 seconds
                        powerCountRed -= 4
                    ### Create Randomization Controls Power-Up
                    print("S Power-Up")
                elif not (snakeRed.bottom + 2 > WINDOW + winY):
                    snakeRed_dir = (0, TILE_SIZE)
                    currRedDir = event.key

            elif event.key == pg.K_a:
                if redPowerToggle:
                    print("A Power-Up")
                elif not (snakeRed.left - 2 < winX):
                    snakeRed_dir = (-TILE_SIZE, 0)
                    currRedDir = event.key

            elif event.key == pg.K_d:
                if redPowerToggle:
                    print("D Power-Up")
                elif not (snakeRed.right + 2 > WINDOW + winX):
                    snakeRed_dir = (TILE_SIZE, 0)
                    currRedDir = event.key

            ### Blue Player:
            if event.key == pg.K_UP:
                if bluePowerToggle:
                    if powerCountBlue >= 3:
                        powerCountBlue -= 3
                        blueSpeedDivider = 2
                        print("UP Power-Up")
                elif not (snakeBlue.top - 2 < winY):
                    snakeBlue_dir = (0, -TILE_SIZE)
                    currBlueDir = event.key

            elif event.key == pg.K_DOWN:
                if bluePowerToggle:
                    print("DOWN Power-Up")
                elif not (snakeBlue.bottom + 2 > WINDOW + winY):
                    snakeBlue_dir = (0, TILE_SIZE)
                    currBlueDir = event.key

            elif event.key == pg.K_LEFT:
                if bluePowerToggle:
                    print("LEFT Power-Up")
                elif not (snakeBlue.left - 2 < winX):
                    snakeBlue_dir = (-TILE_SIZE, 0)
                    currBlueDir = event.key

            elif event.key == pg.K_RIGHT:
                if bluePowerToggle:
                    print("RIGHT Power-Up")
                elif not (snakeBlue.right + 2 > WINDOW + winX):
                    snakeBlue_dir = (TILE_SIZE, 0)
                    currBlueDir = event.key


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

    # font = pg.font.Font('Questrial-Regular.ttf', 65)
    # text_render = font.render(str(i1), True, (255, 255, 255))
    # text_position = (winX + 355, winY - 65)
    # SCREEN.blit(text_render, text_position)

    # print()

    if i1 > 0: # Count from 5
        if j1 < (8): # (8 * 1/8 seconds)
            time_now = pg.time.get_ticks()
            if time_now - time > time_step:
                time = time_now
                frontEnd()
                print("Printing i")
                j1 += 1
            #clock.tick(60)
        ### Write number at top of grid
        else:
            i1 -= 1
            j1 = 0
    else:
        break

    ### Move snakeRed and Draw Tiles
    ### Beginning of time steps
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now

        ### Time-Out Power-UPs with time limit here:
        if redSpeedDivider  == 2:
            redSpeedDividerIter += 1
            #print("redSpeedDividerIter",redSpeedDividerIter)
            if redSpeedDividerIter == 24: ### 3 (* 8 * 1/8) seconds
                redSpeedDivider = 1
                redSpeedDividerIter = 0

        if blueSpeedDivider == 2:
            blueSpeedDividerIter += 1
            if blueSpeedDividerIter == 24:
                blueSpeedDivider = 1
                blueSpeedDividerIter = 0

        ### Draw Previous snakeRed with color based on the grid tile the player went over:

        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        gridRedX = int((snakeRedX-winX-25)/50)
        gridRedY = int((snakeRedY-winY-25)/50)

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
                #snakeRed.move_ip(snakeRed_dir)
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
                #snakeBlue.move_ip(snakeBlue_dir)
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

        ### And then set variable for
        ### halting movement of defeated
        ### player for 3 seconds

        ### Draw all Front-End components:
        frontEnd()

    pg.display.flip()
    clock.tick(60) 




















### This while loop has full respect to Players after the 5 seconds
while True:
    # print("gameTimer:",gameTimer)
    if gameTimer == -1:
        break
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYUP:
            if event.key == pg.K_c:
                redPowerToggle = False
            elif event.key == pg.K_m:
                bluePowerToggle = False
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
                redPowerToggle = True
            if event.key == pg.K_m:
                bluePowerToggle = True

            ### Movement
            if event.key == pg.K_w:
                if redPowerToggle:
                    if powerCountRed >= 3:
                        redSpeedDivider = 2
                        powerCountRed -= 3
                        print("W Power-Up")
                elif not (snakeRed.top - 2 < winY):
                    snakeRed_dir = (0, -TILE_SIZE)
                    currRedDir = event.key

            elif event.key == pg.K_s:
                if redPowerToggle:
                    if powerCountRed >= 4:
                        blueRandomizer = True
                        blueRandomizerIter = 32 ### 32 one-eighth seconds = 4 seconds
                        powerCountRed -= 4
                    ### Create Randomization Controls Power-Up
                    print("S Power-Up")
                elif not (snakeRed.bottom + 2 > WINDOW + winY):
                    snakeRed_dir = (0, TILE_SIZE)
                    currRedDir = event.key

            elif event.key == pg.K_a:
                if redPowerToggle:
                    ### Start Coding the 3x3 Power-Up Area
                    if powerCountRed >= 5:
                        snakeRedX = snakeRed.center[0]
                        snakeRedY = snakeRed.center[1]
                        gridRedX = int((snakeRedX-winX-25)/50)
                        gridRedY = int((snakeRedY-winY-25)/50)
                        for i in range(3):
                            for j in range(3):
                                try:
                                    grid[gridRedY - 1 + j][gridRedX - 1 + i] = RED_TWO
                                    print("WORKING?")
                                except Exception:
                                    print("EXCEPTION!!!")
                                    continue
                        powerCountRed -= 5
                    print("A Power-Up")
                elif not (snakeRed.left - 2 < winX):
                    snakeRed_dir = (-TILE_SIZE, 0)
                    currRedDir = event.key

            elif event.key == pg.K_d:
                if redPowerToggle:
                    print("D Power-Up")
                elif not (snakeRed.right + 2 > WINDOW + winX):
                    snakeRed_dir = (TILE_SIZE, 0)
                    currRedDir = event.key

            ### Blue Player:
            if event.key == pg.K_UP:
                if bluePowerToggle:
                    if powerCountBlue >= 3:
                        powerCountBlue -= 3
                        blueSpeedDivider = 2
                        print("UP Power-Up")
                elif not (snakeBlue.top - 2 < winY):
                    snakeBlue_dir = (0, -TILE_SIZE)
                    currBlueDir = event.key

            elif event.key == pg.K_DOWN:
                if bluePowerToggle:
                    if powerCountBlue >= 4:
                        redRandomizer = True
                        redRandomizerIter = 32 ### 32 one-eighth seconds = 4 seconds
                        powerCountBlue -= 4
                    ### Create Randomization Controls Power-Up
                    print("DOWN Power-Up")
                elif not (snakeBlue.bottom + 2 > WINDOW + winY):
                    snakeBlue_dir = (0, TILE_SIZE)
                    currBlueDir = event.key

            elif event.key == pg.K_LEFT:
                if bluePowerToggle:
                    ### Start Coding the 3x3 Power-Up Area
                    if powerCountBlue >= 5:
                        snakeBlueX = snakeBlue.center[0]
                        snakeBlueY = snakeBlue.center[1]
                        gridBlueX = int((snakeBlueX-winX-25)/50)
                        gridBlueY = int((snakeBlueY-winY-25)/50)
                        for i in range(3):
                            for j in range(3):
                                try:
                                    grid[gridBlueY - 1 + j][gridBlueX - 1 + i] = BLUE_TWO
                                    print("WORKING?")
                                except Exception:
                                    print("EXCEPTION!!!")
                                    continue
                        powerCountBlue -= 5
                    print("LEFT Power-Up")
                elif not (snakeBlue.left - 2 < winX):
                    snakeBlue_dir = (-TILE_SIZE, 0)
                    currBlueDir = event.key

            elif event.key == pg.K_RIGHT:
                if bluePowerToggle:
                    print("RIGHT Power-Up")
                elif not (snakeBlue.right + 2 > WINDOW + winX):
                    snakeBlue_dir = (TILE_SIZE, 0)
                    currBlueDir = event.key


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

        ### Get one second
        eighths += 1
        if eighths == 8:
            eighths = 0
            addedString = ""

            if (gameTimer % 60) < 10:
                addedString = "0"
            gameTimerText = str(int(gameTimer/60)) + ":" + addedString + str(gameTimer % 60)
            gameTimer -= 1

        ### Time-Out Power-UPs with time limit here:
        if redSpeedDivider == 2:
            redSpeedDividerIter += 1
            #print("redSpeedDividerIter",redSpeedDividerIter)
            if redSpeedDividerIter == 24: ### Expires after 3 seconds (24 * one-eighth of a second = 3 seconds)
                redSpeedDivider = 1
                redSpeedDividerIter = 0

        if blueSpeedDivider == 2:
            blueSpeedDividerIter += 1
            if blueSpeedDividerIter == 24: ### Expires after 3 seconds (24 * one-eighth of a second = 3 seconds)
                blueSpeedDivider = 1
                blueSpeedDividerIter = 0


        if redRandomizer:
            redRandomizerIter -= 1
            if redRandomizerIter == 0:
                redRandomizer = False  

        if blueRandomizer:
            blueRandomizerIter -= 1
            if blueRandomizerIter == 0:
                blueRandomizer = False          

        ### Draw Previous snakeRed with color based on the grid tile the player went over:

        snakeRedX = snakeRed.center[0]
        snakeRedY = snakeRed.center[1]

        gridRedX = int((snakeRedX-winX-25)/50)
        gridRedY = int((snakeRedY-winY-25)/50)

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

        tuple_add = [snakeRed.center, snakeRed_dir]

        ### Draw Previous snakeBlue with color based on the grid tile the player went over:

        snakeBlueX = snakeBlue.center[0]
        snakeBlueY = snakeBlue.center[1]

        gridBlueX = int((snakeBlueX-winX-25)/50)
        gridBlueY = int((snakeBlueY-winY-25)/50)

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

        gridBlueX = int((snakeBlueX-winX-25)/50)
        gridBlueY = int((snakeBlueY-winY-25)/50)

        if gridRedY == gridBlueY and gridRedX == gridBlueX:
            playerCollision()
            print("Player Collision!!!")

        ### And then set variable for
        ### halting movement of defeated
        ### player for 5 seconds

        ### Draw all Front-End components:
        frontEnd()
        # print()

    pg.display.flip()
    clock.tick(60) 

### Once the game is done:
draw = True

winner = "Tie"

if redPointsCounter > bluePointsCounter:
    winner = "Red"
elif redPointsCounter < bluePointsCounter:
    winner = "Blue"

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

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

            snakeBlue.move_ip(winX-prevWinX, winY-prevWinY)
            prevSnakeBlue.move_ip(winX-prevWinX, winY-prevWinY)
            power.move_ip(winX-prevWinX, winY-prevWinY)

    ### Move snakeRed and Draw Tiles
    ### Beginning of time steps
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now

        ### Get half a second to display the "YOU WIN" and "YOU LOSE" messages
        fourths += 1
        if fourths == 4:
            fourths = 0
            ### Make blinking effect for the Win and Lose messages
            draw = not draw
            drawWinLose(winner, draw)

    pg.display.flip()
    clock.tick(60) 