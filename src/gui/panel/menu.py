### IMPORTS ###
import pygame as pg

from gui.panel import Panel
import gui.button as button

from util.tuples import *

class Menu(Panel):
    def __init__(self, pixel_coord, pixel_dimen, board, gui):
        Panel.__init__(self, pixel_coord, pixel_dimen)

        # ROOM FOR EIGHT BUTTONS!!
        self.buttons = []
        button_dimen = divide_tuples(pixel_dimen, (4, 2))

        # look button
        look_coord = pixel_coord
        look_color = (255, 100, 100)
        self.look_button = button.Button(
            look_coord, button_dimen, look_color,
            button.toggle_looking, board
        )
        self.buttons.append(self.look_button)

        # test menu button
        test_coord = (pixel_coord[0] + button_dimen[0], pixel_coord[1])
        test_color = (100, 255, 100)
        self.test_button = button.Button(
            test_coord, button_dimen, test_color,
            button.test_panel, gui
        )
        self.buttons.append(self.test_button)



    def draw(self, surface):
        Panel.draw(self, surface)

        for button in self.buttons:
            button.draw(surface)

    def click(self):
        for button in self.buttons: 
            button.click()
