""" main game running program """

### IMPORTS ###
import sys

import pygame as pg

from game import Game

## HANDLE COMMAND LINE INPUTS
arguments = sys.argv
setFOV = bool('nofov' not in arguments)
testroom = bool('testroom' in arguments)

## INITIATE SETTINGS

## PYGAME INITIALIZATION
pg.init()
pg.display.set_caption("🍃Leaflings🍂")

## CREATE GAME OBJECT
game = Game(setFOV, testroom)

game.loop()

pg.quit()
exit(0)

"""
## TEST ENTITY
game_level = all_levels[1]
entity_bgc, entity_fgc = pg.color.Color('blue'), pg.color.Color('white')
random_floor = game_level.get_random_floor()

adoring_fan = entity.npc.NPC(
    (6, 6), (random_floor.tile_x, random_floor.tile_y),
    (entity_bgc, entity_fgc), game_level
)
game_level.add_gameobj(adoring_fan)

adoring_fan.info["Name"] = "Adoring fan"
adoring_fan.info["HP"] = 3

adoring_fan.traits.add(wandering)
adoring_fan.traits.add(hostile)
"""