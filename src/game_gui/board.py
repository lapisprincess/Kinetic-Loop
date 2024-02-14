### IMPORTS ###
import pygame as pg

import game_gui.panel as panel

class BoardPanel(panel.Panel):
    def __init__(self, full_size, board):
        coord = panel.BOARD_COORD
        dimension = panel.BOARD_DIMENSION

        panel.Panel.__init__(self, full_size, coord, dimension)
        self.rect = board

        self.rect.middle = (
            coord[0] + (full_size[0] * panel.BOARD_DIMENSION[0]) / 2, 
            coord[1] + (full_size[1] * panel.BOARD_DIMENSION[1]) / 2 
        )

    def draw(self, surface):
        self.rect.draw(surface)
