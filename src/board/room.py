import pygame as pg
import random

class Room(pg.Rect):
    def __init__(self, tile_coord, tile_dimension, floor, wall):
        self.tiles = pg.sprite.Group()
        self.tile_coord, self.tile_dimension = tile_coord, tile_dimension
        self.floor, self.wall = floor, wall
        tile_x, tile_y = tile_coord[0], tile_coord[1]
        tile_width, tile_height = tile_dimension[0]-1, tile_dimension[1]-1
        # walls
        for i in range(tile_x, tile_x + tile_width):
            self.tiles.add(wall.clone(i, tile_y))
        for i in range(tile_x, tile_x + tile_width):
            self.tiles.add(wall.clone(i, tile_y + tile_height))
        for i in range(tile_y, tile_y + tile_height):
            self.tiles.add(wall.clone(tile_x, i))
        for i in range(tile_y, tile_y + tile_height + 1):
            self.tiles.add(wall.clone(tile_x + tile_width, i))
        # floor
        for y in range(tile_y + 1, tile_y + tile_height):
            for x in range(tile_x + 1, tile_x + tile_width):
                self.tiles.add(floor.clone(x, y))
        pg.Rect.__init__(self, tile_x, tile_y, tile_width, tile_height)

    def update(self):
        for tile in self.tiles: tile.update()

    def get_random_floor(self):
        floors = []
        for tile in self.tiles.sprites():
            if tile.tile_type == 'floor': floors.append(tile)
        return floors[random.randint(0, len(floors)-1)]

    def get_tile(self, tile_x, tile_y):
        for tile in self.tiles.sprites():
            if tile.tile_x == tile_x and tile.tile_y == tile_y:
                return tile
        return None

    def change_to_floor(self, tile_x, tile_y):
        tile = self.get_tile(tile_x, tile_y)
        if tile == None or tile.tile_type == "floor": return None
        self.tiles.remove(tile)
        new_tile = self.floor.clone(tile_x, tile_y)
        self.tiles.add(new_tile)

    def direction_to_other_room(self, other):
        self_left, self_top   = self.tile_coord[0], self.tile_coord[1]
        other_left, other_top = other.tile_coord[0], other.tile_coord[1]
        self_right  = self_left + self.tile_dimension[0]
        other_right = other_left + other.tile_dimension[0]
        self_bottom = self_top + self.tile_dimension[1]
        other_bottom = other_top + other.tile_dimension[1]

        for x in range(self_left + 1, self_right - 1):
            if x in range(other_left + 1, other_right - 1):
                if self_bottom < other_top: return "south"
                if self_top > other_bottom: return "north"
        for y in range(self_top + 1, self_bottom - 1):
            if y in range(other_top + 1, other_bottom - 1):
                if self_right < other_left: return "east"
                if self_left > other_right: return "west"
        return None


    def distance_to_other_room(self, other):
        self_left, self_top   = self.tile_coord[0], self.tile_coord[1]
        other_left, other_top = other.tile_coord[0], other.tile_coord[1]
        self_right  = self_left + self.tile_dimension[0]
        other_right = other_left + other.tile_dimension[0]
        self_bottom = self_top + self.tile_dimension[1]
        other_bottom = other_top + other.tile_dimension[1]

        direction = self.direction_to_other_room(other)
        match direction:
            case "north": return(self_top - other_bottom)
            case "south": return(other_top - self_bottom)
            case "east" : return(other_left - self_right)
            case "west" : return(self_left - other_right)
            case _: return None
        return 0
