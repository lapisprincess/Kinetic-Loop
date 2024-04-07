""" Player class """

### IMPORTS ###
import pygame as pg

from util.pathfind import pathfind
from util.fov import fov_los

from prop.stairs import Stairs

from entity import Entity


### PLAYER CLASS ###
class Player(Entity):
    """Player class, inheriting from Entity """

    def __init__(
        self, 
        sheet_coord :tuple[int,int], 
        tile_coord :tuple[int,int] =None,
        colors :tuple[pg.Color,pg.Color] =None, 
        level =None
    ):
        self.id = "player"
        Entity.__init__(
            self, sheet_coord, tile_coord,
            colors, level
        )

        self.fast_direction = None
        self.travel_path = None
        self.current_room = None

        self.info["name"] = "Tilda"
        self.info["hp"] = 15
        self.info["max_hp"] = self.info["hp"]

        self.visible = True

        self.is_player = True

    def update(self):
        """ constant updater """
        Entity.update(self)
        for tile in self.fov:
            self.level.shadows.add(tile)
        self.fov = fov_los(self.level, self) # player fov should always be up to date

    def move(self, direction, full_movement=False):
        """ player movement has some special features:
        player movement should also account for stairs
        player bumping into entity leads to attack """
        result = Entity.move(self, direction, full_movement, attack_on_move=True)

        if direction in ("up", "down"):
            # check if player walking up/down stairs
            stairs = self.level.get(self.tile_x, self.tile_y, Stairs)
            if stairs is not None and stairs.direction == direction:
                stairs.travel(self)
                return True
            return False

        return result

    def fast_move(self):
        """ continuously move in a direction until obstacle """
        stop = False
        message = None

        # check if hostile entities near player
        for entity in self.level.game_objects:
            if entity is self or not isinstance(entity, Entity):
                continue
            if entity.target is self:
                message = "hostile entity nearby"
                stop = True

        # try moving
        result = Entity.move(self, self.fast_direction)
        if self.fast_direction is None or result is False:
            message = "bumped into an obstacle"
            stop = True

        # see if entered new room
        new_room = self.level.get_room(self.tile_x, self.tile_y)
        if self.current_room is None:
            self.current_room = new_room
        elif new_room != self.current_room:
            message = "entered a new room"
            stop = True

        # any reason to stop, clean exit
        if stop:
            if message is None:
                message = "seemingly no reason?"
            self.level.log_message("Stopped automoving (" + message + ")")
            self.fast_direction = None
            self.current_room = None
            return False
        return True

    def drop(self, item):
        for inventory_object in self.inventory:
            if item == inventory_object:
                self.inventory.remove(inventory_object)


    def travel(self):
        """ fast travel to travel_dest """

        # check if hostile entities near player
        for entity in self.level.game_objects:
            if entity is self or not isinstance(entity, Entity):
                continue
            if entity.target is self:
                self.travel_path = None
                message = "hostile entity nearby"
                self.level.log_message("Stopped traveling (" + message + ")")
                return False

        # general travel cases
        if len(self.travel_path) == 0:
            self.travel_path = None
            return False
        elif self.travel_path is not None:
            self.move(self.travel_path.pop())
            return True