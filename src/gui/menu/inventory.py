""" inventory screen to display player's items """

## IMPORTS ###
import pygame as pg

from gui.button import Button
from gui.menu import Menu
from entity.player import Player


class Inventory(Menu):
    def __init__(
        self, 
        screen_dimensions: tuple[int, int], 
        fonts: pg.font.Font, 
        system, 
    ):
        Menu.__init__(self, "Your stuff: ", screen_dimensions, fonts, system)
        self.system = system


    def update_items(self, player: Player):
        """ update the list of items displayed in inventory menu """

        height = 150
        rectangle = pg.Rect(
            self.rect_xpos, self.rect_ypos+70,
            self.rect_width, self.rect_height-70
        )
        pg.draw.rect(self, pg.Color(100, 150, 100), rectangle)
        for item in player.inventory:

            render = self.fonts["li"].render('-', None, pg.Color(255, 255, 255))
            self.blit(render, (175, height))
            render = self.fonts["li"].render(item.info["name"], None, pg.Color(255, 255, 255))
            self.blit(render, (200, height))

            if len(self.buttons) - 1 > len(player.inventory) * 3:
                continue

            render = self.fonts["li"].render("View", None, pg.Color(255, 255, 255))
            view_button = Button(
                pixel_coord= (400, height-15),
                pixel_dimen= (80, 40), 
                color= pg.Color(100, 100, 100), 
                target= self.system,
                function= item.view,
                text= render
            )
            view_button.draw(self)
            self.buttons.append(view_button)

            render = self.fonts["li"].render("Use", None, pg.Color(255, 255, 255))
            use_button = Button(
                pixel_coord= (500, height-15),
                pixel_dimen= (80, 40), 
                color= pg.Color(100, 100, 100), 
                target= player,
                function= item.use,
                text= render
            )
            use_button.draw(self)
            self.buttons.append(use_button)

            render = self.fonts["li"].render("Drop", None, pg.Color(255, 255, 255))
            drop_button = Button(
                pixel_coord= (600, height-15),
                pixel_dimen= (80, 40), 
                color= pg.Color(100, 100, 100), 
                target= player,
                function= item.drop,
                text= render
            )
            drop_button.draw(self)
            self.buttons.append(drop_button)

            height += 50

        while len(self.buttons) - 1 > len(player.inventory) * 3:
            self.buttons.pop()
