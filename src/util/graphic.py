### IMPORTS ###
import pygame as pg

import sys


### CONSTANTS ###
# 256-tile spritesheet
TILESET_PATH = "data/tiles.png"

# create a global tileset object
tileset = pg.image.load(TILESET_PATH)

# tile dimension calculated on fact that spritesheet has 256 tiles
# divide width by 16 for tile_width
tile_width = tileset.get_size()[0] / 16


### GRAPHIC CLASS ###
class Graphic(pg.Surface):
    def __init__(self, sheet_coord, bgc=None, fgc=None): 
        # initialize blank surface
        pg.Surface.__init__(self, (tile_width, tile_width))

        # adjust tile coordinates to match spritesheet dimensions
        # then crop full tileset by taking specified subsurface
        sheet_x = sheet_coord[0] * tile_width
        sheet_y = sheet_coord[1] * tile_width
        crop = (sheet_x, sheet_y, tile_width, tile_width)
        self.tile = tileset.subsurface(crop)

        # if fgc specified, use PixelArray to alter color
        if fgc != None:
            tile_pixArr = pg.PixelArray(self.tile)
            tile_pixArr.replace(pg.color.Color("white"), fgc)
            self.tile = tile_pixArr.make_surface()

        # if bgc is specified, set it; then add the tile
        if bgc != None: self.fill(bgc)
        self.blit(self.tile, (0,0))

    def set_bgc(self, color):
        self.fill(color)
        self.blit(self.tile, (0,0))
