### IMPORTS ###
import pygame as pg

from gui.panel import Panel
from gui.popout import Popout
from board import Board

### BUTTON CLASS ###
class Button(Panel):
    def __init__(self, pixel_coord, pixel_dimen, color, function, target=None):
        Panel.__init__(self, pixel_coord, pixel_dimen)
        pg.draw.rect(self, color, (0, 0, pixel_dimen[0], pixel_dimen[1]))

        self.function = function
        self.target = target

    def click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.function(self.target)

    def draw(self, surface):
        surface.blit(self, (self.rect.left, self.rect.top))



### SMALL BUTTON FUNCTIONS ###
def toggle_looking(board):
    if type(board) == Board: 
        board.toggle_looking()

def test_panel(gui):
    popout_size = (gui.screen_size[0] - 60, gui.screen_size[1] - 60)
    sample_popout = Popout((30, 30), popout_size)
    gui.popout = sample_popout
