## IMPORTS ###
import pygame as pg

from gui.button import Button, back_to_game
from gui import Panel


## CONSTANTS ###
FIELD_IMG = pg.image.load("data/leafy_field.jpg")


class Menu(Panel):
    def __init__(
        self, 
        header: str,
        screen_dimensions: tuple[int, int], 
        fonts: pg.font.Font, 
        system, 
    ):
        Panel.__init__(self, (0, 0), screen_dimensions, fonts)

        # initialize static pieces
        self.blit(FIELD_IMG, (0, 0))

        self.rect_xpos = screen_dimensions[0] * 1/10
        self.rect_ypos = screen_dimensions[1] * 1/8
        self.rect_width = screen_dimensions[0] - self.rect_xpos*2
        self.rect_height = screen_dimensions[1] - self.rect_ypos*2
        rectangle = pg.Rect(
            self.rect_xpos, self.rect_ypos,
            self.rect_width, self.rect_height
        )
        pg.draw.rect(self, pg.Color(100, 150, 100), rectangle)

        render = self.fonts["h1"].render(header, None, pg.Color(255, 255, 255))
        self.blit(render, (150, 100))

        render = self.fonts["li"].render("Return to game", None, pg.Color(0, 0, 0))
        exit_button = Button(
            pixel_coord= (self.rect_width-49, self.rect_ypos), 
            pixel_dimen= (150, 50), 
            color= pg.Color(200, 255, 200), 
            target= system, 
            function= back_to_game, 
            text= render
        )
        exit_button.draw(self)
        self.buttons.append(exit_button)