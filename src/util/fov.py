import pygame as pg

import util.direction as direction
from board.tile import Tile


# board gets mutated to fit los; seer stays constant
def fov_los(board, seer, pixel_max_dist):
    # start by making everything invisible
    for tile in board.get_everything(): tile.visible = False

    # draw a line from seer to every tile within sight
    seer_coord = (seer.tile_x, seer.tile_y) 
    for tile in board.get_everything_within_range(seer_coord, 0.5):
        tile_coord = (tile.tile_x, tile.tile_y)
        visible_tiles = bresenham_line(seer_coord, tile_coord)
        for tile in visible_tiles:
            tile_obj = board.get_tile(tile[0], tile[1])
            if tile_obj != None: 
                tile_obj.visible = True
                if tile_obj.tile_type == 'wall': break
            ent_obj = board.get_entity(tile[0], tile[1])
            if ent_obj != None: ent_obj.visible = True

    # make sure seer stays visible
    seer.visible = True
    

# shamelessly stolen from rogue basin
# https://www.roguebasin.com/index.php/Bresenham%27s_Line_Algorithm#Python
def bresenham_line(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # check line steepness, rotate accordingly
    is_steep = abs(dy) > abs(dx)
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # swap values if necessary
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # recalculate diff and calculate error
    dx = x2 - x1
    dy = y2 - y1
    error = dx // 2
    ystep = 1 if y1 < y2 else -1

    # iterate and add points in line
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # reverse if swapped earlier
    if swapped:
        points.reverse()
    return points

