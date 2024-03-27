### IMPORTS ###
import pygame as pg

from gui.panel import Panel


### LOG CLASS ###
# log is where messages get logged,
# also used for text input and debugging
class LogPanel(Panel):

    def __init__(self, pixel_coord, pixel_dimension, fonts):
        Panel.__init__(self, pixel_coord, pixel_dimension, fonts)

        self.fonts = fonts
        self.typing = False
        self.type_txt = ""

        self.messages = []
        self.scroll = len(self.messages)


    def draw(self, surface):
        surface.blit(self, (self.rect.left, self.rect.top))

        # messages to draw, in the order they appear in bottom to top
        message1, message2, message3 = None, None, None
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

        if not self.typing:
            if message3 != None: surface.blit(message3, coord3)
            if message2 != None: surface.blit(message2, coord2)
            if message1 != None: surface.blit(message1, coord1)

        if self.typing:
            if message2 != None: surface.blit(message2, coord3)
            if message1 != None: surface.blit(message1, coord2)
            infont = self.fonts['li']
            intxt = infont.render(self.type_txt, False, (255, 255, 255))
            surface.blit(intxt, coord1)


    def add_message(self, message, font=None):
        if font == None: font = self.fonts['li']
        if type(message) == list:
            for message_text in message:
                message_text = "- " + message_text
                message = font.render(message_text, False, (255, 255, 255))
                self.messages.append(message)
                self.scroll = len(self.messages) - 1

        else:
            message_text = "- " + str(message)
            message = font.render(message_text, False, (255, 255, 255))
            self.messages.append(message)
            self.scroll = len(self.messages) - 1


    # simple scroll mutators with bounds
    def scroll_up(self):
        if self.scroll - 3 >= 0: self.scroll -= 1
    def scroll_down(self):
        if self.scroll < len(self.messages) - 1: self.scroll += 1


    # type text into the log like a console
    def type(self, event):

        # leave type mode
        exit_keys = [pg.K_ESCAPE, pg.K_RETURN]
        if event.key in exit_keys:
            self.typing = False

        # delete
        elif event.key == pg.K_BACKSPACE and len(self.type_txt) > 4:
            self.type_txt = self.type_txt[:-1]
        
        elif event.key == pg.K_BACKQUOTE: pass # ignore that char, thnx
        else: self.type_txt += event.unicode # add any other char
