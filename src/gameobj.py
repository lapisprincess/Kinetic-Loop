""" anything that exists on the board inherits from the gameobj class """

## IMPORTS
import pygame as pg
from util import graphic

class GameObj(pg.sprite.Sprite):
    """ general gameobj which holds info needed to exist on the board

    
    """

    def __init__(
        self, sheet_coord, tile_coord=None,
        colors=None, level=None
    ):
        pg.sprite.Sprite.__init__(self)

        if colors is None:
            colors = (pg.Color(0, 0, 0), pg.Color(255, 255, 255))

        self.image = graphic.Graphic(sheet_coord, bgc=colors[0], fgc=colors[1])
        self.rect = self.image.get_rect()
        self.level = level

        if tile_coord is not None:
            self.tile_x, self.tile_y = tile_coord[0], tile_coord[1]
        else:
            self.tile_x, self.tile_y = None, None
        self.info = {}
        self.traits = set()

        self.visible = False
        self.seethrough = False
        self.traversable = False

    def update(self):
        """ update to help render correctly """
        self.rect.x = self.tile_x * graphic.tile_width
        self.rect.y = self.tile_y * graphic.tile_width