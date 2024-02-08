import pygame as pg

import util.direction as direction


# board gets mutated to fit los; seer stays constant
def fov_los(board, seer, pixel_max_dist):
    for tile in board.get_everything():
        tile.visible = False
    for tile in board.get_everything_within_range((seer.tile_x, seer.tile_y), 0.5):
        tile.visible = True
        if tile.visible == True: continue
        visible_tiles = _line(board, seer.rect.center, tile.rect.center)
        if visible_tiles == None: continue
        for line_tile in visible_tiles: line_tile.visible = True


# pixel_coord is a tuple defined as (x, y)
def _line(board, pixel_coord_source, pixel_coord_dest):
    source_distance_to_dest = direction.match_direction(pixel_coord_source, pixel_coord_dest)

    x_dist = board.pixel_distance_between_tiles(pixel_coord_source, (pixel_coord_source[0], pixel_coord_dest[1]))
    xrange = range(0, round(x_dist/board.tile_width))
    
    if x2 > x1: dx = x2 - x1
    else:       dx = x1 - x2
    if y2 > y1: dy = y2 - y1
    else:       dy = y1 - y2
    if dx == 0: slope = 1
    else:       slope = dy / dx

    for x in xrange:
        None



    '''
    out = set()
    x1, y1 = pixel_coord1[0], pixel_coord1[1]
    x2, y2 = pixel_coord2[0], pixel_coord2[1]
    tile_width = round(board.tile_width)
    if x2 > x1: dx, xrange = x2 - x1, range(x1, x2 + tile_width, tile_width)
    else      : dx, xrange = x1 - x2, range(x2, x1 + tile_width, tile_width)
    if y2 > y1: dy = y2 - y1
    else      : dy = y1 - y2
    if dx == 0: slope = 1
    else: slope = dy / dx
    intercept = y1 - slope * x1
    for x in xrange:
        y = slope * x + intercept
        tile_at_pixel = board.tile_at_pixel((x, y))
        entity_at_pixel = board.entity_at_pixel((x, y))
        if entity_at_pixel != None: 
            out.add(entity_at_pixel)
        if tile_at_pixel != None:
            out.add(tile_at_pixel)
            if tile_at_pixel.tile_type == 'wall': break
        else: break
    return out
    '''
