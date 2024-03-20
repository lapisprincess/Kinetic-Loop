""" main level object! levels are what the game is played on """

### IMPORTS ###
import random
import math

import pygame as pg

from util.space import pixel_distance
from util import pathfind as pf

from entity.player import Player
from entity import trait, Entity

from level.room import Room
from level.tunnel import Tunnel
from level.cursor import Cursor

from prop.stairs import Stairs

### level CLASS ###
class Level(pg.Rect):
    """ MFin Level class!

    handles a hefty amount of game mechanics,
    containing and updating entities, tiles, rooms, etc
    """
    def __init__(
            self, tile_width, dimensions,
            controls=None, middle=(0,0), visibility=False, name=""
    ):
        self.surface = pg.Surface(dimensions)
        self.visibility, self.middle = visibility, middle
        self.controls, self.tile_width = controls, tile_width
        self.player = None
        self.name = name
        self.left, self.top = 0, 0

        self.rooms = []
        self.game_objects = pg.sprite.Group()

        self.shadows = set()

        self.cursor = Cursor(self)
        self.cursor.traits.add(trait.fully_controllable)
        self.looking = False
        self.info = []
        self.log = None

        pg.Rect.__init__(self, (0,0), dimensions)


    ### DRAW METHODS ###
    def draw(self, surface):
        """ draw everything included in the level """
        self.surface.fill("black")

        self._draw_shadows()
        self._draw_everything()

        if self.looking:
            self.surface.blit(self.cursor.image, self.cursor.rect)

        surface.blit(self.surface, (self.left, self.top))

    # draw specifically known tiles that are out of view
    def _draw_shadows(self):
        for shadow_tile in self.shadows:
            if shadow_tile is not None and shadow_tile in self.get_all_tiles():
                shadow_tile.image.set_alpha(100)
                self.surface.blit(shadow_tile.image, shadow_tile.rect)

    # draw everything within view
    def _draw_everything(self):
        for room in self.rooms:
            for tile in room.tiles.sprites():
                if tile.visible:
                    tile.image.set_alpha(255)
                    self.surface.blit(tile.image, tile.rect)
        for gameobj in self.game_objects:
            if gameobj.visible:
                gameobj.image.set_alpha(255)
                self.surface.blit(gameobj.image, gameobj.rect)


    ### UPDATE METHODS ###
    def update(self, check_input = False):
        """ major update method! """

        # locate player
        for gameobj in self.game_objects:
            if isinstance(gameobj, Player):
                self.player = gameobj

        # general updates and adjustments
        for gameobj in self.game_objects:
            gameobj.update()
        for room in self.rooms:
            room.update()
        self._adjust_mid()
        self._adjust_entity_bgc()
        self.info = self._get_info()

        if self.player is not None:
            # automatically fast move player
            if self.player.fast_direction is not None:
                self.player.fast_move()
                self._take_entity_turns()

            # automatically move player along travel path
            elif self.player.travel_path is not None:
                self.player.travel()
                self._take_entity_turns()

            # process player input
            elif check_input:
                keys = pg.key.get_pressed()

                # adjust looking
                cond1 = keys[eval("pg." + self.controls['look'][0])]
                cond2 = self.looking and keys[eval("pg." + self.controls['unlook'][0])]
                if cond1 or cond2:
                    self.toggle_looking()

                # wait
                if keys[eval("pg." + self.controls['wait'][0])]:
                    self._take_entity_turns()

                # look
                if self.looking:
                    self.cursor.take_turn()
                    self.cursor.update()
                elif self.player.take_turn():
                    self._take_entity_turns()

                if keys[eval("pg." + self.controls['fire'][0])]:
                    if self.looking:
                        cursor_pos = self.cursor.tile_x, self.cursor.tile_y
                        self.player.attack_ranged(self.get(cursor_pos[0], cursor_pos[1]))
                        self.toggle_looking()

            # toggle whether everything is visible or not
            if not self.visibility:
                for tile in self.get_all_tiles():
                    tile.visible = True
                for gameobj in self.game_objects:
                    gameobj.visible = True

            if self.visibility and self.player.fov is not None:
                for gameobj in self.game_objects:
                    if gameobj in self.player.fov:
                        gameobj.visible = True
                    else:
                        gameobj.visible = False
                for tile in self.get_all_tiles():
                    if tile in self.player.fov:
                        tile.visible = True
                    else:
                        tile.visible = False

    def _take_entity_turns(self):
        for gameobj in self.game_objects:
            if gameobj == self.player or not isinstance(gameobj, Entity):
                continue
            gameobj.take_turn()

    def _adjust_mid(self):
        if (self.looking) and (self.middle != (0,0)):
            self.left = -self.cursor.rect.left + self.middle[0]
            self.top = -self.cursor.rect.top + self.middle[1]
        elif (self.player is not None) and (self.middle != (0,0)):
            self.left = -self.player.rect.left + self.middle[0]
            self.top = -self.player.rect.top + self.middle[1]

    # keep bgc consistent between level and entity
    def _adjust_entity_bgc(self):
        for gameobj in self.game_objects.sprites():
            tile = self.get_tile(gameobj.tile_x, gameobj.tile_y)
            if tile is None:
                print("Something's in the void......")
                print("Coords: ", gameobj.tile_x, gameobj.tile_y, "\n")
                continue
            tile_bgc = tile.colors[0]
            gameobj.image.set_bgc(tile_bgc)

    # get relevant info based on cursor/player position
    def _get_info(self):
        out = []
        if self.looking:
            cursor_x = self.cursor.rect.x / self.tile_width
            cursor_y = self.cursor.rect.y / self.tile_width

            tile_at_cursor = self.get_tile(cursor_x, cursor_y)
            if tile_at_cursor is not None and tile_at_cursor.visible:
                out = [tile_at_cursor.get_info()]
            else: out = []

            entity_at_cursor = self.get(cursor_x, cursor_y, Entity)
            if entity_at_cursor is not None and entity_at_cursor.visible:
                out.append(entity_at_cursor.get_info())

        else: out = [self.player.get_info()]

        return out


    ### GETTERS ###
    def get(self, tile_x, tile_y, tp=None):
        """ abstract getter to grab anything of a given type """

        gameobj = self.get_game_object(tile_x, tile_y, tp)
        if gameobj is not None:
            return gameobj

        tile = self.get_tile(tile_x, tile_y, tp)
        if tile is not None:
            return tile

        # nothing found :(
        return None

    def get_game_object(self, tile_x, tile_y, tp=None):
        """ get any game object on the board of specified type """
        search_coord = (tile_x, tile_y)

        for gameobj in self.game_objects:
            if gameobj is None:
                continue
            gameobj_coord = (gameobj.tile_x, gameobj.tile_y)
            if search_coord == gameobj_coord:
                if tp is None or isinstance(gameobj, tp):
                    return gameobj
        return None

    def get_entity(self, tile_x, tile_y):
        """ this method shouldn't be necessary, but here we are. """
        return self.get_game_object(tile_x, tile_y, Entity)
        # would you call bad inheritance 'code incest?'
    
    def get_tile(self, tile_x, tile_y, tp=None):
        """ get any tile on the board """
        search_coord = tile_x, tile_y

        for room in self.rooms:
            for tile in room.tiles:
                if tile is None:
                    continue
                tile_coord = (tile.tile_x, tile.tile_y)
                if search_coord == tile_coord:
                    if tp is None or isinstance(tile, tp):
                        return tile
        return None

    def get_all_tiles(self):
        """ since tiles are wrapped inside of rooms,
        this method pulls all tiles from all rooms """
        out = []
        for room in self.rooms:
            for tile in room.tiles:
                if tile is not None:
                    out.append(tile)
        return out

    def get_pixel(self, pixel_x, pixel_y, tp=None):
        """ abstract getter to grab anything of a given type, given pixel coord """
        pixel_x /= self.tile_width
        pixel_y /= self.tile_width
        gameobj = self.get_game_object(pixel_x, pixel_y, tp)
        if gameobj is not None:
            return gameobj

        tile = self.get_tile(pixel_x, pixel_y, tp)
        if tile is not None:
            return tile

        # nothing found :(
        return None

    def get_everything_within_range(self, center_tile_coord, tile_distance):
        """ get everything within a tile distance """
        tile_distance /= 10
        things_in_range = []
        for gameobj in self.game_objects:
            dist = pixel_distance(
                (gameobj.tile_x, gameobj.tile_y), center_tile_coord
            )
            if (dist/self.tile_width) < tile_distance:
                things_in_range.append(gameobj)
        for tile in self.get_all_tiles():
            dist = pixel_distance(
                (tile.tile_x, tile.tile_y), center_tile_coord
            )
            if (dist/self.tile_width) < tile_distance:
                things_in_range.append(tile)
        return things_in_range

    def get_room(self, tile_x, tile_y):
        """ getter to grab room given tile location """
        for room in self.rooms:
            room_range_x = range(room.left, room.left + room.width)
            room_range_y = range(room.top, room.top + room.height)
            if tile_x in room_range_x and tile_y in room_range_y:
                return room
        return None

    def get_all_rooms(self):
        """ get all rooms that are strictly rooms, not tunnels """
        all_rooms = []
        for room in self.rooms:
            if not isinstance(room, Tunnel):
                all_rooms.append(room)
        return all_rooms


    def get_random_floor(self, frustration=0):
        """ get a random floor """
        if frustration == 5:
            return None

        rooms_only = []
        for room in self.rooms:
            if not isinstance(room, Tunnel):
                rooms_only.append(room)

        chosen_room = rooms_only[random.randint(0, len(rooms_only)-1)]
        chosen_floor = chosen_room.get_random_floor()
        coord = (chosen_floor.tile_x, chosen_floor.tile_y)
        if self.get(coord[0], coord[1], Entity) is None:
            self.get_random_floor(frustration+1)
        return chosen_floor

    def are_connected(self, room1, room2):
        """ checks if two rooms are connected """
        for tunnel in self.rooms:
            if not isinstance(tunnel, Tunnel):
                continue
            if room1 in tunnel.rooms and room2 in tunnel.rooms:
                return True
        return False


    ### MUTATORS ###
    def add_gameobj(self, gameobj, tile_coord=None):
        """ add any game object, 
        either at a specified or random location """
        if tile_coord is None:
            tile = self.get_random_floor()
            tile_coord = (tile.tile_x, tile.tile_y)
            while self.get_game_object(tile_coord[0], tile_coord[1]) is not None:
                tile = self.get_random_floor()
                tile_coord = (tile.tile_x, tile.tile_y)
        gameobj.tile_x = tile_coord[0]
        gameobj.tile_y = tile_coord[1]
        gameobj.level = self
        self.game_objects.add(gameobj)

    def log_message(self, message):
        """ print a message either in the game log or in console """
        if self.log is None:
            print(message)
        else:
            self.log.add_message(message)

    def build_room(self, tile_coord, tile_dimension, floor, wall):
        """ try and build a new room, given no overlaps """
        if tile_dimension[0] <= 2 or tile_dimension[1] <= 2:
            return None
        new_room = Room(tile_coord, tile_dimension, floor, wall)
        for existing_room in self.rooms:
            if new_room.colliderect(existing_room):
                return None
        self.rooms.append(new_room)
        return new_room

    def connect_rooms(self, room1, room2, max_dist = 8):
        """ connect two rooms via tunnel """
        new_tunnel = Tunnel(
            room1, room2,
            room1.floor, room1.wall,
            fix_rooms = False
        )

        # conditions when rooms can't be connected
        if new_tunnel == (0, 0, 0, 0):
            return False
        if max_dist is not None and new_tunnel.distance > max_dist:
            return False
        for room in self.rooms:
            if room not in (room1, room2) and room.overlap(new_tunnel):
                return False

        if new_tunnel is None:
            return False

        # successful connection
        room1.connections.append(room2)
        room2.connections.append(room1)
        new_tunnel = Tunnel(
            room1, room2,
            room1.floor, room1.wall,
            fix_rooms=True
        )
        self.rooms.append(new_tunnel)
        return True

    def validate(self):
        """ ensures every room is connected to every other room TODO """
        for room1 in self.get_all_rooms():
            for room2 in self.get_all_rooms():
                if room1 is room2:
                    continue
                tile1 = room1.get_random_floor()
                center1 = tile1.tile_x, tile1.tile_y
                tile2 = room2.get_random_floor()
                center2 = tile2.tile_x, tile2.tile_y
                if pf.pathfind(center1, center2, self) is None:
                    return False
        return True


    def kill_orphans(self):
        """ there were orphan rooms.
        This method kills orphans (just like me fr). """

        for room in self.get_all_rooms():
            if len(room.connections) == 0:
                self.rooms.remove(room)

    def toggle_looking(self):
        """ toggle whether the player is in look mode or not """
        self.looking = not self.looking
        self.cursor.tile_x = self.player.tile_x
        self.cursor.tile_y = self.player.tile_y
        self.cursor.update()


def connect_floors(lower, upper):
    random_lower_floor = lower.get_random_floor()
    random_upper_floor = upper.get_random_floor()

    random_lower_coord = (random_lower_floor.tile_x, random_lower_floor.tile_y)
    random_upper_coord = (random_upper_floor.tile_x, random_upper_floor.tile_y)
    stairs_up = Stairs(random_lower_coord, 'up', upper, random_upper_coord)
    stairs_down = Stairs(random_upper_coord, 'down', lower, random_lower_coord)

    lower.add_gameobj(stairs_up, random_lower_coord)
    upper.add_gameobj(stairs_down, random_upper_coord)