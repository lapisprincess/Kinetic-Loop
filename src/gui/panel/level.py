### IMPORTS ###
import pygame as pg

from gui.panel import Panel

class LevelPanel(Panel):
    def __init__(self, pixel_coord, pixel_dimension, level):
        Panel.__init__(self, pixel_coord, pixel_dimension)
        self.rect = level

        self.rect.middle = (
            pixel_coord[0] + (pixel_dimension[0] / 2),
            pixel_coord[1] + (pixel_dimension[1] / 2)
        )

    def draw(self, surface):
        self.rect.draw(surface)
