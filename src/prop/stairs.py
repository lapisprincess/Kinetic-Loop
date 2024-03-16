""" stairs which allow the player to travel between floors """

## IMPORTS
import pygame as pg

from gameobj import GameObj

## STAIR CONSTANTS
STAIR_DOWN_SHEET_COORD = (14, 3)
STAIR_UP_SHEET_COORD = (12, 3)
STAIR_BGC = pg.Color(0, 0, 0)
STAIR_FGC = pg.Color(255, 255, 255)

class Stairs(GameObj):
    """ stairs are a prop which allow transporation between levels """

    def __init__(self, tile_coord, direction, dest, dest_loc=None):
        sheet = STAIR_DOWN_SHEET_COORD
        if direction == "up":
            sheet = STAIR_UP_SHEET_COORD
        GameObj.__init__(self, sheet, tile_coord, (STAIR_BGC, STAIR_FGC))

        self.seethrough = True
        self.traversable = True

        self.direction = direction
        self.dest = dest
        self.dest_loc = dest_loc

    def travel(self, traveller):
        """ basic stair function, make entity travel between floors """
        self.dest.add_gameobj(traveller, self.dest_loc)
