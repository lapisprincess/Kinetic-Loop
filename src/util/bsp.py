### IMPORTS ###
import pygame as pg
import random
import math

from level.room import Room


### CONSTANTS ###
MIN_ROOM_SIZE = 7


### BSP ###
class Partition(pg.Rect):

    # split one partition into two, based on randomly selected direction
    def split(self, tile_width: int):
        min_room_size = MIN_ROOM_SIZE * tile_width

        # horizontal split
        if random.randint(0,1): 
            deviance = round(self.width / min_room_size)
            rand = random.randint(1, deviance)
            size_a = rand * (self.width / (deviance + 1))
            subpartition_a = Partition(
                self.left, self.top, 
                size_a, self.height)
            size_b = self.width - size_a
            subpartition_b = Partition(
                self.left + size_a, self.top, 
                size_b, self.height)

        # vertical split
        else: 
            deviance = round(self.height / min_room_size)
            rand = random.randint(1, deviance)
            size_a = rand * (self.height / (deviance + 1))
            subpartition_a = Partition(
                self.left, self.top, 
                self.width, size_a)
            size_b = self.height - size_a
            subpartition_b = Partition(
                self.left, self.top + size_a,
                self.width, size_b)

        # if either subpartition is too small, don't split. otherwise, return!
        if size_a < min_room_size or size_b < min_room_size: return None
        return (subpartition_a, subpartition_b)


    # build a room, add it to the partition and return
    def build_room(self, floor, wall, tilesize, min_tiles, max_tiles):
        part_left_tiles = math.ceil(self.left / tilesize) + 1
        part_top_tiles = math.ceil(self.top / tilesize) + 1
        part_width_tiles = math.floor(self.width / tilesize) - 1
        part_height_tiles = math.floor(self.height / tilesize) - 1

        width = random.randint(min_tiles, part_width_tiles)
        if width > max_tiles: width = max_tiles

        height = random.randint(min_tiles, part_height_tiles)
        if height > max_tiles: height = max_tiles

        left = part_left_tiles + random.randint(0, part_width_tiles - width)
        top = part_top_tiles + random.randint(0, part_height_tiles - height)
        return self.level.build_room((left, top), (width, height), floor, wall)


# split every partition a certain number of times
def bsp(level, complexity: int) -> list[Partition]:
    out = [Partition(level)]
    for lvl in range(0, complexity):
        for partition in out:
            new_partitions = partition.split(level.tile_width)
            if new_partitions != None: 
                out.remove(partition)
                for new_partition in new_partitions: 
                    out.append(new_partition)
    for partition in out: partition.level = level
    return out
