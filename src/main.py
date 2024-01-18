### IMPORTS ###
import pygame as pg
import copy

import board
import board.tile as tile
import board.entity as entity

### TEMPORARY CONSTANTS ###
SCREEN_WIDTH = 1028
SCREEN_HEIGHT = 512
TILESET_PATH = "data/tiles.png"



### PYGAME INITIALIZATION ###
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()


### PREPARING BOARD ###
board = board.Board()

# random colors
red = pg.color.Color('red')
green = pg.color.Color('green')
blue = pg.color.Color('blue')
black = pg.color.Color('black')

# temporary player entity
player = entity.Entity(0, 4, green, red, 0, 0)
board.entities.add(player)

# size of the board (for now)
width, height = 5, 14
for y in range(height):
    for x in range(width):
        if green.r < 245: green.r += 5
        else: green.r %= 255
        new_tile = tile.Tile('floor', 12, 2, green, black, x, y)
        board.tiles.add(new_tile)


### GAME LOOP ###
running = True
while running:
    # utility stuff
    pg.display.flip()
    clock.tick(60)
    for event in pg.event.get(): 
        if event.type == pg.QUIT: running = False

    # clear screen
    screen.fill("black")

    # draw and update board
    board.update()
    board.draw(screen)


### CLEAN EXIT ###
pg.quit()
exit(0)
