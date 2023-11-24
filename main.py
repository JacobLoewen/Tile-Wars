import pygame as pg
from random import randrange


WINDOW = 800
TILE_SIZE = 50

# 25, 775, 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)

# random.randrange(start, stop[, step]) The ", step" function specifies that within the range from start to stop, it will not get a random
# number where it does not equal (start + (step * n)), n is an element of integers. For example: For 25, 775, 50, the step is 50, so it will get
# random values in the list of 25, 75, 125, 175, 225, ..., 625, 675, 725, and 775. It will never get anything like 320 or 710. 
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_position()
SCREEN = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
currDir = pg.K_0

idle = 0

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

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -TILE_SIZE)
                dirs[pg.K_s] = 0
                currDir = event.key 
                idle = 0
            if event.key == pg.K_s and dirs[pg.K_s]:
                snake_dir = (0, TILE_SIZE)
                dirs[pg.K_w] = 0 
                currDir = event.key
                idle = 0 
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-TILE_SIZE, 0)
                dirs[pg.K_d] = 0 
                currDir = event.key 
                idle = 0
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (TILE_SIZE, 0)
                dirs[pg.K_a] = 0 
                currDir = event.key 
                idle = 0
            

    SCREEN.fill('black')
    drawGrid()
    # check borders and selfeating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        idle = 1
    # check food
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
    pg.draw.rect(SCREEN, 'red', food)
    # draw snake
    [pg.draw.rect(SCREEN, 'green', segment) for segment in segments]
    # move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())

        # Segments is a list object initialized and
        # every 'segment' is a copy of the actual
        # snake and remains in the same position.

        segments = segments[-length:]

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
        else:
            dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

    pg.display.flip()
    clock.tick(60) 