### IMPORTS ###
import pygame as pg

import util.graphic as graphic


### GLOBALS ###
tile_types = ['floor', 'wall']
default_type = tile_types[0]


### TILE CLASS ###
'''
Tiles are sprites which can both be rendered and which
contain data which make up the structure of the map.

Instance variables:
    - tile_type         # type of tile (floor/wall)     : str
    - bgc               # background color for entities : pg.Color
    - tile_x, tile_y    # tile x/y coordinates          : int
    - image             # tile image                    : pg.Surface
    - rect              # tile coord/dimensions         : pg.Rect
'''
class Tile(pg.sprite.Sprite):
    def __init__(self, tile_coord, sheet_coord, tile_type, bgc, fgc):
        self.tile_x,    self.tile_y     =   tile_coord[0],    tile_coord[1]
        self.sheet_x,   self.sheet_y    =   sheet_coord[0],   sheet_coord[1]
        self.bgc,       self.fgc        =   bgc,              fgc
        self.visible = True
        if tile_type not in tile_types:
            print("illegal tile type used!")
            print("given: " + tile_type)
            print("defaulting to: " + default_type)
            tile_type = default_type
        else: self.tile_type = tile_type
        self.image = graphic.Graphic(sheet_coord, bgc, fgc)
        self.rect = self.image.get_rect()
        pg.sprite.Sprite.__init__(self)
        self.update()

    def update(self):
        self.rect.x = self.tile_x * graphic.tile_width
        self.rect.y = self.tile_y * graphic.tile_width

    def clone(self, tile_x, tile_y):
        return Tile(
            tile_coord  = (tile_x, tile_y),
            sheet_coord = (self.sheet_x, self.sheet_y),
            tile_type   = self.tile_type,
            bgc = self.bgc, fgc = self.fgc
        )

    def pixel_collide(self, pixel_coord) -> bool:
        x, y = pixel_coord[0], pixel_coord[1]
        tile_x_range = range(self.rect.left, self.rect.left + self.rect.width)
        tile_y_range = range(self.rect.top, self.rect.top + self.rect.height)
        if (x in tile_x_range) and (y in tile_y_range): return True
        return False


### SAMPLE TILES ###
# colors
lime_green = pg.color.Color(50,  250, 50)
dark_green = pg.color.Color(0,   150, 0)
grey       = pg.color.Color(100, 100, 100)
black      = pg.color.Color(0,   0,   0)
white      = pg.color.Color(255, 255, 255)
# tiles
cobble_floor = Tile((0,0), (9, 15), 'floor', grey, black)
cobble_wall  = Tile((0,0), (0, 11), 'wall', grey, black)
