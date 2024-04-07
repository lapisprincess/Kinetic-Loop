### IMPORTS ###
import json
import pygame as pg

from gameobj import GameObj
from item.effect import all_effects

from gui.menu.objectinfo import ObjectMenu

ITEM_DATA_PATH = open("data/gameobjects/items.json")

class Item(GameObj):
    def __init__(
        self, 
        sheet_coord: tuple[int,int] =(0,0), 
        tile_coord: tuple[int,int] =None, 
        fgc: pg.Color =None, 
        effect =None,
        info_intake: dict =None,
    ):
        if fgc is None:
            fgc = pg.Color(255, 255, 255)
        GameObj.__init__(self, sheet_coord, tile_coord, (pg.Color(0, 0, 0), fgc))

        self.seethrough = True
        self.traversable = True
        self.visible = True
        if info_intake is not None:
            for key in info_intake:
                val = info_intake[key]
                self.info[key] = val
        self.info["amount"] = 0

        self.image = self.info["image"]

        self.effect = effect

    def grab(self, player):
        self.visible = False
        self.tile_x, self.tile_y = 0, 0
        player.inventory.append(self)

    def use(self, target): 
        self.effect(target, self.info["amount"])
        target.inventory.remove(self)

    def drop(self, player):
        if self not in player.inventory:
            return
        self.visible = True
        self.tile_x = player.tile_x
        self.tile_y = player.tile_y
        player.inventory.remove(self)

    def view(self, system):
        new_menu = ObjectMenu(self, system.screen_dimension, system.all_fonts, system)
        system.menu = new_menu

    def clone(self):
        return Item(
            effect= self.effect,
            info_intake= self.info
        )


def parse_item_data(all_levels):
    """ transform json data into item templates """
    level_items = [[]]

    # initialize output list
    for i in all_levels:
        level_items.append([])

    item_data = json.load(ITEM_DATA_PATH)
    for raw_item_data in item_data:

        # gather preliminary data
        item_info = {}
        item_info["name"] = raw_item_data["name"]
        item_info["description"] = raw_item_data["description"]
        item_sheet_coord = raw_item_data["tile"]

        # create item
        new_item = Item(
            sheet_coord= item_sheet_coord,
            tile_coord= None,
            info_intake= item_info
        )

        # handle effects
        item_effect = raw_item_data["effect"]
        new_item.effect= all_effects[item_effect]

        # stow item
        level_items[raw_item_data["level"]-1].append(new_item)

    return level_items