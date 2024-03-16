""" """

### IMPORTS ###
import pygame as pg

from entity import Entity


### CONSTANTS ###
CURSOR_GRAPHIC = (8, 5)
CURSOR_FGC = pg.Color(150, 150, 50)
CURSOR_BGC = pg.Color(100, 0, 0)


### CURSOR CLASS ###
class Cursor(Entity):
    """ """
    def __init__(self, level):
        Entity.__init__(
            self, CURSOR_GRAPHIC,
            colors=(CURSOR_BGC, CURSOR_FGC), level=level
        )
        self.info["HP"] = 1 # cursor, plz don't die
