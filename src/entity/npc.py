### IMPORTS ###
import pygame as pg

from entity import Entity
from util.pathfind import pathfind


class NPC(Entity):
    def follow_entity(self, target, board):
        self_coord = (self.tile_x, self.tile_y)
        target_coord = (target.tile_x, target.tile_y)
        path = pathfind(board, self_coord, target_coord)
        self.move(path.pop()["direction"], board)
