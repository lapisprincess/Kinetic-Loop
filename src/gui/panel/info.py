### IMPORTS ###
import pygame as pg

from gui.panel import Panel


### CONSTANTS ###
COLOR = (255, 255, 255)


### INFO PANEL CLASS ###
class InfoPanel(Panel):
    def __init__(self, pixel_coord, pixel_dimension):
        Panel.__init__(self, pixel_coord, pixel_dimension)

        self.info = (None, None)


    def draw(self, surface, li_font, h1_font):
        Panel.draw(self, surface)

        if self.info[0] != None:
            self._draw_info(self.info[0], surface, li_font, h1_font)
        if self.info[1] != None:
            pg.draw.line(
                surface, COLOR,
                (self.mid.left, self.mid.top + (self.mid.height / 2)),
                (
                    self.mid.left + self.mid.width, 
                    self.mid.top + (self.mid.height / 2)
                )
            )
            self._draw_info(self.info[1], surface, li_font, h1_font, True)



    def _draw_info(self, info, surface, li_font, h1_font, half = False):
        if half: mod = round(self.mid.height / 2)
        else: mod = 0
        
        # first image
        image = info["image"]
        coord = (
            self.mid.left + self.mid.width * 0.05,
            self.mid.top + mod + 15
        )
        surface.blit(image, coord)

        # second image
        name = info["name"]
        text = h1_font.render(name, False, COLOR)
        coord = (
            self.mid.left + self.mid.width * 0.2, 
            self.mid.top + mod + 10
        )
        surface.blit(text, coord)

        # draw rest
        depth = 50
        for key in info:
            if key == "image": continue
            elif key == "name": continue
            val = str(info[key])
            key += ':'
            key_render = li_font.render(key, False, COLOR)
            val_render = li_font.render(val, False, COLOR)
            key_coord = (
                self.mid.left + self.mid.width * 0.10,
                self.mid.top + mod + depth
            )
            val_coord = (
                self.mid.left + self.mid.width * 0.70,
                self.mid.top + mod + depth
            )
            surface.blit(key_render, key_coord)
            surface.blit(val_render, val_coord)
            depth += 20


    def set_info(self, info):
        if len(info) == 0:
            self.info = (None, None)
        elif len(info) == 1:
            self.info = (info[0], None)
        else:
            self.info = (info[0], info[1])
