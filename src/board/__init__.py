### IMPORTS ###
import pygame as pg
import random

import graphic

from board.entity.player import Player


### BOARD CLASS ###
'''
The board class is the 'system', the glue that keeps everything together.
Ideally coordinates everything and has tools like pathfinding algos
and dungeon generation!
Also manages the entity, tile, and object subclasses, all of which depend
on information stored by the board.

Instance variables:
    - tiles, entities       # sprite groups holding tiles/entities  : pg.Group
    - screen_x, screen_y    # where on the screen to draw the board : int
'''
class Board():
    def __init__(self, screen_coord):
        # initialize our two sprite groups
        self.tiles, self.entities = pg.sprite.Group(), pg.sprite.Group()
        self.screen_x, self.screen_y = screen_coord[0], screen_coord[1]

    def draw(self, surface):
        self.tiles.draw(surface)
        self.entities.draw(surface)

    '''
    Update method which both keeps everything coordinated spacially and
    logically, and also handles grabbing inputs for the player to handle
    (if one exists). The param check_input is used to avoid key repeats.

    @param check_input  # whether we can check for inputs   : bool
    '''
    def update(self, check_input = False):
        # keep background color consistent between entities and tiles
        for entity in self.entities.sprites():
            tile_bgc = self.get_tile(entity.tile_x, entity.tile_y).bgc
            entity.image.set_bgc(tile_bgc)

        # everything needs to align with the board
        for sprite in (self.tiles.sprites() + self.entities.sprites()):
            sprite.rect.x = self.screen_x + sprite.tile_x * graphic.tile_width
            sprite.rect.y = self.screen_y + sprite.tile_y * graphic.tile_width

        if not check_input: return

        keys = pg.key.get_pressed()
        for entity in self.entities.sprites():
            if type(entity) == Player:
                if entity.process_input(keys, self): self.__update()

    '''
    Standard version of update which ticks all entities and tiles once.
    '''
    def __update(self):
        self.entities.update()
        self.tiles.update()

    '''
    Given x,y tile coordinates, return tile located there, if any.
    @param tile_x, tile_y   # x,y coord of tile on board    : int
    @return                 # tile at x,y coord, or None    : Tile
    '''
    def get_tile(self, tile_x, tile_y):
        for tile in self.tiles.sprites():
            if tile.tile_x == tile_x and tile.tile_y == tile_y:
                return tile
        return None

    '''
    Method which picks a random floor tile to return.
    '''
    def get_random_floor(self):
        floors = []
        for tile in self.tiles.sprites():
            if tile.tile_type == 'floor': floors.append(tile)
        chosen_tile = floors[random.randint(0, len(floors)-1)]
        return floors[random.randint(0, len(floors)-1)]


    '''
    The build_room method should build a room at (tile_x, tile_y) of
    given width and height. We start by defining the extremities as the
    specified wall type, then fill the interior with the floor type.
    If no floor or wall type is specified, we instead use pre-defined tiles.
    '''
    def build_room(self, coord, dimension, floor, wall):
        tile_x, tile_y = coord[0], coord[1]
        width, height = dimension[0], dimension[1]
        for y in range(tile_y, tile_y + height + 1):
            for x in range(tile_x, tile_x + width + 1):
                if self.get_tile(x, y) != None: return False
        width += 1
        height += 1

        # define walls
        for i in range(tile_x, tile_x + width):
            self.tiles.add(wall.clone(i, tile_y))
        for i in range(tile_x, tile_x + width):
            self.tiles.add(wall.clone(i, tile_y + height))
        for i in range(tile_y, tile_y + height):
            self.tiles.add(wall.clone(tile_x, i))
        for i in range(tile_y, tile_y + height + 1):
            self.tiles.add(wall.clone(tile_x + width, i))

        # fill in floor
        for y in range(tile_y + 1, tile_y + height):
            for x in range(tile_x + 1, tile_x + width):
                self.tiles.add(floor.clone(x, y))

        return True
