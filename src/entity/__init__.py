### IMPORTS ###
import pygame as pg

import util.graphic as graphic
import util.direction as d


### ENTITY CLASS ###
class Entity(pg.sprite.Sprite):
    def __init__(self, tile_coord, sheet_coord, bgc, fgc):
        self.tile_x, self.tile_y = tile_coord[0], tile_coord[1]
        self.inventory = []
        self.visible = True

        self.image = graphic.Graphic(sheet_coord, bgc, fgc)
        self.rect = self.image.get_rect()

        # pre-emptive update for accuracy
        self.update()

        pg.sprite.Sprite.__init__(self)


    # every entity should adjust their rectangles accordingly
    def update(self): 
        self.rect.x = self.tile_x * graphic.tile_width
        self.rect.y = self.tile_y * graphic.tile_width


    # universal move method, usable by any entity to move one tile at a time
    def move(self, direction, board):
        (x, y) = d.necessary_movement(direction)
        x_coord, y_coord = self.tile_x + x, self.tile_y + y
        new_tile = board.get_tile(x_coord, y_coord)
        if (new_tile != None) and (new_tile.tile_type == 'floor'):
            self.tile_x, self.tile_y = x_coord, y_coord
