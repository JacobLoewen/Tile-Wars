import pygame as pg
from random import randrange


WINDOW = 750
TILE_SIZE = 50

# 25, 775, 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) # The '//' function is division but rounds the number down as well (into int format)

# random.randrange(start, stop[, step]) The ", step" function specifies that within the range from start to stop, it will not get a random
# number where it does not equal (start + (step * n)), n is an element of integers. For example: For 25, 775, 50, the step is 50, so it will get
# random values in the list of 25, 75, 125, 175, 225, ..., 625, 675, 725, and 775. It will never get anything like 320 or 710. 
# These values represent the CENTER of the tile
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

### Create grid | In order to exchange grid -> positioning, do formula y = 25 + 50x where x is the position of the tile in range (0, 14). For
# positioning -> grid, it will be x = (y - 25)/50 where y is the position number from range (25, 775). 
grid = [[0 for _ in range(WINDOW // TILE_SIZE)] for _ in range(WINDOW // TILE_SIZE)] # deep copy

tile = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake = tile.copy()
#snake.center = get_random_position()
snake.center = (375, 675)
length = 1
snake_dir = (0, 0)
time, time_step = 0, 110*2
food = snake.copy()
food.center = get_random_position()
SCREEN = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
currDir = pg.K_0
prevSnake = snake.copy()

idle = 1

### Colors:
base_red = (102, 0, 0, 255)
base_blue = (0, 0, 102, 255)

character_red = (255, 0, 0, 255)
character_blue = (0, 0, 204, 255)

red_lvl_one = (255, 102, 102, 255)
blue_lvl_one = (102, 102, 255, 255)

red_lvl_two = (255, 51, 51, 255)
blue_lvl_two = (51, 51, 255, 255)

def homeBases():
    # Setup Blue home base:
    global SCREEN
    global tile
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
            print(str(posX) + ", " + str(h))
            tile.center = (posX, posY)
            pg.draw.rect(SCREEN, base_blue, tile)
    
    # Setup Red home base:
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
            tile.center = (posX, posY)
            pg.draw.rect(SCREEN, base_red, tile)

def drawGrid():
    global TILE_SIZE
    global WINDOW
    global SCREEN
    WINDOW_WIDTH = WINDOW
    WINDOW_HEIGHT = WINDOW
    for x in range(0, WINDOW_WIDTH, TILE_SIZE):
        for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
            rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pg.draw.rect(SCREEN, 'white', rect, 1)

SCREEN.fill('black')
drawGrid()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            print("left: " + str(snake.left) + ", right: " + str(snake.right) + ".")
            print("top: " + str(snake.top) + ", bottom: " + str(snake.bottom) + ".")

            ### Key is Top; Previous motion was NOT downwards; Tile is NOT currently at a place where it can not be.
            if event.key == pg.K_w and dirs[pg.K_w] and not (snake.top - 2 < 0):
                snake_dir = (0, -TILE_SIZE)
                # snake.move_ip(snake_dir)
                dirs[pg.K_s] = 0
                currDir = event.key 
                idle = 0
            elif event.key == pg.K_s and dirs[pg.K_s] and not (snake.bottom + 2 > WINDOW):
                snake_dir = (0, TILE_SIZE)
                # snake.move_ip(snake_dir)
                dirs[pg.K_w] = 0 
                currDir = event.key
                idle = 0 
            elif event.key == pg.K_a and dirs[pg.K_a] and not(snake.left - 2 < 0):
                snake_dir = (-TILE_SIZE, 0)
                # snake.move_ip(snake_dir)
                dirs[pg.K_d] = 0 
                currDir = event.key 
                idle = 0
            elif event.key == pg.K_d and dirs[pg.K_d] and not (snake.right + 2 > WINDOW):
                snake_dir = (TILE_SIZE, 0)
                # snake.move_ip(snake_dir)
                dirs[pg.K_a] = 0 
                currDir = event.key 
                idle = 0
            elif snake.left - 2 < 0 or snake.right + 2 > WINDOW or snake.top - 2 < 0 or snake.bottom + 2 > WINDOW:
                idle = 1
                print("IDLE IS 1: " + str(idle))



    # check borders. If so, reset
    #self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    # if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW: #or self_eating:
        #snake.center, food.center = get_random_position(), get_random_position()
        #length, snake_dir = 1, (0, 0)
        #idle = 1



    # check food
    #if snake.center == food.center:
    #    food.center = get_random_position()
    #   length += 1
    
    
    # draw food
    #pg.draw.rect(SCREEN, 'white', food)
    
    # draw snake
    #[pg.draw.rect(SCREEN, 'green', segment) for segment in segments]


    ### Move Snake and Draw Tiles
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now

        #if not(snake.left - 2 < 0 or snake.right + 2 > WINDOW or snake.top - 2 < 0 or snake.bottom + 2 > WINDOW):
        #    snake.move_ip(snake_dir)


        ### do not move in place if the direction will go out of bounds

        tuple_add = [snake.center, snake_dir]

        print(tuple_add)

        tuple_sum_0 = sum(t[0] for t in tuple_add)
        tuple_sum_1 = sum(t[1] for t in tuple_add)

        if snake.left - 2 < 0 and dirs[pg.K_d] == 0:
            print("Can no longer go left")
        elif snake.right + 2 > WINDOW and dirs[pg.K_a] == 0:
            print("Can no longer go right")
        elif snake.top - 2 < 0 and dirs[pg.K_s] == 0:
            print("Can no longer go up")
        elif snake.bottom + 2 > WINDOW and dirs[pg.K_w] == 0:
            print("Can no longer go down")
        else:
            snake.move_ip(snake_dir)
        

        #move in place

        #if not (snake.left - 2 < 0 or snake.right + 2 > WINDOW or snake.top - 2 < 0 or snake.bottom + 2 > WINDOW):
        #    snake.move_ip(snake_dir)
        #print("left: " + str(snake.left) + ", right: " + str(snake.right) + ".")


        # Get tile in snake_dir

        print(snake.center)

        #snake_dir_color

        lightYellow = (255, 153, 153, 127)
        #try:
            #print(SCREEN.get_at(snake.center))
        #except:
            #print("No color at this point!")

        ### Draw Previous Snake
        pg.draw.rect(SCREEN, red_lvl_one, prevSnake)

        ### Make 'base' tiles static where the first layer disappears but the player tile does not
        homeBases()

        ### Draw Character Tile
        pg.draw.rect(SCREEN, character_red, snake)


        prevSnake = snake.copy()


        #segments.append(snake.copy())

        # Segments is a list object initialized and
        # every 'segment' is a copy of the actual
        # snake and remains in the same position.

        #segments = segments[-length:]

        # The length feature only keeps the most
        # recent segements of the snake so that
        # it can appear as if the snake is actually
        # moving, even though all the squares are
        # in stop motion!


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
        ### Testing no 'else' so that the tile can not move past border
        #else:
            #dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

    pg.display.flip()
    clock.tick(60) 