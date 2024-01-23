### IMPORTS ###
import pygame as pg

import graphic


### ENTITY CLASS ###
'''
Entities are sprites that are drawn onto tiles and which contain
information that allows them to exist and navigate their surroundings.

Instance variables:
    - bgc
    - tile_x, tile_y
    - image             # tile image                    : pg.Surface
    - rect              # tile coord/dimensions         : pg.Rect
    - inventory         # items held by entity          : [Item]
'''
class Entity(pg.sprite.Sprite):
    def __init__(
        self,
        sheet_coord,    # sprite loc in tileset : int
        bgc, fgc,       # entity color          : pg.Color
        tile_coord      # entity coord          : int
    ):
        # initialize variables
        self.tile_x, self.tile_y = tile_coord[0], tile_coord[1]
        self.image = graphic.Graphic(sheet_coord, bgc, fgc)
        self.rect = self.image.get_rect()

        self.inventory = []

        pg.sprite.Sprite.__init__(self)

    def update(self): None

    def move(self, direction, board):
        match direction:
            case 'north': x, y = 0, -1
            case 'south': x, y = 0, 1
            case 'west': x, y = -1, 0
            case 'east': x, y = 1, 0
            case 'north-west': x, y = -1, -1
            case 'north-east': x, y = 1, -1
            case 'south-west': x, y = -1, 1
            case 'south-east': x, y = 1, 1

        x_coord, y_coord = self.tile_x + x, self.tile_y + y
        try:
            if board.get_tile(x_coord, y_coord).tile_type == 'floor':
                self.tile_x, self.tile_y = x_coord, y_coord
        except: print("trying to move into the void!!")
