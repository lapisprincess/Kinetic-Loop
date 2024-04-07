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


    def draw(self, surface, li_font, h1_font, level_name):
        Panel.draw(self, surface)

        render = h1_font.render(level_name, False, COLOR)
        coord = (
            self.mid.left, 
            self.mid.top + 10
        )
        surface.blit(render, coord)

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



    def _draw_info(self, info, surface, li_font, h1_font, half = False, is_player = False):
        if half: 
            mod = round(self.mid.height / 2)
            overhead = 0
        else: 
            mod = 0
            overhead = h1_font.size('')[1] + 10

        head = 10
        name = info["name"]
        xpos = self.mid.left + self.mid.width * 0.2
        while ' ' in name:
            if h1_font.size(name)[0] > self.mid.width-xpos:
                word = name[:name.index(' ')]
                name = name[name.index(' ') + 1:]
                text = h1_font.render(word, False, COLOR)
                coord = (
                    self.mid.left + self.mid.width * 0.2, 
                    overhead + self.mid.top + mod + head
                )
                surface.blit(text, coord)
                head += h1_font.size(name)[1]
        text = h1_font.render(name, False, COLOR)
        coord = (
            self.mid.left + self.mid.width * 0.2, 
            overhead + self.mid.top + mod + head
        )
        surface.blit(text, coord)
        
        image = info["image"]
        coord = (
            self.mid.left + self.mid.width * 0.05,
            overhead + self.mid.top + mod + 15
        )
        surface.blit(image, coord)

        # draw rest
        head += 30
        key = "HP:"
        val = str(info["hp"])
        key_render = li_font.render(key, False, COLOR)
        val_render = li_font.render(val, False, COLOR)
        key_coord = (
            self.mid.left + self.mid.width * 0.10,
            overhead + self.mid.top + mod + head
        )
        val_coord = (
            self.mid.left + self.mid.width * 0.70,
            overhead + self.mid.top + mod + head
        )
        surface.blit(key_render, key_coord)
        surface.blit(val_render, val_coord)
        if is_player:
            max_hp = "/" + str(info["max_hp"])
            coord = (
                self.mid.left + self.mid.width * 0.70 + 15,
                overhead + self.mid.top + mod + 50
            )
            surface.blit(max_hp, coord)


    def set_info(self, info):
        """ displays either one or two entities in the info panel """
        if len(info) == 0:
            self.info = (None, None)
        elif len(info) == 1:
            self.info = (info[0], None)
        else:
            self.info = (info[0], info[1])