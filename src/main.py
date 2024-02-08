### IMPORTS ###
import pygame as pg
import random
import time

import util
import util.debug as debug
import util.graphic as graphic

import entity
import entity.player
import entity.npc

import item
import item.consumable

import board
import board.tile as tile


### INITIATE SETTINGS ###
DATA_PATH = "data/"
controls = util.define_controls(DATA_PATH)
settings = util.define_settings(DATA_PATH)


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
game_board = board.Board(
    controls, graphic.tile_width, screen_dimensions, 
    (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 
    True
)

'''
cobble_floor, cobble_wall = tile.cobble_floor, tile.cobble_wall
room1 = game_board.build_room((0, 5), (5, 10), cobble_floor, cobble_wall)
room2 = game_board.build_room((6, 5), (10, 10), cobble_floor, cobble_wall)
game_board.connect_rooms(room1, room2)
'''
game_board.generate_floor(7)

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

## ENTITY THAT WILL FOLLOW THE PLAYER
entity_bgc, entity_fgc = pg.color.Color('blue'), pg.color.Color('white')
random_floor = game_board.get_random_floor()
adoring_fan = entity.npc.NPC(
    (random_floor.tile_x, random_floor.tile_y),
    (6, 6),
    entity_bgc, entity_fgc
)
game_board.entities.add(adoring_fan)


game_board._update()

### GAME LOOP ###
running = True
while running:
    #if pg.key.get_pressed()[pg.K_BACKQUOTE]: debug.debug()

    check_input = False
    pg.display.flip()
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False
        if event.type == pg.KEYDOWN: check_input = True

    screen.fill("black")
    game_board.update(check_input)
    game_board.draw(screen)

pg.quit()
exit(0)
