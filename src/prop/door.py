import pygame as pg

from prop import Prop

class Door(Prop):
    def __init__(self, tile_coord, sheet_coord, bgc, fgc):
        Tile.__init__(self, tile_coord, sheet_coord, 'wall', bgc, fgc)

    def open_door(self):
        self.tile_type = 'interactive'

    def close_door(self):
        self.ile_type = 'wall'
