""" main game running program """

### IMPORTS ###
import sys
import pygame as pg

from game import Game

## HANDLE COMMAND LINE INPUTS
arguments = sys.argv
setFOV = bool('nofov' not in arguments)
setEntities = bool('noents' not in arguments)
stg = bool('stg' in arguments)

## PYGAME INITIALIZATION
pg.init()
pg.display.set_caption("🍃Leaflings🍂")
icon = pg.image.load("data/icon.png")
pg.display.set_icon(icon)

## CREATE GAME OBJECT
game = Game(setFOV, setEntities, stg)
game.loop()

## GRACEFUL EXIT
pg.quit()
exit(0)
