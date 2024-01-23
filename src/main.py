### IMPORTS ###
import pygame as pg
import random

import item
import item.consumable as consumable

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
board = board.Board((50, 50))

r = 0

# make a room (testing!)
width, height = random.randint(5, 15), random.randint(5, 15)
board.build_room((0, 0), (width, height), tile.cobble_floor, tile.cobble_wall)
#board.build_room((0, 0), (width, height), tile.cobble_floor, tile.cobble_wall)

# temporary player entity
player_bgc, player_fgc = pg.color.Color('green'), pg.color.Color('white')
random_floor = board.get_random_floor()
player = entity.player.Player(
    (0, 4),
    player_bgc, player_fgc, 
    (random_floor.tile_x, random_floor.tile_y)
)
player.inventory.append(consumable.health_potion)
board.entities.add(player)


### GAME LOOP ###
running = True
while running:
    if pg.key.get_pressed()[pg.K_BACKQUOTE]: # debugging
        # prompt and interpret user input
        prompt = input("\n> ") + " "
        command = []
        while ' ' in prompt:
            command.append(prompt[: prompt.index(' ')])
            prompt = prompt[prompt.index(' ') + 1 :]

        # pull parameters fromp command
        params = command[1:]
        try: 
            for i in range(0, len(params)): params[i] = int(params[i])
        except: None # if it can't be made into an int, it shouldn't change

        # pull command
        command = command[0]

        # interpret command
        if command == "build_room" and len(params) >= 4:
            cond = board.build_room(
                (params[0], params[1]), 
                (params[2], params[3]), 
                tile.cobble_floor, tile.cobble_wall
            ) # cond allows us to report whether build was successful
            if cond: print("success!")
            else: print("failed to build room!")

        elif command == "kill" and len(params) >= 1:
            for entity in board.entities.sprites():
                if entity.id == params[0]: entity.kill()

        else: # no suitable command
            print("unrecognized command!")

    # utility stuff
    check_input = False
    pg.display.flip()
    clock.tick(60)
    for event in pg.event.get(): 
        if event.type == pg.QUIT: running = False
        if event.type == pg.KEYDOWN: check_input = True

    # clear screen
    screen.fill("black")

    # draw and update board
    board.update(check_input)
    board.draw(screen)


### CLEAN EXIT ###
pg.quit()
exit(0)
