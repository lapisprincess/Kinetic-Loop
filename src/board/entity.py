import pygame as pg

import board

'''
Entities only contain information pertaining
to specific entity objects, to be drawn onto tiles.

Instance variables:
    -
'''

class Entity(pg.sprite.Sprite):
    def __init__(
        self,
        sheet_x, sheet_y,   # sprite loc in tileset : int
        bgc, fgc,           # entity color          : pg.Color
        tile_x, tile_y      # entity coord          : int
    ):
        self.bgc, self.tile_x, self.tile_y = bgc, tile_x, tile_y

        self.image = pg.surface.Surface((board.tile_width,board.tile_width))
        self.image.fill(bgc)
        self.entity_image = board.crop_image(sheet_x, sheet_y, fgc)
        self.image.blit(self.entity_image, (0,0))

        self.rect = self.image.get_rect()

        pg.sprite.Sprite.__init__(self)

    def update(self): None

    def set_bgc(self, color):
        self.image.fill(color)
        self.image.blit(self.entity_image, (0,0))
