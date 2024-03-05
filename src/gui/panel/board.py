### IMPORTS ###
import pygame as pg

from gui.panel import Panel

class Board(Panel):
    def __init__(self, pixel_coord, pixel_dimension, board):
        Panel.__init__(self, pixel_coord, pixel_dimension)
        self.rect = board

        self.rect.middle = (
            pixel_coord[0] + (pixel_dimension[0] / 2),
            pixel_coord[1] + (pixel_dimension[1] / 2)
        )

    def draw(self, surface):
        self.rect.draw(surface)
