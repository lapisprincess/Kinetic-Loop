""" weapons, used to whack/shoot stuff with """

## IMPORTS
from item import Item

class Weapon(Item):
    def __init__(self, item_id, damage, sheet_coord=(0,0), fgc=None):
        Item.__init__(self, item_id, sheet_coord, fgc)
        self.damage = damage

        self.type = "melee"