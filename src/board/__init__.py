### IMPORTS ###
import pygame as pg
import random
import math

import util.graphic as graphic
from util.fov import fov_los
from util.bsp import bsp

import board.tile as tile
from board.room import Room
from board.tunnel import Tunnel

from entity.player import Player
from entity.npc import NPC


FOV_WIDTH = 6


### BOARD CLASS ###
class Board(pg.Rect):
    def __init__(self, controls, tile_width, dimensions, middle=(0,0), visibility=False):
        self.surface = pg.Surface(dimensions)
        self.visibility, self.middle = visibility, middle
        self.controls, self.tile_width = controls, tile_width
        self.rooms, self.tunnels = [], []
        self.tiles = pg.sprite.Group()
        self.entities = pg.sprite.Group()
        self.layers = [self.tiles, self.rooms, self.tunnels, self.entities]
        self.player = None
        pg.Rect.__init__(self, (0,0), dimensions)

    def draw(self, surface):
        self.surface.fill("black")
        for thing in self.get_everything():
            if thing.visible: self.surface.blit(thing.image, thing.rect)
        surface.blit(self.surface, (self.left, self.top))

    def update(self, check_input = False):
        self.player = None
        for entity in self.entities.sprites():
            if type(entity) == Player:
                self.player = entity
                if self.visibility: fov_los(self, entity, FOV_WIDTH * self.tile_width)
        if self.player != None and self.middle != (0,0):
            self.left = -self.player.rect.left + self.middle[0]
            self.top = -self.player.rect.top + self.middle[1]
        # keep background color consistent between entities and tiles
        for entity in self.entities.sprites():
            tile_bgc = self.get_tile(entity.tile_x, entity.tile_y).bgc
            entity.image.set_bgc(tile_bgc)
        # register inputs, tick on input
        if not check_input: return
        for entity in self.entities.sprites():
            if type(entity) == Player:
                if entity.process_input(self.controls, self): self._update()

    # private tick function
    def _update(self):
        for room in self.rooms: room.update()
        for entity in self.entities.sprites():
            if type(entity) == NPC:
                if self.player == None: continue
                entity.follow_entity(self.player, self)
        self.entities.update()
        self.tiles.update()


    ### GETTERS ###
    def get_tile(self, tile_x, tile_y):
        for tunnel in self.tunnels:
            for tile in tunnel.tiles.sprites():
                if tile.tile_x == tile_x and tile.tile_y == tile_y: 
                    return tile
        for room in self.rooms:
            for tile in room.tiles.sprites():
                if tile.tile_x == tile_x and tile.tile_y == tile_y: 
                    return tile
        for tile in self.tiles.sprites():
            if tile.tile_x == tile_x and tile.tile_y == tile_y: 
                return tile
        return None

    def get_anything(self, tile_x, tile_y):
        things = []
        for thing in self.get_everything():
            if thing.tile_x == tile_x and thing.tile_y == tile_y:
                things.append(thing)
        return things

    def get_tile_at_pixel(self, pixel_x, pixel_y):
        for tile in self.tiles.sprites():
            if tile.pixel_collide(pixel_x, pixel_y): return tile
        return None

    def get_everything(self):
        everything = []
        for layer in self.layers:
            if type(layer) == pg.sprite.Group:
                for thing in layer.sprites():
                    everything.append(thing)
                continue
            for space in layer:
                for thing in space.tiles.sprites():
                    everything.append(thing)
        return everything

    def get_everything_within_range(self, center_tile_coord, tile_distance):
        things_in_range = []
        for thing in self.get_everything():
            dist = self.pixel_distance_between_tiles((thing.tile_x, thing.tile_y), center_tile_coord)
            if dist/self.tile_width < tile_distance:
                things_in_range.append(thing)
        return things_in_range

    def entity_at_pixel(self, pixel_coord):
        for entity in self.entities.sprites():
            if entity.pixel_collide(pixel_coord[0], pixel_coord[1]): return entity
        return None

    def pixel_distance_between_tiles(self, tile_coord1, tile_coord2):
        x1, y1 = tile_coord1[0], tile_coord1[1]
        x2, y2 = tile_coord2[0], tile_coord2[1]
        if   x2 >= x1: dx = x2 - x1
        elif x1 >  x2: dx = x1 - x2
        if   y2 >= y1: dy = y2 - y1
        elif y1 >  y2: dy = y1 - y2
        return math.sqrt(dx * dx + dy * dy)

    def get_random_floor(self):
        chosen_room = self.rooms[random.randint(0, len(self.rooms)-1)]
        return chosen_room.get_random_floor()


    ### MUTATORS ###
    def build_room(self, tile_coord, tile_dimension, floor, wall):
        if tile_dimension[0] <= 2 or tile_dimension[1] <= 2: return None
        new_room = Room(tile_coord, tile_dimension, floor, wall)
        for existing_room in self.rooms:
            if new_room.colliderect(existing_room): return None
        self.rooms.append(new_room)
        return new_room

    def generate_floor(self, complexity):
        for partition in bsp(self, complexity):
            floor, wall = tile.cobble_floor, tile.cobble_wall
            partition.build_room(floor, wall, 16, 3, 10)

    def connect_rooms(self, room1, room2):
        if room1.distance_to_other_room(room2) == None: return None
        new_tunnel = Tunnel(room1, room2, room1.floor, room1.wall)
        if new_tunnel == None: return None
        self.tunnels.append(new_tunnel)
