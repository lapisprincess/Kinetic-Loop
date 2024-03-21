""" panels help structure gui """

### IMPORTS ###
import pygame as pg


### CONSTANTS ###
MID_PRCNT = (0.75, 0.72)
BORDER = pg.image.load("data/leafy_border.png")
BORDER_ALT = pg.image.load("data/leafy_border_alt.png")


### PANEL CLASS ###
class Panel(pg.Surface):
    def __init__(self, pixel_coord, pixel_dimension, fonts=None):
        pg.Surface.__init__(self, pixel_dimension)
        self.rect = pg.Rect(pixel_coord, pixel_dimension)
        self.mid = None
        self.fonts=fonts

        self.buttons = []


    def set_border(self, mid_color=None, alt=False):
        """ add a border around the panel """
        self.mid = pg.Rect(
            self.rect.left, self.rect.top,
            self.rect.width * MID_PRCNT[0],
            self.rect.height * MID_PRCNT[1]
        )
        self.mid.center = self.rect.center

        new_scale = (self.rect.width, self.rect.height)
        if alt:
            scaled_border = pg.transform.scale(BORDER_ALT, new_scale)
        else:
            scaled_border = pg.transform.scale(BORDER, new_scale)

        if mid_color is not None:
            adjusted_rect = (0, 0, self.rect.width, self.rect.height)
            pg.draw.rect(self, mid_color, adjusted_rect)

        self.blit(scaled_border, (0, 0))


    def draw(self, surface):
        """ panel drawer """
        surface.blit(self, (self.rect.left, self.rect.top))
        for button in self.buttons:
            button.draw(surface)


    def click_button(self):
        """ click buttons on the panel """
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                button.click()



    def update(self):
        """ placeholder update method in case of idle panel """
        pass