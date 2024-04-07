""" display info about given object """

## IMPORTS
import pygame as pg

from gui.button import Button
from gui.menu import Menu


class ObjectMenu(Menu):
    def __init__(
        self,
        gameobj,
        screen_dimensions: tuple[int, int],
        fonts: pg.font.Font,
        system,
    ):
        name = gameobj.info["name"]
        Menu.__init__(self, name, screen_dimensions, fonts, system)

        height = 150
        for info_key in gameobj.info:
            info_val = gameobj.info[info_key]
            render = self.fonts["li"].render('-', None, pg.Color(255, 255, 255))
            self.blit(render, (175, height))
            render = self.fonts["li"].render(info_key, None, pg.Color(255, 255, 255))
            self.blit(render, (200, height))
            render = self.fonts["li"].render(':' + str(info_val), None, pg.Color(255, 255, 255))
            self.blit(render, (300, height))
            height += 30