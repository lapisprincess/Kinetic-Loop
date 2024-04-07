""" universal entity module """

## IMPORTS
import json
import pygame as pg

from util import graphic
import util.direction as directionality
from util.fov import fov_los

from entity import trait

from prop.stairs import Stairs

from gameobj import GameObj


## CONSTANTS
UNARMED_DMG = 5
FOV_WIDTH = 6

ENTITY_DATA_PATH = open("data/gameobjects/entity.json")


## ENTITY CLASS
class Entity(GameObj):
    """ entity class holding all basic entity information """

    def __init__(
        self, 
        sheet_coord :tuple[int,int],
        tile_coord :tuple[int,int] =None,
        colors :tuple[pg.Color,pg.Color] =None, #(bgc, fgc)
        level =None,
        info_intake :dict =None
    ):

        # dress up given information to make it computer-legible
        adjusted_info = {}
        if info_intake is not None:
            for info in info_intake:
                adjusted_info[info] = info_intake[info]

        # initialize as game object
        GameObj.__init__(self, sheet_coord, tile_coord, colors, level, adjusted_info)

        # store crucial information
        if "hp" not in self.info:
            self.info["hp"] = 1
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


    ## MUTATORS
    def update(self):
        """ update checks extra entity-specific variables """
        GameObj.update(self)
        if self.info["hp"] <= 0:
            self.level.log_message(self.get_info()["name"] + " died!!")
            self.kill()

    def take_turn(self):
        """ take turn, basing action taken on traits and priorities """
        self.fov = fov_los(self.level, self) # new fov
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

    def add_item(self, new_item):
        """ Give the entity a new item """
        self.inventory.append(new_item)

    def move(self, direction, full_movement=False, attack_on_move=False):
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
            if attack_on_move:
                self.attack(entity)
                return True
            return False

        # see if anything is in the way
        thing = self.level.get(x_coord, y_coord)
        if not full_movement and (thing is None or thing.traversable is False):
            return False

        # success!
        self.tile_x = x_coord
        self.tile_y = y_coord
        return True

    def attack(self, target):
        """ for now, only melee combat is ready """
        self._attack_melee(target)

    def _attack_ranged(self, target):
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

    def _attack_melee(self, target):
        """ combat with adjacent targets """
        weapon = self.equipped["weapon"]
        if weapon is not None and weapon.type == "melee":
            dmg = weapon.dmg
            weapon_name = weapon.name
        else:
            dmg = UNARMED_DMG
            weapon_name = "fists"

        message = self.get_info()["name"]
        message += " attacked " + target.get_info()["name"]
        message += " for " + str(dmg) + " damage"
        message += " with their " + weapon_name + "!"
        self.level.log_message(message)

        target.info["hp"] -= dmg
        target.update()

    def heal(self, amount):
        newval = self.info["hp"] + amount
        if "max_hp" in self.info and newval > self.info["max_hp"]:
            amount = self.info["max_hp"] - self.info["hp"]
            if amount > 1:
                self.level.log.add_message(self.info["name"] + " healed for " + str(amount) + "!")
            self.info["hp"] = self.info["max_hp"]
        else:
            if amount > 1:
                self.level.log.add_message(self.info["name"] + " healed for " + str(amount) + "!")
            self.info["hp"] = newval


    ## GETTERS
    def get_info(self):
        """ info getter which fills in necessary information """
        if "name" not in self.info:
            self.info["name"] = "leafling"
        if "image" not in self.info:
            self.info["image"] = self.image

        return self.info

    def get_surrounding_game_objects(self):
        """ returns a list of game objects directly around the entity """
        all_gameobjs = []
        for direction in directionality.all_directions:
            x = self.tile_x + directionality.necessary_movement(direction)[0]
            y = self.tile_y + directionality.necessary_movement(direction)[1]
            gameobj = self.level.get_entity(x, y)
            if gameobj is not None and isinstance(gameobj, Entity):
                all_gameobjs.append(gameobj)
        return all_gameobjs


    ## MISC
    def clone(self, tile_x:int =None, tile_y:int =None):
        """ Method to create a duplicate of entity,
        useful for creating duplicatable template entities! """
        if tile_x is None:
            tile_x = self.tile_x
        if tile_y is None:
            tile_y = self.tile_y

        new_entity = Entity(
            self.sheet_coord,
            (tile_x, tile_y),
            self.colors,
            self.level,
            self.info
        )

        for trait in self.traits:
            new_entity.traits.add(trait)
        
        return new_entity


def parse_entity_data(all_levels):
    """ transform json data into entity templates """
    level_entities = [[]]

    # initialize output list
    for i in all_levels:
        level_entities.append([])

    entities_data = json.load(ENTITY_DATA_PATH)
    for raw_entity_data in entities_data:

        # gather preliminary data
        entity_info = {}
        entity_info["name"] = raw_entity_data["name"]
        entity_info["description"] = raw_entity_data["description"]
        entity_info["hp"] = raw_entity_data["hp"]
        entity_sheet_coord = raw_entity_data["tile"]

        # create entity
        new_entity = Entity(
            sheet_coord =entity_sheet_coord,
            tile_coord =None,
            level =all_levels[raw_entity_data["level"]-1],
            info_intake =entity_info
        )

        # handle traits
        entity_traits = raw_entity_data["traits"]
        for entity_trait in entity_traits:
            new_trait = trait.all_traits[entity_trait]
            new_entity.traits.add(new_trait)

        # stow entity
        level_entities[raw_entity_data["level"]-1].append(new_entity)

    return level_entities