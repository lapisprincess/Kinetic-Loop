### IMPORTS ###
import pygame as pg
import random

from board.room import Room


### TUNNEL CLASS ###
'''
building a tunnel involves four steps:
    1. check whether the rooms allign, get direction from room1 to room2
    2. get a random location which fits between the intersect of both rooms
    3. build a room using these new coordinates
    4. change walls on both sides to floors
'''
class Tunnel(Room):
    def __init__(self, room1, room2, floor, wall, fix_rooms = True):
        self.rooms = [room1, room2]
        room1_left, room1_top   = room1.tile_coord[0], room1.tile_coord[1]
        room2_left, room2_top   = room2.tile_coord[0], room2.tile_coord[1]
        room1_right             = room1_left + room1.tile_dimension[0]
        room2_right             = room2_left + room2.tile_dimension[0] 
        room1_bottom            = room1_top  + room1.tile_dimension[1]
        room2_bottom            = room2_top  + room2.tile_dimension[1]
        self.distance, direction, overlaps = 0, None, []

        # figure out what direction room1 is from room2
        for x in range(room1_left + 1, room1_right - 1):
            if x in range(room2_left + 1, room2_right - 1):
                overlaps.append(x)
                if room1_bottom <= room2_top: direction = "south"
                if room1_top >= room2_bottom: direction = "north"
        for y in range(room1_top + 1, room1_bottom - 1):
            if y in range(room2_top + 1, room2_bottom - 1):
                overlaps.append(y)
                if room1_right <= room2_left: direction = "east"
                if room1_left >= room2_right: direction = "west"

        if direction == None: return None
        if direction == "north" or direction == "south":
            if room1_right < room2_left or room1_left > room2_right:
                print("Diagonal")
                return None
            if room2_right < room1_left or room2_left > room1_right:
                print("Diagonal")
                return None
        if direction == "east" or direction == "west":
            if room1_bottom < room2_top or room1_top > room2_bottom:
                print("Diagonal")
                return None
            if room2_bottom < room1_top or room2_top > room1_bottom:
                print("Diagonal")
                return None

        # where to connect the rooms
        chosen_overlap = overlaps[random.randint(0, len(overlaps)-1)]

        match direction:
            case "north": 
                self.distance = room1_top - room2_bottom + 2
                coord = (chosen_overlap - 1, room2_bottom - 1)
                dimension = (3, self.distance)
                Room.__init__(self, coord, dimension, floor, wall)
                self.change_to_floor(chosen_overlap, room1_top)
                self.change_to_floor(chosen_overlap, room2_bottom - 1)
                if fix_rooms:
                    room1.change_to_floor(chosen_overlap, room1_top)
                    room2.change_to_floor(chosen_overlap, room2_bottom - 1)
            case "south": 
                self.distance = room2_top - room1_bottom + 2
                coord = (chosen_overlap - 1, room1_bottom - 1)
                dimension = (3, self.distance)
                Room.__init__(self, coord, dimension, floor, wall)
                self.change_to_floor(chosen_overlap, room1_bottom - 1)
                self.change_to_floor(chosen_overlap, room2_top)
                if fix_rooms:
                    room1.change_to_floor(chosen_overlap, room1_bottom - 1)
                    room2.change_to_floor(chosen_overlap, room2_top)
            case "east" : 
                self.distance = room2_left - room1_right + 2
                coord = (room1_right - 1, chosen_overlap - 1)
                dimension = (self.distance, 3)
                Room.__init__(self, coord, dimension, floor, wall)
                self.change_to_floor(room1_right - 1, chosen_overlap)
                self.change_to_floor(room2_left, chosen_overlap)
                if fix_rooms:
                    room1.change_to_floor(room1_right - 1, chosen_overlap)
                    room2.change_to_floor(room2_left, chosen_overlap)
            case "west" : 
                self.distance = room1_left - room2_right + 2
                coord = (room2_right - 1, chosen_overlap - 1)
                dimension = (self.distance, 3)
                Room.__init__(self, coord, dimension, floor, wall)
                self.change_to_floor(room2_right - 1, chosen_overlap)
                self.change_to_floor(room1_left, chosen_overlap)
                if fix_rooms:
                    room1.change_to_floor(room2_right - 1, chosen_overlap)
                    room2.change_to_floor(room1_left, chosen_overlap)
