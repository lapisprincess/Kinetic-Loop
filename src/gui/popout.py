import pygame as pg

from gui.panel import Panel

### POPOUT CLASS ###
class Popout(Panel):
    def __init__(self, pixel_coord, pixel_dimension):
        Panel.__init__(self, pixel_coord, pixel_dimension)
        self.set_border((10, 80, 30))

    def update(self): None
