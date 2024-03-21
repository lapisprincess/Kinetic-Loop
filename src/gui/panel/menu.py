### IMPORTS ###
import pygame as pg

from gui.panel import Panel
import gui.button as button

from util.tuples import *

class MenuPanel(Panel):
    def __init__(self, pixel_coord, pixel_dimen, level, gui):
        Panel.__init__(self, pixel_coord, pixel_dimen)

        # ROOM FOR EIGHT BUTTONS!!
        self.buttons = []
        button_dimen = divide_tuples(pixel_dimen, (4, 2))

        # look button
        look_coord = pixel_coord
        look_color = (255, 100, 100)
        self.look_button = button.Button(
            look_coord, button_dimen, look_color,
            button.toggle_looking, level
        )
        self.buttons.append(self.look_button)



    def draw(self, surface):
        Panel.draw(self, surface)

        for button in self.buttons:
            button.draw(surface)

    def click(self):
        for button in self.buttons: 
            button.click()
