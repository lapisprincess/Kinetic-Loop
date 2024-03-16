""" random spatial methods """
import math

def pixel_collide(
        pixel_coord: tuple[int, int],
        pixel_area: tuple[int, int, int, int]) -> bool:
    """ check if a point is contained within an area """
    coord_x, coord_y = pixel_coord[0], pixel_coord[1]
    area_top, area_left = pixel_area[0], pixel_area[1]
    area_width, area_height = pixel_area[2], pixel_area[3]
    x_range = range(area_left, area_left + area_width)
    y_range = range(area_top, area_top + area_height)
    return ((coord_x in x_range) and (coord_y in y_range))

def pixel_distance(coord1, coord2):
    """ calculate the distance given two coords """
    x1, y1 = coord1[0], coord1[1]
    x2, y2 = coord2[0], coord2[1]
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return math.sqrt(dx * dx + dy * dy)
