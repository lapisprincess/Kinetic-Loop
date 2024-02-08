import pygame as pg

import util.direction_management as dm

# A* ftw!!
# returns list of tiles forming shortest path between points
def pathfind(board, tile_coord1, tile_coord2):
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


def _pathfind(board, curr_location, dest, lvl):
    None


def _calculate_score(board, node):
    return 0


'''
node(direction, tile_from, tile_to, score)

score = dist from src + admissible heuristic

'''
