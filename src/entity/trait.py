### IMPORTS ###
import pygame as pg
import random

import util.pathfind as pf

from entity.player import Player
from entity.npc import NPC


### TRAIT CLASS ###
class Trait:
    def __init__(self, priority, method):
        self.priority = priority
        self.method = method

    def act(self, parent): return self.method(parent)



### MOVEMENT TRAITS ###
# NOTE: movements that use multiple keys must come first to work!
MOVEMENTS = [
    'north-east', 'north-west', 'south-east', 'south-west',
    'fast-north', 'fast-south', 'fast-east', 'fast-west',
    'north', 'south', 'west', 'east',
]

def control(parent, full=False):
    pressed_keys = pg.key.get_pressed()

    # cycle through all possible movements
    for move in MOVEMENTS:
        needed_controls = parent.board.controls[move]
        check_controls = []

        # check if all key values are matched
        for key in needed_controls:
            if pressed_keys[eval("pg." + key)]: check_controls.append(True)
            else: check_controls.append(False)

        # if all keys that need to be pressed are pressed, success!
        if all(check_controls):
            if 'fast' in move:
                parent.fast_direction = move[move.index('-')+1:]
                return True
            else: return parent.move(move, full)

    # no move was made
    return False

controllable = Trait(2, control)


def full_control(parent): return control(parent, True)
fully_controllable = Trait(2, full_control)


def wander(parent):
    direction = random.randint(0, len(MOVEMENTS) - 1)
    return parent.move(MOVEMENTS[direction])
    '''
    if attempt:
        self.frustration_i = 0
        return True
    elif (self.frustration == self.frustration_i):
        self.frustration_i = 0
        return False
    else:
        self.frustration_i += 1
        return self.act(parent)
    '''
wandering = Trait(3, wander)


# placeholder automatic pathfinding function
def pathfind(parent, target):
    parent_coord = (parent.tile_x, parent.tile_y)
    target_coord = (target.tile_x, target.tile_y)
    path = pf.pathfind(parent_coord, target_coord, parent.board)
    if path != None and len(path) != 0: return parent.move(path[0])



def target_nearby(parent):
    if parent.target == None:
        for thing in parent.fov:
            if type(thing) == Player:
                parent.target = thing
                return True
    else: return pathfind(parent, parent.target)
hostile = Trait(2, target_nearby)

# attack anything on sight
class Hostile(Trait): 
    pass

# attack only when provoked
class Defensive(Trait):
    def act(self, parent):
        None

# never attacks, flees when provoked
class Peaceful(Trait):
    def pas(self, parent):
        Trait.pas()
        None
        #if parent.state == 'combat': parent.state = 'flee'

# can attack neighbors
class Melee(Trait):
    def __init__(self):
        Trait.__init__(self, 9)
        self.action = False
        self.passive = True

# can attack from a distance
class Range(Trait):
    pass
