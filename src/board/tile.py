### IMPORTS ###
import pygame as pg

import board


### GLOBALS ###
tile_types = ['floor', 'wall']


### TILE CLASS ###
'''
Tiles are sprites which can both be rendered and which
contain data which make up the structure of the map.

Instance variables:
    - tile_type     # type of tile (floor/wall)     : String
    - bgc/fgc       # background/foreground color   : pg.Color
    - image         # tile image                    : pg.Surface
    - rect          # tile coord/dimensions         : pg.Rect
'''
class Tile(pg.sprite.Sprite):
    def __init__(
        self,
        tile_type,          # type of tile          : String
        sheet_x, sheet_y,   # sprite loc in tileset : int
        bgc, fgc,           # tile colors           : pg.Color
        tile_x, tile_y      # tile coord            : int
    ):
        self.tile_type, self.bgc = tile_type, bgc
        self.tile_x, self.tile_y = tile_x, tile_y

        # create a blank surface and a copy of the tile's graphic
        self.image = pg.surface.Surface((board.tile_width,board.tile_width))
        self.image.fill(bgc)
        self.image.blit(board.crop_image(sheet_x, sheet_y, fgc), (0,0))

        # create rect and set at adjusted coordinates for render
        self.rect = self.image.get_rect()

        pg.sprite.Sprite.__init__(self)


    '''

    '''
    def update(self): None



### SAMPLE TILES ###
green = pg.color.Color('green')
black = pg.color.Color('black')

grass = Tile('floor', 12, 2, green, black, 0, 0)
