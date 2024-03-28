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