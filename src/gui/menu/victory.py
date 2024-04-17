""" victory screen for when the player reaches the end """

### IMPORTS ###
import pygame as pg

from gui import Button
from gui import Panel


### CONSTANTS ###
VICTORY_ART = pg.image.load("data/victory.jpg")


class VictoryMenu(Panel):
    def __init__(self, screen_dimensions: tuple[int, int], fonts: pg.font.Font):
        Panel.__init__(self, (0, 0), screen_dimensions, fonts)

        self.fill("white")

        screenx, screeny = screen_dimensions[0]*3/5, screen_dimensions[1]*1/7
        self.blit(VICTORY_ART, (screenx-200, screeny))

        render = self.fonts["h1"].render("You won!", None, (0, 0, 0))
        self.blit(render, (screenx, screeny))
        render = self.fonts["li"].render("Enjoy your victory dates :)", None, (0, 0, 0))
        self.blit(render, (screenx, screeny+30))

        # final stats to be displayed (mutable)
        stats = {
            "level": 0,
            "most coolest posession": None
        }
        """
        stats to print:
        level
        most coolest posession
        """

        render = self.fonts["li"].render("Exit", None, (0, 0, 0))
        self.exit_button = Button(
            (screenx, 200),
            (100, 50),
            (200, 200, 200),
            exit,
            text= render
        )
        self.exit_button.draw(self)
        self.buttons.append(self.exit_button)
