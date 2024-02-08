import pygame as pg
import random
import math

from board.tile import cobble_floor
from board.tile import cobble_wall

# partitioning work (needed for dungeon generation)
def bsp(board, complexity):
    out = [Partition(board)]
    for i in range(0, complexity):
        for j in range(0, len(out)):
            new_partitions = out[j].split(5, board.tile_width)
            if new_partitions != None: 
                for new_partition in new_partitions: 
                    out.append(new_partition)
    for partition in out: partition.board = board
    return out

class Partition(pg.Rect):
    def split(self, min_room_size_tiles, tile_width):
        min_room_size = min_room_size_tiles * tile_width
        if random.randint(0,1): # horizontal split
            deviance = round(self.width / min_room_size)
            rand = random.randint(1, deviance)
            size_a = rand * (self.width / (deviance + 1))
            size_b = self.width - size_a
            subpartition_a = Partition(
                    self.left, self.top, 
                    size_a, self.height)
            subpartition_b = Partition(
                    self.left + size_a, self.top, 
                    size_b, self.height)
        else: # vertical split
            deviance = round(self.height / min_room_size)
            rand = random.randint(1, deviance)
            size_a = rand * (self.height / (deviance + 1))
            size_b = self.height - size_a
            subpartition_a = Partition(
                    self.left, self.top, 
                    self.width, size_a)
            subpartition_b = Partition(
                    self.left, self.top + size_a,
                    self.width, size_b)
        if size_a < min_room_size or size_b < min_room_size: return None
        return (subpartition_a, subpartition_b)

    def build_room(self, floor, wall, tilesize, min_tiles, max_tiles):
        part_left_tiles = math.ceil(self.left / tilesize)
        part_top_tiles = math.ceil(self.top / tilesize)
        part_width_tiles = math.floor(self.width / tilesize)
        part_height_tiles = math.floor(self.height / tilesize)

        width = random.randint(min_tiles, part_width_tiles)
        if width > max_tiles: width = max_tiles
        height = random.randint(min_tiles, part_height_tiles)
        if height > max_tiles: height = max_tiles

        left = part_left_tiles + random.randint(0, part_width_tiles - width)
        top = part_top_tiles + random.randint(0, part_height_tiles - height)
        self.board.build_room((left, top), (width, height), floor, wall)
