""" Various traits usable when defining entities """

### IMPORTS ###
import random
import pygame as pg

import util.pathfind as pf

from prop.stairs import Stairs

from entity.player import Player


## TRAIT CLASS
class Trait:
    """ TODO """
    def __init__(self, priority, method):
        self.priority = priority
        self.method = method

    def act(self, parent):
        """ TODO """
        return self.method(parent)



## MOVEMENT TRAITS
# NOTE: movements that use multiple keys must come first to work!
MOVEMENTS = [
    'north-east', 'north-west', 'south-east', 'south-west',
    'fast-north', 'fast-south', 'fast-east', 'fast-west',
    'north', 'south', 'west', 'east',
    'up', 'down',
]

def control(parent, full=False):
    """ Allows entity to be controlled """
    pressed_keys = pg.key.get_pressed()

    # cycle through all possible movements
    for move in MOVEMENTS:
        needed_controls = parent.level.controls[move]
        check_controls = []

        # check if all key values are matched
        for key in needed_controls:
            if pressed_keys[eval("pg." + key)]:
                check_controls.append(True)
            else: check_controls.append(False)

        # if all keys that need to be pressed are pressed, success!
        if all(check_controls):
            if 'fast' in move:
                parent.fast_direction = move[move.index('-')+1:]
                return True
            return parent.move(move, full)

    # no move was made
    return False

controllable = Trait(2, control)


def full_control(parent):
    """ Control entity with no effects """
    return control(parent, True)
fully_controllable = Trait(2, full_control)


def wander(parent):
    """ Make entity wander randomly """
    direction = random.randint(0, len(MOVEMENTS) - 1)
    return parent.move(MOVEMENTS[direction])
    """
    if attempt:
        self.frustration_i = 0
        return True
    elif (self.frustration == self.frustration_i):
        self.frustration_i = 0
        return False
    else:
        self.frustration_i += 1
        return self.act(parent)
    """
wandering = Trait(3, wander)


def pathfind_trait(parent, target):
    """ Placeholder pathfinding trait """
    if target is None:
        return None
    parent_coord = (parent.tile_x, parent.tile_y)
    target_coord = (target.tile_x, target.tile_y)
    path = pf.pathfind(parent_coord, target_coord, parent.level)
    if path is not None and len(path) != 0:
        return parent.move(path[0])
    return None


def ranged(parent, target):
    cond1 = parent.equipped["Weapon"].type = "ranged"
    cond2 = target in parent.fov
    if cond1 and cond2:
        pass


def target_nearby(parent):
    """ Target any nearby entity (only player for now) """
    if parent.target is None:
        for gameobj in parent.get_surrounding_game_objects():
            if gameobj is parent.target:
                parent.attack(parent.target)
        for thing in parent.fov:
            if isinstance(thing, Player):
                parent.target = thing
                return True
    return pathfind_trait(parent, parent.target)
hostile = Trait(2, target_nearby)


all_traits = {
    "hostile": hostile,
    "wandering": wandering,
    "controllable": controllable,
    "fully_controllable": fully_controllable,
}