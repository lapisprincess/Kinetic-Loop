### IMPORTS ###
import pygame as pg

from item import Item


### CONSUMABLE CLASS ###
'''

'''
class Consumable(Item):
    def __init__(
        self,
        item_id='',         # id code                           : str
        sheet_coord=(0,0),  # sprite loc in tileset             : (int,int)
        fgc=None,           # tile colors                       : pg.Color
        charge=-1           # number of times it can be used    : int
    ):
        Item.__init__(self, item_id, sheet_coord, fgc)
        self.charge = charge

    def consume(self) -> bool:
        if self.charge == 0: return False
        if self.charge > 0: self.charge -= 1
        self.use()
        return True


health_potion = Consumable('potion', (13, 10), charge=5)
