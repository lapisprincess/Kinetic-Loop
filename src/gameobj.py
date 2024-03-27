""" anything that exists on the board inherits from the gameobj class """

## IMPORTS
import pygame as pg
from util import graphic

class GameObj(pg.sprite.Sprite):
    """ general gameobj which holds info needed to exist on the board

    
    """

    def __init__(
        self, 
        sheet_coord: tuple[int,int], 
        tile_coord: tuple[int,int] =None,
        colors: tuple[pg.Color,pg.Color] =None, 
        level: int =None,
        info: dict =None,
    ):
        if tile_coord is None:
            tile_coord = 0, 0
        if colors is None:
            colors = (pg.Color("black"), pg.Color("white"))
        if level is None:
            level = 0
        if info is None:
            info = {
                "name": "Mystery object",
                "hp": 0
            }

        pg.sprite.Sprite.__init__(self)

        self.tile_x, self.tile_y = tile_coord[0], tile_coord[1]
        self.info = info
        self.traits = set()

        self.image = graphic.Graphic(sheet_coord, bgc=colors[0], fgc=colors[1])
        self.info["image"] = self.image
        self.rect = self.image.get_rect()
        self.level = level

        self.visible = True
        self.seethrough = False
        self.traversable = False

        self.is_player = False

    def update(self):
        """ update to help render correctly """
        self.rect.x = self.tile_x * graphic.tile_width
        self.rect.y = self.tile_y * graphic.tile_width