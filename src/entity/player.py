### IMPORTS ###
import pygame as pg

from entity import Entity
from entity.npc import NPC


### PLAYER CLASS ###
class Player(Entity):
    def __init__(self, tile_coord, sheet_coord, bgc, fgc, board):
        self.id = "player"
        Entity.__init__(self, tile_coord, sheet_coord, bgc, fgc, board)

        self.fast_direction = None
        self.current_room = None

        self.info["Name"] = "Tilda"
        self.info["HP"] = 15
        self.info["Roots"] = 0


    def fast_move(self):
        stop = False
        message = None

        # try moving
        result = Entity.move(self, self.fast_direction)
        if self.fast_direction == None or result == False: 
            message = "bumped into an obstacle"
            stop = True

        # see if entered new room
        new_room = self.board.get_room_at_tile(self.tile_x, self.tile_y)
        if self.current_room == None:
            self.current_room = new_room
        elif new_room != self.current_room: 
            message = "entered a new room"
            stop = True

        # any reason to stop, clean exit
        if stop:
            if message == None: message = "seemingly no reason?"
            self.board.log_message("Stopped automoving (" + message + ")")
            self.fast_direction = None
            self.current_room = None


    def take_turn(self):
        Entity.take_turn(self)


    def update(self):
        Entity.update(self)
        for tile in self.fov:
            if type(tile) != NPC:
                self.board.shadows.add(tile)
