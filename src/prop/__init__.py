import pygame as pg

from gameobj import GameObj

class Prop(GameObj):
    def __init__(self, tile_coord, sheet_coord, bgc, fgc):
        GameObj.__init__(self, sheet_coord, tile_coord, (bgc, fgc))


    def use(self):
        pass
