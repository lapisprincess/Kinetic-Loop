### IMPORTS ###
import pygame as pg
import random
import math

import util.graphic as graphic
from util.space import pixel_collide

import board.tile as tile
from board.room import Room
from board.tunnel import Tunnel
from board.cursor import Cursor

from entity.player import Player
from entity.npc import NPC
import entity.trait as trait

### BOARD CLASS ###
class Board(pg.Rect):
    def __init__(
            self, controls, 
            tile_width, dimensions, 
            middle=(0,0), visibility=False
    ):
        self.surface = pg.Surface(dimensions)
        self.visibility, self.middle = visibility, middle
        self.controls, self.tile_width = controls, tile_width
        self.player = None

        self.rooms, self.tunnels = [], []
        self.tiles = pg.sprite.Group()
        self.entities = pg.sprite.Group()
        self.layers = [self.tiles, self.rooms, self.tunnels, self.entities]

        self.shadows = set()

        self.cursor = Cursor(self.tile_width, self)
        self.cursor.traits.add(trait.fully_controllable)
        self.looking = False
        self.info = []
        self.log = None

        pg.Rect.__init__(self, (0,0), dimensions)


    ### DRAW METHODS ###
    def draw(self, surface):
        self.surface.fill("black")
        self._draw_shadows()
        self._draw_everything()
        if self.looking: self.surface.blit(self.cursor.image, self.cursor.rect)
        surface.blit(self.surface, (self.left, self.top))

    # draw specifically known tiles that are out of view
    def _draw_shadows(self):
        for shadow_tile in self.shadows:
            shadow_tile.image.set_alpha(100)
            self.surface.blit(shadow_tile.image, shadow_tile.rect)

    # draw everything within view
    def _draw_everything(self):
        for thing in self.get_everything():
            if thing.visible: 
                thing.image.set_alpha(255)
                self.surface.blit(thing.image, thing.rect)


    ### UPDATE METHODS ###
    def update(self, check_input = False):
        
        # standard updates
        self.entities.update()
        self.tiles.update()
        for room in self.rooms: room.update()

        # locate player
        for entity in self.entities.sprites():
            if (type(entity) == Player): self.player = entity

        # adjust visibility around player
        if (self.visibility) and (self.player != None): 
            for tile in self.get_everything(): 
                if tile in self.player.fov: tile.visible = True
                else: tile.visible = False

        # adjust middle around player
        self._adjust_mid()
        self._adjust_entity_bgc()
        self.info = self._get_info()

        # automatically move player if in fast mode
        if self.player.fast_direction != None:
            self.player.fast_move()
            self._take_entity_turns()

        # rest of update reacts off inputs
        if (not check_input) or (self.player == None): return
        keys = pg.key.get_pressed()

        # adjust looking
        cond1 = keys[eval("pg." + self.controls['look'][0])]
        cond2 = self.looking and keys[eval("pg." + self.controls['unlook'][0])]
        if cond1 or cond2: self.toggle_looking()

        if keys[eval("pg." + self.controls['wait'][0])]:
            self._take_entity_turns()

        if self.looking: 
            self.cursor.take_turn()
            self.cursor.update()
        elif self.player.take_turn(): self._take_entity_turns()

    # private tick function
    def _take_entity_turns(self):
        for entity in self.entities.sprites():
            if entity == self.player: continue
            entity.take_turn()

    # adjust board to project around player
    def _adjust_mid(self):
        if (self.looking) and (self.middle != (0,0)):
            self.left = -self.cursor.rect.left + self.middle[0]
            self.top = -self.cursor.rect.top + self.middle[1]
        elif (self.player != None) and (self.middle != (0,0)):
            self.left = -self.player.rect.left + self.middle[0]
            self.top = -self.player.rect.top + self.middle[1]

    # keep bgc consistent between board and entity
    def _adjust_entity_bgc(self):
        for entity in self.entities.sprites():
            tile_bgc = self.get_tile(entity.tile_x, entity.tile_y).bgc
            entity.image.set_bgc(tile_bgc)

    # get relevant info based on cursor/player position
    def _get_info(self):
        out = []
        if self.looking:
            cursor_x = self.cursor.rect.x / self.tile_width
            cursor_y = self.cursor.rect.y / self.tile_width

            tile_at_cursor = self.get_tile(cursor_x, cursor_y)
            if tile_at_cursor != None and tile_at_cursor.visible: 
                out = [tile_at_cursor.get_info()]
            else: out = []
            
            entity_at_cursor = self.get_entity(cursor_x, cursor_y)
            if entity_at_cursor != None and entity_at_cursor.visible:
                out.append(entity_at_cursor.get_info())

        else: out = [self.player.get_info()]

        return out

    # toggle look
    def toggle_looking(self):
        self.looking = not self.looking
        self.cursor.tile_x = self.player.tile_x
        self.cursor.tile_y = self.player.tile_y
        self.cursor.update()



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

    def get_entity(self, tile_x, tile_y):
        for entity in self.entities.sprites():
            if entity.tile_x == tile_x and entity.tile_y == tile_y:
                return entity
        return None

    def get_tile_at_pixel(self, pixel_x, pixel_y):
        for tile in self.tiles.sprites():
            if tile.pixel_collide(pixel_x, pixel_y): return tile
        return None

    def get_entity_at_pixel(self, pixel_x, pixel_y):
        for entity in self.entities.sprites():
            if entity.pixel_collide(pixel_x, pixel_y):
                return entity
        return None
    
    def get_room_at_tile(self, tile_x, tile_y):
        for room in self.rooms + self.tunnels:
            if room.get_tile(tile_x, tile_y) != None:
                return room

    def get_anything(self, tile_x, tile_y):
        things = []
        for thing in self.get_everything():
            if thing.tile_x == tile_x and thing.tile_y == tile_y:
                things.append(thing)
        return things

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
            dist = self.pixel_distance_between_tiles(
                    (thing.tile_x, thing.tile_y), center_tile_coord)
            if dist/self.tile_width < tile_distance:
                things_in_range.append(thing)
        return things_in_range

    def pixel_distance_between_tiles(self, tile_coord1, tile_coord2):
        x1, y1 = tile_coord1[0], tile_coord1[1]
        x2, y2 = tile_coord2[0], tile_coord2[1]
        if   x2 >= x1: dx = x2 - x1
        elif x1 >  x2: dx = x1 - x2
        if   y2 >= y1: dy = y2 - y1
        elif y1 >  y2: dy = y1 - y2
        return math.sqrt(dx * dx + dy * dy)

    def get_random_floor(self):
        while True:
            chosen_room = self.rooms[random.randint(0, len(self.rooms)-1)]
            chosen_floor = chosen_room.get_random_floor()
            coord = (chosen_floor.tile_x, chosen_floor.tile_y)
            if self.get_entity(coord[0], coord[1]) == None: 
                break
        return chosen_floor

    def are_connected(self, room1, room2):
        for tunnel in self.tunnels:
            if room1 in tunnel.rooms and room2 in tunnel.rooms:
                return True
        return False

    def log_message(self, message):
        li_font = pg.font.Font("data/font.otf", size=14)
        if self.log == None: print(message)
        else: self.log.add_message(message)



    ### MUTATORS ###
    def add_entity(self, entity):
        self.entities.add(entity)
        entity.board = self

    def build_room(self, tile_coord, tile_dimension, floor, wall):
        if tile_dimension[0] <= 2 or tile_dimension[1] <= 2: return None
        new_room = Room(tile_coord, tile_dimension, floor, wall)
        for existing_room in self.rooms:
            if new_room.colliderect(existing_room): return None
        self.rooms.append(new_room)
        return new_room

    # connect two rooms with a tunnel
    def connect_rooms(self, room1, room2, max_dist = None):
        room2_left, room2_top = room2.tile_coord[0], room2.tile_coord[1]
        room2_right = room2.tile_coord[0] + room2.tile_dimension[0]
        room2_bottom = room2.tile_coord[1] + room2.tile_dimension[1]

        new_tunnel = Tunnel(
            room1, room2, 
            room1.floor, room1.wall, 
            fix_rooms = False
        )
        if new_tunnel == (0, 0, 0, 0): return False
        if max_dist != None and new_tunnel.distance > max_dist: return False

        for room in self.rooms:
            if (room != room1 and room != room2) and room.overlap(new_tunnel):
                return False

        if new_tunnel == None: return False
        else: 
            new_tunnel = Tunnel(
                room1, room2, 
                room1.floor, room1.wall, 
                fix_rooms=True
            )
            self.tunnels.append(new_tunnel)
            return True
