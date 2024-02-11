import pygame as pg

from board.tile import Tile

class Prop(Tile):
    def __init__(self, tile_coord, sheet_coord, bgc, fgc):
        Tile.__init__(self, tile_coord, sheet_coord, 'interactive', bgc, fgc)
