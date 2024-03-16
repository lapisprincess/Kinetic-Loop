import pygame as pg

from gui.panel import Panel

### POPOUT CLASS ###
class Popout(Panel):
    def __init__(self, pixel_coord, pixel_dimension):
        Panel.__init__(self, pixel_coord, pixel_dimension)
        self.set_border((180, 225, 180), alt=True)

    def update(self): None
