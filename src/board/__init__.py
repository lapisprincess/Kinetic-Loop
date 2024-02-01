### IMPORTS ###
import pygame as pg
import random

import util.graphic as graphic

from board.room import Room
from entity.player import Player


### BOARD CLASS ###
'''
The board class is the 'system', the glue that keeps everything together.
Ideally coordinates everything and has tools like pathfinding algos
and dungeon generation!

Instance variables:
    - tiles, entities       # sprite groups holding tiles/entities  : pg.Group
    - screen_x, screen_y    # where on the screen to draw the board : int
'''
class Board(pg.Rect):
    def __init__(self, controls, tile_width, dimensions):
        self.controls, self.tile_width = controls, tile_width
        self.rooms = []
        self.tiles = pg.sprite.Group()
        self.entities = pg.sprite.Group()
        pg.Rect.__init__(self, (0, 0), dimensions)

    def draw(self, surface):
        for room in self.rooms: room.tiles.draw(surface)
        self.tiles.draw(surface)
        self.entities.draw(surface)

    def update(self, check_input = False):
        # keep background color consistent between entities and tiles
        for entity in self.entities.sprites():
            tile_bgc = self.get_tile(entity.tile_x, entity.tile_y).bgc
            entity.image.set_bgc(tile_bgc)

        if not check_input: return
        for entity in self.entities.sprites():
            if type(entity) == Player:
                if entity.process_input(self.controls, self): self.__update()

    def __update(self):
        for room in self.rooms: room.update()
        self.entities.update()
        self.tiles.update()


    def get_tile(self, tile_x, tile_y):
        for tile in self.tiles.sprites():
            if tile.tile_x == tile_x and tile.tile_y == tile_y: return tile
        for room in self.rooms:
            x, y = room.tile_coord[0], room.tile_coord[1]
            w, h = room.dimension[0],  room.dimension[1]
            if (tile_x in range(x, x+w)) or (tile_y in range(y, y+h)):
                return room.get_tile(tile_x, tile_y)
        return None

    def get_random_floor(self):
        chosen_room = self.rooms[random.randint(0, len(self.rooms)-1)]
        return chosen_room.get_random_floor()

    def build_room(self, tile_coord, dimension, floor, wall):
        if dimension[0] <= 2 or dimension[1] <= 2: return None
        new_room = Room(tile_coord, dimension, floor, wall)
        for existing_room in self.rooms:
            if new_room.colliderect(existing_room): return None
        self.rooms.append(new_room)
        return new_room

    # returns a list of partitioned rectangles 
    def bsp(self, levels):
        out = [self.Partition(self)]
        i = 0
        while i <= levels:
            for i in range(0, len(out)):
                new_partitions = out[i].split(3, self.tile_width)
                if new_partitions != None: 
                    for new_partition in new_partitions: out.append(new_partition)
                    out.remove(out[i])
            i+=1
        return out

    class Partition(pg.Rect):
        def split(self, min_room_width_tiles, tile_width):
            min_room_width = min_room_width_tiles * tile_width
            if random.randint(0,1): # horizontal split
                deviance = round(self.width / min_room_width)
                rand = random.randint(1, deviance)
                size_a = rand * (self.width / (deviance + 1))
                size_b = self.width - size_a
                subpartition_a = Board.Partition(
                    self.left, self.top, 
                    size_a, self.height)
                subpartition_b = Board.Partition(
                    self.left + size_a, self.top, 
                    size_b, self.height)
            else: # vertical split
                deviance = round(self.height / min_room_width)
                rand = random.randint(1, deviance)
                size_a = rand * (self.height / (deviance + 1))
                size_b = self.height - size_a
                subpartition_a = Board.Partition(
                    self.left, self.top, 
                    self.width, size_a)
                subpartition_b = Board.Partition(
                    self.left, self.top + size_a,
                    self.width, size_b)
            if size_a < min_room_width or size_b < min_room_width: return None
            return (subpartition_a, subpartition_b)

        def build_room(self, board, floor, wall):
            None
