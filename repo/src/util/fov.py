import pygame as pg

import util.direction as direction
from board.tile import Tile


# board gets mutated to fit los; seer stays constant
def fov_los(board, seer, pixel_max_dist):
    for tile in board.get_everything():
        tile.visible = False
    for tile in board.get_everything_within_range((seer.tile_x, seer.tile_y), 0.5):
        tile.visible = True
        #if tile.visible == True: continue
        visible_tiles = _line(board, seer, tile)
        for line_tile in visible_tiles: line_tile.visible = True
    seer.visible = True


# pixel_coord is a tuple defined as (x, y)
def _line(board, source, dest):
    x_src, x_dst = source.tile_x, dest.tile_x
    y_src, y_dst = source.tile_y, dest.tile_y

    line_direction = direction.match_direction((x_src, y_src), (x_dst, y_dst))
    dx = abs(x_src - x_dst)
    dy = abs(y_src - y_dst)

    out = set()
    if dx == 0 and dy == 0:
        return out
    elif dx > dy:
        y = 0
        for x in range(0, dx):
            if dy == 0: y = 0
            elif x % dy == dy - 1: y += 1
            mod = direction.necessary_movement(line_direction)
            mod_x1, mod_x2 = x * mod[0], (x - 1) * mod[0]
            mod_y = y * mod[1]
            things  = board.get_anything(x_src + mod_x1, y_src + mod_y)
            things += board.get_anything(x_src + mod_x2, y_src + mod_y)
            for thing in things:
                out.add(thing)
                if type(thing) == Tile and thing.tile_type == 'wall': 
                    return out
    elif dy >= dx:
        x = 0
        for y in range(0, dy):
            if dx == 0: x = 0
            elif y % dx == dx - 1: x += 1
            mod = direction.necessary_movement(line_direction)
            mod_x = x * mod[0]
            mod_y1, mod_y2 = y * mod[1], (y - 1) * mod[1]
            things  = board.get_anything(x_src + mod_x, y_src + mod_y1)
            things += board.get_anything(x_src + mod_x, y_src + mod_y2)
            for thing in things:
                out.add(thing)
                if type(thing) == Tile and thing.tile_type == 'wall': 
                    return out
    return out
