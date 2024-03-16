### IMPORTS ###
import pygame as pg

import math
import time

import util.direction as direction


### NODE CLASS ###
class Node:
    def __init__(self, x, y, dest, prev=None):
        self.x, self.y = x, y
        self.prev = prev

        if prev == None: self.g = 0
        else: self.g = prev.g + 1
        self.h = self.heuristic(dest)
        self.f = self.g + self.h

        self.neighbors = []
        for neighbor in direction.get_all_neighbors((x, y)):
            self.neighbors.append((neighbor[0], neighbor[1]))

    def heuristic(self, dest):
        x = abs(dest[0] - self.x)
        y = abs(dest[1] - self.y)
        dist = round(math.sqrt(x * x + y * y))
        return dist



def pathfind(source, dest, level):
    """ main pathfinding method, using A* algo """
    open_set = []
    open_set.append(Node(source[0], source[1], dest))
    frustration = 0

    while len(open_set) > 0 and frustration < 1000:
        # find the tile with the lowest score
        current = None
        for node in open_set:
            if (current is None) or (node.f < current.f):
                current = node
        if current is None:
            break

        # if tile is dest, return reconstructed path!
        if (current.x, current.y) == dest:
            return reconstruct_path(current)

        open_set.remove(current)
        for neighbor in current.neighbors:
            neighbor_tile = level.get_tile(neighbor[0], neighbor[1])
            if not neighbor_tile.traversable:
                continue

            tentative_node = Node(neighbor[0], neighbor[1], dest, current)
            added = False
            for node in open_set:
                if neighbor[0] == node.x and neighbor[1] == node.y:
                    if tentative_node.g < node.g:
                        node = tentative_node
                    added = 1

            if not added:
                open_set.append(tentative_node)

        frustration+=1


    # no path possible
    return None

def reconstruct_path(current):
    full_path = []
    while current.prev != None:
        current_loc = (current.x, current.y)
        prev_loc = (current.prev.x, current.prev.y)
        step = direction.match_direction(prev_loc, current_loc)
        full_path.append(step)
        current = current.prev
    full_path.reverse()
    return full_path


# I AM A FUCKING GOD FOR MAKING THIS WORK T~T
# IT ONLY TOOK ME ONE WHOLE FUCKING MONTH GAHRAHRHAH
