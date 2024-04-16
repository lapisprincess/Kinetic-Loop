""" display info about given object """

## IMPORTS
import pygame as pg

# from gui.button import Button
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
        size = self.fonts["h1"].size(name)
        self.blit(gameobj.info["image"], (200+size[0], 100+(size[1]/3)))

        height = 150
        for info_key in gameobj.info:
            if info_key in ("image", "name"):
                continue
            render = self.fonts["li"].render('-' + info_key + ": ", None, pg.Color(255, 255, 255))
            self.blit(render, (175, height))

            info_val = gameobj.info[info_key]
            if isinstance(info_val, int):
                render = self.fonts["li"].render(str(info_val), None, pg.Color(255, 255, 255))
                self.blit(render, (300, height))
                height += 30
                continue

            line = ""
            for word in info_val.split(' '):
                line += word + ' '
                size = self.fonts["li"].size(line)
                if size[0] + 300 > screen_dimensions[0]-200:
                    render = self.fonts["li"].render(line, None, pg.Color(255, 255, 255))
                    self.blit(render, (300, height))
                    line = ""
                    height += size[1]
            render = self.fonts["li"].render(line, None, pg.Color(255, 255, 255))
            self.blit(render, (300, height))
            height += 30
