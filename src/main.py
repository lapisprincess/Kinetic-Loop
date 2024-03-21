""" main game running program """

### IMPORTS ###
import sys
import pygame as pg

from game import Game

## HANDLE COMMAND LINE INPUTS
arguments = sys.argv
setFOV = bool('nofov' not in arguments)
stg = bool('stg' in arguments)

## PYGAME INITIALIZATION
pg.init()
pg.display.set_caption("🍃Leaflings🍂")

## CREATE GAME OBJECT
game = Game(setFOV, stg)
game.loop()

## GRACEFUL EXIT
pg.quit()
exit(0)