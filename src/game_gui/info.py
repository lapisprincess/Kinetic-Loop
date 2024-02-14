### IMPORTS ###
import pygame as pg

import game_gui.panel as panel

class InfoPanel(panel.Panel):
    def __init__(self, full_size: int):
        coord = panel.INFO_COORD
        dimension = panel.INFO_DIMENSION

        panel.Panel.__init__(self, full_size, coord, dimension)

