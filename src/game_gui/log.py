### IMPORTS ###
import pygame as pg

import game_gui.panel as panel

class LogPanel(panel.Panel):
    def __init__(self, full_size: int):
        coord = panel.LOG_COORD
        dimension = panel.LOG_DIMENSION

        self.messages = []
        self.scroll = len(self.messages)

        panel.Panel.__init__(self, full_size, coord, dimension)

    def draw(self, surface):
        surface.blit(self, (self.rect.left, self.rect.top))

        message1, message2, message3 = None, None, None
        # messages to draw, in the order they appear in
        if len(self.messages) >= 1:
            message1 = self.messages[self.scroll]

        if len(self.messages) >= 3:
            message3 = self.messages[self.scroll - 2]
        if len(self.messages) >= 2:
            message2 = self.messages[self.scroll - 1]
        if len(self.messages) >= 1:
            message1 = self.messages[self.scroll]

        if self.mid != None:
            coord3 = (self.mid.left, self.mid.top)
            coord2 = (self.mid.left, self.mid.top + (self.mid.height*1/3))
            coord1 = (self.mid.left, self.mid.top + (self.mid.height*2/3))
        else: 
            coord3 = (self.rect.left, self.rect.top)
            coord2 = (self.rect.left, self.rect.top + (self.rect.height*1/3))
            coord1 = (self.rect.left, self.rect.top + (self.rect.height*2/3))

        if message3 != None: surface.blit(message3, coord3)
        if message2 != None: surface.blit(message2, coord2)
        if message1 != None: surface.blit(message1, coord1)


    def add_messages(self, font, messages):
        for message_text in messages:
            message_text = "- " + message_text
            message = font.render(message_text, False, (255, 255, 255))
            self.messages.append(message)
            self.scroll = len(self.messages) - 1

    def scroll_up(self):
        if self.scroll - 3 >= 0: self.scroll -= 1

    def scroll_down(self):
        if self.scroll < len(self.messages) - 1: self.scroll += 1
