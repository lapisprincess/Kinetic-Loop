### IMPORTS ###
import pygame as pg

import util.graphic as graphic


class Item():
    def __init__(
        self,
        item_id,            # id code               : str
        sheet_coord=(0,0),  # sprite loc in tileset : (int,int)
        fgc=None            # tile colors           : pg.Color
    ):
        self.item_id  = item_id
        self.image = graphic.Graphic(sheet_coord, fgc)

    def use(self): None
