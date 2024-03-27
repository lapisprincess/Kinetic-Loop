### IMPORTS ###
import pygame as pg
from gameobj import GameObj


class Item(GameObj):
    def __init__(self, sheet_coord=(0,0), tile_coord=None, fgc=None):
        if fgc is None:
            fgc = pg.Color(255, 255, 255)
        GameObj.__init__(self, sheet_coord, tile_coord, (pg.Color(0, 0, 0), fgc))

        self.seethrough = True
        self.traversable = True
        self.visible = True

    def use(self): None

    def grab(self, player):
        self.visible = False
        self.tile_x, self.tile_y = 0, 0
        player.inventory.append(self)
