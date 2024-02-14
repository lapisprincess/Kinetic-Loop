### IMPORTS ###
import pygame as pg


### CONSTANTS ###
# dimensions, demarking percentage of screen taken up
BOARD_COORD = (0, 0)
BOARD_DIMENSION = (0.75, 0.75)

LOG_COORD = (0, 0.75)
LOG_DIMENSION = (0.75, 0.25)

INFO_COORD = (0.75, 0)
INFO_DIMENSION = (0.25, 0.75)

MENU_COORD = (0.75, 0.75)
MENU_DIMENSION = (0.25, 0.25)


### PANEL CLASS ###
class Panel(pg.Surface):
    def __init__(self, full_size, coord_mod, dimension_mod):
        pixel_coord = (
            coord_mod[0] * full_size[0], 
            coord_mod[1] * full_size[1]
        )
        pixel_dimension = (
            dimension_mod[0] * full_size[0], 
            dimension_mod[1] * full_size[1]
        )

        self.mid = None
        self.rect = pg.Rect(pixel_coord, pixel_dimension)
        pg.Surface.__init__(self, pixel_dimension)


    # set an image to wrap around the border
    def set_border(self, image, mid_prcnt = (1, 1), mid_color = None):
        self.mid = pg.Rect(
            self.rect.left, self.rect.top, 
            self.rect.width * mid_prcnt[0], 
            self.rect.height * mid_prcnt[1]
        )
        self.mid.center = self.rect.center

        new_scale = (self.rect.width, self.rect.height)
        scaled_image = pg.transform.scale(image, new_scale)

        if mid_color != None:
            adjusted_rect = (0, 0, self.rect.width, self.rect.height)
            pg.draw.rect(self, mid_color, adjusted_rect)

        self.blit(scaled_image, (0, 0))


    def draw(self, surface):
        surface.blit(self, (self.rect.left, self.rect.top))
