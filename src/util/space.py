def pixel_collide(
        pixel_coord: tuple[int, int], 
        pixel_area: tuple[int, int, int, int]) -> bool:
    coord_x, coord_y = pixel_coord[0], pixel_coord[1]
    area_top, area_left = pixel_area[0], pixel_area[1]
    area_width, area_height = pixel_area[2], pixel_area[3]
    x_range = range(area_left, area_left + area_width)
    y_range = range(area_top, area_top + area_height)
    if (coord_x in x_range) and (coord_y in y_range): return True
    else: return False
