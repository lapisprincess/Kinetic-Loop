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

import game_gui as gi


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

cursor_img = pg.image.load("data/cursor.png")
cursor_pressed_img = pg.image.load("data/cursor_pressed.png")
cursor = pg.cursors.Cursor((0, 0), cursor_img)
cursor_pressed = pg.cursors.Cursor((0, 0), cursor_pressed_img)
pg.mouse.set_cursor(cursor)



### PREPARING BOARD ###
game_board = board.Board(
    controls, graphic.tile_width, (500, 500), 
    #visibility = True
)

'''
cobble_floor, cobble_wall = tile.cobble_floor, tile.cobble_wall
room1 = game_board.build_room((0, 5), (5, 10), cobble_floor, cobble_wall)
#roomx = game_board.build_room((7, 3), (5, 15), cobble_floor, cobble_wall)
room2 = game_board.build_room((15, 15), (10, 10), cobble_floor, cobble_wall)
game_board.connect_rooms(room1, room2)
'''
game_board.generate_floor(8)




### GUI INITIALIZATION ###
border = pg.image.load("data/leafy_border.png")
font = pg.font.Font("data/font.otf", size=14)

game_gui = gi.GUI(screen_dimensions, font, game_board)

game_gui.log.set_border(border, mid_prcnt = (0.75, 0.72), mid_color = (10, 50, 0))
game_gui.info.set_border(border, mid_prcnt = (0.75, 0.72), mid_color = (0, 80, 20))

game_gui.add_messages([
    "Message 1",
    "Message 2",
    "Message 3",
    "Message 4",
])





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



### GAME LOOP ###
game_board._update() # preemptive update
running = True
while running:
    #if pg.key.get_pressed()[pg.K_BACKQUOTE]: debug.debug()
    check_input = False
    pg.display.flip()
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False
        if event.type == pg.KEYDOWN: check_input = True
        if event.type == pg.MOUSEWHEEL:
            mouse_pos = pg.mouse.get_pos()
            if event.y >= 0: direction = 'up'
            else: direction = 'down'
            game_gui.scroll(direction, mouse_pos)
        if event.type == pg.MOUSEBUTTONDOWN:
            pg.mouse.set_cursor(cursor_pressed)
        if event.type == pg.MOUSEBUTTONUP:
            pg.mouse.set_cursor(cursor)

    screen.fill("black")
    game_board.update(check_input)
    game_gui.draw(screen)

pg.quit()
exit(0)
