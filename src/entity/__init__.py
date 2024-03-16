"""Universal entity module"""

## IMPORTS
import pygame as pg

from util import graphic
import util.direction as directionality
from util.fov import fov_los

from prop.stairs import Stairs

from gameobj import GameObj


## CONSTANTS
UNARMED_DMG = 5
FOV_WIDTH = 6


## ENTITY CLASS
class Entity(GameObj):
    """Informal entity class to be inherited

    """

    def __init__(
        self, sheet_coord, tile_coord=None,
        colors=None, level=None
    ):

        GameObj.__init__(self, sheet_coord, tile_coord, colors, level)

        self.info["HP"] = 0
        self.info["Name"] = "Sprout"

        self.target = None
        self.inventory = []
        self.equipped = {
            "helmet" : None,
            "Armor" : None,
            "Weapon" : None,
        }

        self.visible = True
        self.seethrough = True
        self.traversable = False

        if self.level is not None and tile_coord is not None:
            self.fov = fov_los(self.level, self)
        else: self.fov = None

        self.traits = set()


    def update(self):
        """ TODO """
        GameObj.update(self)

        self.fov = fov_los(self.level, self)

        if self.info["HP"] <= 0:
            self.level.log_message(self.get_info()["Name"] + " died!!")
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


    # universal move method, usable by any entity to move one tile at a time
    # returns True if any action taken
    def move(self, direction, full_movement=False):
        """ TODO """

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
        return True


    # default info provider, filling in missing key info
    def get_info(self):
        """ TODO """
        if "Name" not in self.info:
            self.info["Name"] = "Leafling"
        if "Image" not in self.info:
            self.info["Image"] = self.image

        return self.info


    def damage(self, dmg):
        """ TODO """
        self.info["HP"] -= dmg

    def attack(self, target):
        """ TODO """
        dmg = UNARMED_DMG
        if self.equipped["Weapon"] is not None:
            dmg = self.equipped["Weapon"].damage
        message = self.get_info()["Name"]
        message += " attacked " + target.get_info()["Name"]
        message += " for " + str(dmg) + " damage!"
        self.level.log_message(message)
        target.damage(dmg)
        target.update()

    def add_item(self, new_item):
        """ Give the entity a new item """
        self.inventory.append(new_item)
