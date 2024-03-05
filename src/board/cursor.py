### IMPORTS ###
import pygame as pg

from util.graphic import Graphic

from entity import Entity


### CONSTANTS ###
CURSOR_GRAPHIC = (8, 5)
CURSOR_FGC = pg.Color(150, 150, 50)
CURSOR_BGC = pg.Color(100, 0, 0)


### CURSOR CLASS ###
class Cursor(Entity):
    def __init__(self, tile_size, board):
        Entity.__init__(
            self, (0, 0), 
            CURSOR_GRAPHIC, CURSOR_BGC, CURSOR_FGC,
            board
        )
        self.info["HP"] = 1 # cursor, plz don't die
