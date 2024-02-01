### IMPORTS ###
import pygame as pg
import random
import time

import util.init as init
import util.debug as debug
import util.graphic as graphic

import entity

import item
import item.consumable

import board
import board.tile as tile


### INITIATE SETTINGS ###
DATA_PATH = "data/"
controls = init.define_controls(DATA_PATH)
settings = init.define_settings(DATA_PATH)


### TEMPORARY CONSTANTS ###
SCREEN_WIDTH  = int(settings['screen_width'])
SCREEN_HEIGHT = int(settings['screen_height'])
screen_dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)


### PYGAME INITIALIZATION ###
pg.init()
pg.display.set_caption("🍃Leaflings🍂")
screen = pg.display.set_mode(screen_dimensions)
clock = pg.time.Clock()


### PREPARING BOARD ###
game_board = board.Board(controls, graphic.tile_width, screen_dimensions)

'''
## CODE FOR MAKING THE PLAYER
player_bgc, player_fgc = pg.color.Color('green'), pg.color.Color('white')
random_floor = game_board.get_random_floor()
player = entity.player.Player(
    (random_floor.tile_x, random_floor.tile_y),
    (0, 4),
    player_bgc, player_fgc 
)
player.inventory.append(item.consumable.health_potion)
game_board.entities.add(player)
'''

i = 0
white = (255, 255, 255)
transparent = (0, 0, 0, 0)
for partition in game_board.bsp(4):
    pg.draw.rect(screen, white, partition, width=3)
    i += 1
#    partition.build_room(game_board, board.tile.cobble_floor, board.tile.cobble_wall)

### GAME LOOP ###
running = True
while running:
#    if pg.key.get_pressed()[pg.K_BACKQUOTE]: debug.debug()

    check_input = False
    pg.display.flip()
    clock.tick(60)
    for event in pg.event.get(): 
        if event.type == pg.QUIT: running = False
        if event.type == pg.KEYDOWN: check_input = True

    #screen.fill("black")
    game_board.update(check_input)
    game_board.draw(screen)

pg.quit()
exit(0)
