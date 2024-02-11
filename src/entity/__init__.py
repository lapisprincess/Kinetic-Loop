### IMPORTS ###
import pygame as pg

import util.graphic as graphic
import util.direction_management as dm


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
    def __init__(self, tile_coord, sheet_coord, bgc, fgc):
        self.tile_x, self.tile_y = tile_coord[0], tile_coord[1]
        self.inventory = []
        self.visible = True

        self.image = graphic.Graphic(sheet_coord, bgc, fgc)
        self.rect = self.image.get_rect()

        self.update()
        pg.sprite.Sprite.__init__(self)

    def update(self): 
        self.rect.x = self.tile_x * graphic.tile_width
        self.rect.y = self.tile_y * graphic.tile_width

    def move(self, direction, board):
        (x, y) = dm.necessary_movement(direction)
        x_coord, y_coord = self.tile_x + x, self.tile_y + y
        try:
            if board.get_tile(x_coord, y_coord).tile_type == 'floor':
                self.tile_x, self.tile_y = x_coord, y_coord
        except: print("trying to move into the void!!")

    def pixel_collide(self, pixel_coord) -> bool:
        x, y = pixel_coord[0], pixel_coord[1]
        tile_x_range = range(self.rect.left, self.rect.left + self.rect.width)
        tile_y_range = range(self.rect.top, self.rect.top + self.rect.height)
        if (x in tile_x_range) and (y in tile_y_range): return True
        return False
