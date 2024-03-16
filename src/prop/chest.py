""" chests contain loot for the player to collect! """

## IMPORTS
import pygame as pg
from gameobj import GameObj

## CONSTANTS
CHEST_SHEET_COORD = 8, 13
STAIR_BGC = pg.Color(0, 0, 0)
STAIR_FGC = pg.Color(255, 255, 255)


class Chest(GameObj):
    """ container full of items for the player to take """

    def __init__(self, tile_coord):
        GameObj.__init__(self, CHEST_SHEET_COORD, tile_coord, (STAIR_BGC, STAIR_FGC))

        self.storage = []
        self.seethrough = True
