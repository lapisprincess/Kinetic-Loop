### IMPORTS ###
import pygame as pg
import random
import time
import sys

import util
from util.graphic import tile_width
from util.debug import debug

import entity
import entity.player
import entity.npc
from entity.trait import *

import item
import item.consumable

import board
import board.tile as tile
import board.floor_generator as floorgen

import gui



### GET COMMAND LINE INPUTS ###
arguments = sys.argv

if 'nofov' in arguments: setFOV = False
else: setFOV = True

if 'testroom' in arguments: testroom = True
else: testroom = False



### INITIATE SETTINGS ###
DATA_PATH = "data/"
controls = util.define_controls(DATA_PATH)
settings = util.define_settings(DATA_PATH)


### CONSTANTS ###
SCREEN_WIDTH  = int(settings['screen_width'])
SCREEN_HEIGHT = int(settings['screen_height'])
screen_dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)


### PYGAME INITIALIZATION ###
pg.init()
pg.display.set_caption("🍃Leaflings🍂")
screen = pg.display.set_mode(screen_dimensions)
clock = pg.time.Clock()

## CUTE CURSOR ##
cursor_img = pg.image.load("data/cursor.png")
cursor_pressed_img = pg.image.load("data/cursor_pressed.png")
cursor = pg.cursors.Cursor((0, 0), cursor_img)
cursor_pressed = pg.cursors.Cursor((0, 0), cursor_pressed_img)
pg.mouse.set_cursor(cursor)



### PREPARING BOARD ###
game_board = board.Board(
    controls, tile_width, (500, 500), 
    visibility = setFOV
)

if testroom:
    cobble_floor, cobble_wall = tile.cobble_floor, tile.cobble_wall
    room1 = game_board.build_room((0, 5), (5, 10), cobble_floor, cobble_wall)
    room2 = game_board.build_room((15, 5), (10, 10), cobble_floor, cobble_wall)
    room3 = game_board.build_room((0, 15), (5, 15), cobble_floor, cobble_wall)
    game_board.connect_rooms(room2, room1)
    game_board.connect_rooms(room3, room1)
else: floorgen.generate_floor(game_board, 8, tile.grass, tile.woodwall)


### FONTS ###
li_font = pg.font.Font("data/font.otf", size=14)
h1_font = pg.font.Font("data/font.otf", size=20)

### GUI INITIALIZATION ###
all_fonts = { 'li': li_font, 'h1': h1_font, }
game_gui = gui.GUI(screen_dimensions, all_fonts, game_board)
game_board.log = game_gui.log



## CODE FOR MAKING THE PLAYER
player_bgc, player_fgc = pg.color.Color('green'), pg.color.Color('white')
random_floor = game_board.get_random_floor()

player = entity.player.Player(
    (random_floor.tile_x, random_floor.tile_y),
    (0, 4),
    player_bgc, player_fgc,
    game_board
) 
game_board.add_entity(player)

player.inventory.append(item.consumable.health_potion)
player.traits.add(controllable)

## TEST ENTITY
entity_bgc, entity_fgc = pg.color.Color('blue'), pg.color.Color('white')
random_floor = game_board.get_random_floor()

adoring_fan = entity.npc.NPC(
    (random_floor.tile_x, random_floor.tile_y),
    (6, 6),
    entity_bgc, entity_fgc,
    game_board
) 
game_board.add_entity(adoring_fan)

adoring_fan.info["Name"] = "Adoring fan"
adoring_fan.info["HP"] = 3
adoring_fan.info["Love for PC"] = 1000000

adoring_fan.traits.add(wandering)
adoring_fan.traits.add(hostile)




### GAME LOOP ###
running = True
while running:
    if pg.key.get_pressed()[pg.K_ESCAPE] and game_gui.popout != None: 
        game_gui.popout = None

    pg.display.flip()
    clock.tick(30)

    check_input = False

    for event in pg.event.get():
        if event.type == pg.QUIT: running = False

        if event.type == pg.MOUSEWHEEL:
            if event.y >= 0: direction = 'up'
            else: direction = 'down'
            game_gui.scroll(direction)

        if event.type == pg.MOUSEBUTTONDOWN: 
            pg.mouse.set_cursor(cursor_pressed)
            if game_gui.popout == None: game_gui.menu.click()
        else: pg.mouse.set_cursor(cursor)

        # process keystrokes
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKQUOTE and not game_gui.log.typing:
                game_gui.log.type_txt = "db> ";
                game_gui.log.typing = True;
            if event.key == pg.K_RETURN and game_gui.log.typing:
                debug(game_board, game_gui.log) 
            if game_gui.log.typing:
                game_gui.log.type(event)
            check_input = True


    screen.fill("black")
    if game_gui.popout == None and not game_gui.log.typing:
        game_board.update(check_input)
        game_gui.update()
    elif game_gui.popout != None:
        game_gui.popout.update()

    game_gui.info.set_info(game_board.info)
    game_gui.draw(screen)

pg.quit()
exit(0)
