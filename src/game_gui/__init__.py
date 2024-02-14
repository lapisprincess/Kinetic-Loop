import pygame as pg

from game_gui.panel import Panel
from game_gui.board import BoardPanel
from game_gui.log import LogPanel
from game_gui.info import InfoPanel
from game_gui.menu import MenuPanel



class GUI(pg.Surface):
    def __init__(self, full_size, font, board):
        self.font = font

        # board panel
        self.board = BoardPanel(full_size, board)

        # log panel
        self.log = LogPanel(full_size)

        # info panel
        self.info = InfoPanel(full_size)

        # menu panel

    def draw(self, surface):
        self.board.draw(surface)
        self.log.draw(surface)
        self.info.draw(surface)


    def add_messages(self, messages): 
        self.log.add_messages(self.font, messages)


    def scroll(self, direction, mouse_pos):
        xrange = range(
            self.log.rect.left, 
            self.log.rect.left + self.log.rect.width
        )
        yrange = range(
            self.log.rect.top, 
            self.log.rect.top + self.log.rect.height
        )
        if mouse_pos[0] in xrange and mouse_pos[1] in yrange:
            match direction:
                case 'up': self.log.scroll_up()
                case 'down': self.log.scroll_down()
