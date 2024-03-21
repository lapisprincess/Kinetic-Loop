""" game over screen for when the player dies """

### IMPORTS ###
import pygame as pg

from gui.button import Button
from gui.panel import Panel


### CONSTANTS ###
GAME_OVER_ART = pg.image.load("data/bones.png")


class GameOverMenu(Panel):
    def __init__(self, screen_dimensions: tuple[int, int], fonts: pg.font.Font):
        Panel.__init__(self, (0, 0), screen_dimensions, fonts)
        
        # initialize static pieces
        self.fill("#dddcc9")
        self.blit(GAME_OVER_ART, (0, screen_dimensions[1] - 240))

        render = self.fonts["h1"].render("You died!", None, (0, 0, 0))
        screenx, screeny = screen_dimensions[0], screen_dimensions[1]
        self.blit(render, (screenx * 3/5, screeny * 1/7))
        
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
            (300, 200),
            (100, 50),
            (255, 255, 255),
            exit,
            text= render
        )
        self.exit_button.draw(self)
        self.buttons.append(self.exit_button)