### IMPORTS ###
import pygame as pg

from gui.panel import Panel
from gui.panel.board import Board
from gui.panel.log import Log
from gui.panel.info import Info
from gui.panel.menu import Menu

from gui.popout import Popout

from util.tuples import *


### CONSTANTS ###
# values represent percentages,
# to be compared to screen size
BOARD_COORD = (0, 0)
BOARD_DIMEN = (0.75, 0.75)

LOG_COORD = (0, 0.75)
LOG_DIMEN = (0.75, 0.25)

INFO_COORD = (0.75, 0)
INFO_DIMEN = (0.25, 0.75)

MENU_COORD = (0.75, 0.75)
MENU_DIMEN = (0.25, 0.25)


class GUI(pg.Surface):
    def __init__(self, screen_size, fonts, board):
        self.screen_size = screen_size
        self.li = fonts['li']
        self.h1 = fonts['h1']

        self.panels = []

        popout_size = (screen_size[0] - 60, screen_size[1] - 60)
        sample_popout = Popout((30, 30), popout_size)
        self.popout = None;


        # board panel
        board_coord = multiply_tuples(BOARD_COORD, screen_size)
        board_dimen = multiply_tuples(BOARD_DIMEN, screen_size)
        self.board = Board(board_coord, board_dimen, board)
        self.panels.append(self.board)

        # log panel
        log_coord = multiply_tuples(LOG_COORD, screen_size)
        log_dimen = multiply_tuples(LOG_DIMEN, screen_size)
        self.log = Log(log_coord, log_dimen, fonts)
        self.panels.append(self.log)

        # info panel
        info_coord = multiply_tuples(INFO_COORD, screen_size)
        info_dimen = multiply_tuples(INFO_DIMEN, screen_size)
        self.info = Info(info_coord, info_dimen)
        self.panels.append(self.info)

        # menu panel
        menu_coord = multiply_tuples(MENU_COORD, screen_size)
        menu_dimen = multiply_tuples(MENU_DIMEN, screen_size)
        self.menu = Menu(menu_coord, menu_dimen, board, self)
        self.panels.append(self.menu)

        # set borders where needed
        self.log.set_border(mid_color = (10, 50, 0))
        self.info.set_border(mid_color = (0, 80, 20))

    def draw(self, surface):
        self.board.draw(surface)
        self.log.draw(surface)
        self.info.draw(surface, self.li, self.h1)
        self.menu.draw(surface)
        if self.popout != None:
            self.popout.draw(surface)

    def add_messages(self, messages): 
        self.log.add_messages(self.li, messages)


    def update(self):
        for panel in self.panels:
            panel.update()

    def scroll(self, direction):
        mouse_pos = pg.mouse.get_pos()
        log_xrange = range(
            self.log.rect.left, 
            self.log.rect.left + self.log.rect.width
        )
        log_yrange = range(
            self.log.rect.top, 
            self.log.rect.top + self.log.rect.height
        )
        if mouse_pos[0] in log_xrange and mouse_pos[1] in log_yrange:
            match direction:
                case 'up': self.log.scroll_up()
                case 'down': self.log.scroll_down()

    # register mouseclick on buttons
    def click(self):
        mouse_pos = pg.mouse.get_pos()

        # buttons should only be located in the menu panel or in a popout
        for button in (self.menu.buttons): #+ self.popout.buttons):
            button_xrange = range(
                button.rect.left,
                button.rect.left + button.rect.width
            )
            cond1 = mouse_pos[0] in button_xrange
            button_yrange = range(
                button.rect.top,
                button.rect.top + button.rect.height
            )
            cond2 = mouse_pos[1] in button_yrange
            if cond1 and cond2: button.click()
