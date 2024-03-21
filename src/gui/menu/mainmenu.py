""" main menu screen """

## IMPORTS
import pygame as pg

from gui import Panel

## CONSTANTS
TREE_IMG = pg.image.load("data/tree.jpg")

class MainMenu(Panel):
    def __init__(self, screen_dimensions: tuple[int, int], fonts: pg.font.Font):
        Panel.__init__(self, (0, 0), screen_dimensions, fonts)

        # initialize static pieces
        self.blit(TREE_IMG, (0, -80))

        text = "Leaflings"
        y = 40
        for char in text:
            rendered_char = self.fonts["h1"].render(char, None, pg.Color(255, 255, 255))
            self.blit(rendered_char, (100, y))
            y += self.fonts["h1"].size(char)[1] # increase y by text height