"""Universal entity module"""

## IMPORTS
import json
import pygame as pg

from util import graphic
import util.direction as directionality
from util.fov import fov_los

from prop.stairs import Stairs

from gameobj import GameObj


## CONSTANTS
UNARMED_DMG = 5
FOV_WIDTH = 6
DATA_FILE = open("data/gameobjects/entity.json")


## ENTITY CLASS
class Entity(GameObj):
    """Informal entity class to be inherited

    """

    def __init__(
        self, 
        sheet_coord :tuple[int,int],
        tile_coord :tuple[int,int] =None,
        colors :tuple[pg.Color,pg.Color] =None, #(bgc, fgc)
        level =None,
        info :dict =None
    ):
        
        # initialize as game object
        GameObj.__init__(self, sheet_coord, tile_coord, colors, level, info)

        # store crucial information
        if "hp" not in self.info:
            self.info["hp"] = 0
        if "name" not in self.info:
            self.info["name"] = "Sprout"

        # store params for cloning
        self.sheet_coord, self.colors = sheet_coord, colors
        
        # extra info
        self.target = None
        self.inventory = []
        self.equipped = {
            "helmet" : None,
            "armor" : None,
            "weapon" : None,
        }

        # spacial info
        self.visible = True
        self.seethrough = True
        self.traversable = False

        # initial fov intake
        if self.level is not None and tile_coord is not None:
            self.fov = fov_los(self.level, self)
        else: self.fov = None

        # space for traits to be added (will likely become a parameter TODO)
        self.traits = set()


    def update(self):
        """ TODO """
        GameObj.update(self)

        if self.info["hp"] <= 0:
            self.level.log_message(self.get_info()["name"] + " died!!")
            self.kill()

    def take_turn(self):
        """ TODO """
        for trait in self.traits:
            if trait.priority != 1:
                continue
            if trait.act(self) is True:
                return True
        for trait in self.traits:
            if trait.priority != 2:
                continue
            if trait.act(self) is True:
                return True
        for trait in self.traits:
            if trait.priority != 3:
                continue
            if trait.act(self) is True:
                return True
        return False


    def move(self, direction, full_movement=False):
        """ move entity, respecting obstacles.
        returns true if move successful, false otherwise """

        # get new coordinates
        mods = directionality.necessary_movement(direction)
        if mods is None:
            return False
        x, y = mods[0], mods[1]
        x_coord = self.tile_x + x
        y_coord = self.tile_y + y

        # check if entity at new coords, auto-interact if so
        entity = self.level.get(x_coord, y_coord, Entity)
        if entity is not None and full_movement is False:
            self.attack(entity)
            return False

        # see if anything is in the way
        thing = self.level.get(x_coord, y_coord)
        if not full_movement and (thing is None or thing.traversable is False):
            return False

        # success!
        self.tile_x = x_coord
        self.tile_y = y_coord
        self.fov = fov_los(self.level, self) # new fov
        return True


    # default info provider, filling in missing key info
    def get_info(self):
        """ TODO """
        if "name" not in self.info:
            self.info["name"] = "leafling"
        if "image" not in self.info:
            self.info["image"] = self.image

        return self.info


    def attack(self, target):
        self.attack_melee(target)

    def attack_ranged(self, target):
        """ TODO """
        if target not in self.fov:
            self.level.log_message("Out of range!")
            return
        if not isinstance(target, Entity):
            self.level.log_message("Can only fire at entities!")
            return

        weapon = self.equipped["weapon"]
        if weapon is not None and weapon.type == "ranged":
            dmg = weapon.dmg
            weapon_name = weapon.name
        else:
            self.level.log_message("Cannot fire a melee weapon!")
            return

        message = self.get_info()["name"]
        message += " fired at " + target.get_info()["name"]
        message += " for " + str(dmg) + " damage "
        message += " with their " + weapon_name + "!"
        self.level.log_message(message)

        self.info["HP"] -= dmg
        target.update()

    def attack_melee(self, target):
        """ TODO """
        weapon = self.equipped["weapon"]
        if weapon is not None and weapon.type == "melee":
            dmg = weapon.dmg
            weapon_name = weapon.name
        else:
            dmg = UNARMED_DMG
            weapon_name = "fists"

        message = self.get_info()["name"]
        message += " attacked " + target.get_info()["name"]
        message += " for " + str(dmg) + " damage "
        message += " with their " + weapon_name + "!"
        self.level.log_message(message)

        self.info["hp"] -= dmg
        target.update()

    def add_item(self, new_item):
        """ Give the entity a new item """
        self.inventory.append(new_item)

    def clone(self, tile_x:int =None, tile_y:int =None):
        """ Method to create a duplicate of entity,
        useful for creating duplicatable template entities! """
        if tile_x is None:
            tile_x = self.tile_x
        if tile_y is None:
            tile_y = self.tile_y

        return Entity(
            self.sheet_coord,
            (tile_x, tile_y),
            self.colors,
            self.level,
            self.info
        )



def parse_entity_data(all_levels):
    entities = []

    entities_data = json.load(DATA_FILE)["entities"]
    for entity_data in entities_data:

        entity_info = {}
        entity_info["name"] = entity_data["name"]
        entity_info["description"] = entity_data["description"]
        entity_info["hp"] = entity_data["hp"]

        entity_sheet_coord = entity_data["tile"][0], entity_data["tile"][1]
        entities.append(Entity(
            sheet_coord =entity_sheet_coord,
            tile_coord =None,
            level =all_levels[entity_data["level"]],
            info = entity_info
        ))

    return entities