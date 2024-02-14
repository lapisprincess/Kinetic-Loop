### IMPORTS ###
import pygame as pg

from collections import defaultdict
import util.direction as d
import queue
import math

### PATHFINDER ###
# returns list of tiles forming shortest path between points
# adapted from wikipedia's A* pseudocode
# https://en.wikipedia.org/wiki/A*_search_algorithm
def pathfind(board, start, goal):
    discovered = set()
    discovered.add(start)
    origins = {}
    distances_start = {start: 0}
    heuristics = {start: _hrstc(board, start, goal)}

    while (len(discovered) != 0):
        curr = _lowest_discovered_heuristic(heuristics, discovered)
        if curr == goal:
            return _reconstruct_path(origins, curr)

        discovered.remove(curr)
        for direction in d.all_directions:
            (mod_x, mod_y) = d.necessary_movement(direction)
            mod_coord = (curr.tile_x + mod_x, curr.tile_y + mod_y)
            neighbor = board.get_tile(mod_coord[0], mod_coord[1])

            if neighbor == None: continue
            tentative = distances_start.get(curr) + 1
            neighbor_distance = distances_start.get(neighbor)
            if (neighbor_distance == None) or (tentative < neighbor_distance):
                origins[neighbor] = curr
                distances_start[neighbor] = tentative
                heuristics[neighbor] = _hrstc(board, neighbor, goal)
                discovered.add(neighbor)

    # couldn't reach goal
    return None


### HELPERS ###
# searches through a dictionary for key with the lowest value
def _lowest_discovered_heuristic(heuristics, discovered):
    lowest_node = None
    for node in discovered:
        score = heuristics.get(node)
        if (lowest_node == None) or (score != None and score < heuristics.get(lowest_node)):
            lowest_node = node
    return lowest_node

# takes two tiles and returns tile distance between them,
# regardless of walls or nonespace
def _hrstc(board, tile1, tile2):
    coord1, coord2 = tile1.rect.center, tile2.rect.center
    dx, dy = abs(coord2[0] - coord1[0]), abs(coord2[1] - coord1[1])
    dist = math.sqrt(dx * dx + dy * dy)
    out = round(dist / board.tile_width)
    return out
    
def _reconstruct_path(origins, current):
    total_path = [current]
    while (current in origins.keys()):
        current = origins[current]
        total_path.prepend(current)
    return total_path




'''

    GRAVEYARD

def _pathfind(board, tile_coord1, tile_coord2):
    curr_location = tile_coord1
    lvl = 0
    out = []
    #while curr_location != tile_coord2:

    out = []
    for direction in dm.all_directions:
        (x, y) = dm.necessary_movement(direction)
        adjusted_tile_coord = (tile_coord1[0] + x, tile_coord1[1] + y)
        adjusted_tile = board.get_tile(
            adjusted_tile_coord[0], adjusted_tile_coord[1])
        if adjusted_tile.tile_type == "wall": continue
        node = {
            'direction': direction,
            'tile_from': tile_coord1, 'tile_to': adjusted_tile_coord,
            'score': 0
        }
        _calculate_score(board, node)
        out.append(node)
    return out

    1. Start with empty priority queue P
    2. Start with empty set of previously visited nodes V
    3. Add start node s to P with cost f(s)
    4. If P is empty, then stop, no solution.
    5. Remove node x with lowest f(x) from P.
    6. If x is goal, stop with success.
    7. For each nx in successors of x:
        a) calculate f(nx) (= f(x) + delta)
        b) if nx not visited yet OR
              nx is in the priority queue P but with higher f(nx) OR
              nx has been visited but with higher f(nx)
           then place/update nx to P with new cost and
                update V to include (nx, f(nx), x)
    8. Go to 4

'''
