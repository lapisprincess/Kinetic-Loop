import pygame as pg
import random



'''
The build_room method should build a room at (tile_x, tile_y) of
given width and height. We start by defining the extremities as the
specified wall type, then fill the interior with the floor type.
If no floor or wall type is specified, we instead use pre-defined tiles.
'''
class Room(pg.Rect):
    def __init__(self, tile_coord, dimension, floor, wall):
        self.tiles = pg.sprite.Group()
        self.tile_coord, self.dimension = tile_coord, dimension
        tile_x, tile_y = tile_coord[0], tile_coord[1]
        width, height = dimension[0]+1, dimension[1]+1
        # walls
        for i in range(tile_x, tile_x + width):
            self.tiles.add(wall.clone(i, tile_y))
        for i in range(tile_x, tile_x + width):
            self.tiles.add(wall.clone(i, tile_y + height))
        for i in range(tile_y, tile_y + height):
            self.tiles.add(wall.clone(tile_x, i))
        for i in range(tile_y, tile_y + height + 1):
            self.tiles.add(wall.clone(tile_x + width, i))
        # floor
        for y in range(tile_y + 1, tile_y + height):
            for x in range(tile_x + 1, tile_x + width):
                self.tiles.add(floor.clone(x, y))
        pg.Rect.__init__(self, tile_x, tile_y, width, height)

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
