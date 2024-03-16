### IMPORTS ###
import pygame as pg
from gameobj import GameObj

import util.graphic as graphic


class Item(GameObj):
    def __init__(self, item_id, sheet_coord=(0,0), fgc=None):
        self.item_id  = item_id
        self.image = graphic.Graphic(sheet_coord, fgc)

    def use(self): None
