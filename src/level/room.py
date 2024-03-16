### IMPORTS ###
import pygame as pg
import random


### ROOM CLASS ###
class Room(pg.Rect):
    def __init__(self, tile_coord, tile_dimension, floor, wall):
        self.tiles = pg.sprite.Group()
        self.tile_coord, self.tile_dimension = tile_coord, tile_dimension
        self.floor, self.wall = floor, wall
        tile_x, tile_y = tile_coord[0], tile_coord[1]
        tile_width, tile_height = tile_dimension[0]-1, tile_dimension[1]-1

        center_tilex = round(tile_x + tile_width / 2)
        center_tiley = round(tile_y + tile_height / 2)
        self.center_tile_coord = (center_tilex, center_tiley)

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
        for tile in self.tiles:
            tile.update()

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

    def get_perimeter(self, level):
        out = []
        tile_x, tile_y = self.tile_coord[0], self.tile_coord[1]
        tile_width  = self.tile_dimension[0] - 1
        tile_height = self.tile_dimension[1] - 1
        for i in range(tile_x, tile_x + tile_width):
            out.append(level.get_tile(i, tile_y))
        for i in range(tile_x, tile_x + tile_width):
            out.append(level.get_tile(i, tile_y + tile_height))
        for i in range(tile_y, tile_y + tile_height):
            out.append(level.get_tile(tile_x, i))
        for i in range(tile_y, tile_y + tile_height + 1):
            out.append(level.get_tile(tile_x + tile_width, i))
        return out

    def change_to_floor(self, tile_x, tile_y):
        tile = self.get_tile(tile_x, tile_y)
        if tile == None: print("Actually, it's out of range!")
        if tile == None or tile.tile_type == "floor": 
            print("Already floor!")
            return None
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


    def overlap(self, room) -> bool:
        coord1, dmnsn1 = self.tile_coord, self.tile_dimension
        coord2, dmnsn2 = room.tile_coord, room.tile_dimension

        left1, right1 = coord1[0], coord1[0] + dmnsn1[0]
        top1, bottom1 = coord1[1], coord1[1] + dmnsn1[1]
        xrange1, yrange1 = range(left1, right1), range(top1, bottom1)

        left2, right2 = coord2[0], coord2[0] + dmnsn2[0]
        top2, bottom2 = coord2[1], coord2[1] + dmnsn2[1]
        xrange2, yrange2 = range(left2, right2), range(top2, bottom2)

        for x in xrange1:
            for y in yrange1:
                if x in xrange2 and y in yrange2: return True
        for x in xrange2:
            for y in yrange2:
                if x in xrange1 and y in yrange1: return True
        return False

    def overlapping_tiles(self, room):
        coord1, dmnsn1 = self.tile_coord, self.tile_dimension
        coord2, dmnsn2 = room.tile_coord, room.tile_dimension

        left1, right1 = coord1[0], coord1[0] + dmnsn1[0]
        top1, bottom1 = coord1[1], coord1[1] + dmnsn1[1]
        xrange1, yrange1 = range(left1, right1), range(top1, bottom1)

        left2, right2 = coord2[0], coord2[0] + dmnsn2[0]
        top2, bottom2 = coord2[1], coord2[1] + dmnsn2[1]
        xrange2, yrange2 = range(left2, right2), range(top2, bottom2)

        out = []
        for x in xrange1:
            top_tile = room.get_tile(x, top1)
            bot_tile = room.get_tile(x, bottom1)
            if top_tile != None and top_tile.tile_type == 'wall': 
                out.append(top_tile)
            if bot_tile != None and bot_tile.tile_type == 'wall': 
                out.append(bot_tile)
        for y in yrange1:
            left_tile  = room.get_tile(left1, y)
            right_tile = room.get_tile(right1, y)
            if left_tile  != None and left_tile.tile_type == 'wall': 
                out.append(left_tile)
            if right_tile != None and right_tile.tile_type == 'wall': 
                out.append(right_tile)
        return out


    # connect two rooms with a tunnel
    def connect_rooms(self, room2, max_dist = None):
        room2_left, room2_top = room2.tile_coord[0], room2.tile_coord[1]
        room2_right = room2.tile_coord[0] + room2.tile_dimension[0]
        room2_bottom = room2.tile_coord[1] + room2.tile_dimension[1]

        new_tunnel = Tunnel(
            self, room2, 
            self.floor, self.wall, 
            fix_rooms = False
        )
        if new_tunnel == (0, 0, 0, 0): return False
        if max_dist != None and new_tunnel.distance > max_dist: return False

        for room in self.rooms:
            if (room != self and room != room2) and room.overlap(new_tunnel):
                return False

        if new_tunnel == None: return False
        else: 
            new_tunnel = Tunnel(
                self, room2, 
                self.floor, self.wall, 
                fix_rooms=True
            )
            self.tunnels.append(new_tunnel)
            return True
