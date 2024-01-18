import pygame as pg

from entity import Entity



class Player(Entity):
    def __init__(self, coord_x, coord_y):
        tile_x, tile_y, color = 0, 4, pg.color.Color(150,50,50)
        Entity.__init__(self, tile_x, tile_y, color, coord_x, coord_y)
