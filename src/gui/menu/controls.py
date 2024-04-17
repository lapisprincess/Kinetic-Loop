""" victory screen for when the player reaches the end """

### IMPORTS ###
import pygame as pg

from gui import Button
from gui import Panel


### CONSTANTS ###
CONTROLS_ART = pg.image.load("data/controls.png")


class ControlsMenu(Panel):
    def __init__(self, screen_dimensions: tuple[int, int], fonts: pg.font.Font):
        Panel.__init__(self, (0, 0), screen_dimensions, fonts)

        self.blit(CONTROLS_ART, (0, 0))

        screenx, screeny = screen_dimensions[0], screen_dimensions[1]

        render = self.fonts["h1"].render("Move the player (@)", None, (0, 0, 0))
        text_coord = (screenx * 3/5, screeny * 1/12)
        self.blit(render, text_coord)
        line_coords = ((screenx * 1/2, text_coord[1]+10), (text_coord[0]-10, text_coord[1]+10))
        pg.draw.line(self, (0, 0, 0), line_coords[0], line_coords[1])

        render = self.fonts["h1"].render("Move the player (@) diagonally", None, (0, 0, 0))
        text_coord = (screenx * 3/5, screeny * 4/12)
        self.blit(render, text_coord)
        line_coords = ((screenx * 1/2, text_coord[1]+10), (text_coord[0]-10, text_coord[1]+10))
        pg.draw.line(self, (0, 0, 0), line_coords[0], line_coords[1])

        render = self.fonts["h1"].render("Examine the board", None, (0, 0, 0))
        text_coord = (screenx * 3/5, screeny * 6/12)
        self.blit(render, text_coord)
        line_coords = ((screenx * 1/2, text_coord[1]+10), (text_coord[0]-10, text_coord[1]+10))
        pg.draw.line(self, (0, 0, 0), line_coords[0], line_coords[1])

        render = self.fonts["h1"].render("View selected entity's info", None, (0, 0, 0))
        text_coord = (screenx * 3/5, screeny * 7/12)
        self.blit(render, text_coord)
        line_coords = ((screenx * 1/2, text_coord[1]+10), (text_coord[0]-10, text_coord[1]+10))
        pg.draw.line(self, (0, 0, 0), line_coords[0], line_coords[1])

        render = self.fonts["h1"].render("Open inventory", None, (0, 0, 0))
        text_coord = (screenx * 3/5, screeny * 8/12)
        self.blit(render, text_coord)
        line_coords = ((screenx * 1/2, text_coord[1]+10), (text_coord[0]-10, text_coord[1]+10))
        pg.draw.line(self, (0, 0, 0), line_coords[0], line_coords[1])

        render = self.fonts["h1"].render("Open player stats (not ready)", None, (0, 0, 0))
        text_coord = (screenx * 3/5, screeny * 9/12+10)
        self.blit(render, text_coord)
        line_coords = ((screenx * 1/2, text_coord[1]+10), (text_coord[0]-10, text_coord[1]+10))
        pg.draw.line(self, (0, 0, 0), line_coords[0], line_coords[1])

        render = self.fonts["h1"].render("Close a menu (such as this one!)", None, (0, 0, 0))
        text_coord = (screenx * 3/5, screeny * 12/14+10)
        self.blit(render, text_coord)
        line_coords = ((screenx * 1/2, text_coord[1]+10), (text_coord[0]-10, text_coord[1]+10))
        pg.draw.line(self, (0, 0, 0), line_coords[0], line_coords[1])
