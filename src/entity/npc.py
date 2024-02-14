### IMPORTS ###
import pygame as pg

from entity import Entity
from util.pathfind import pathfind


class NPC(Entity):
    def follow_entity(self, target, board):
        path = pathfind(board, self, target)
        #print(path)
        #self.move(path.pop()["direction"], board)
