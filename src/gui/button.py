### IMPORTS ###
import pygame as pg


### BUTTON CLASS ###
class Button(pg.Surface):

    def __init__(
        self, 
        pixel_coord :tuple[int, int],
        pixel_dimen :tuple[int, int],
        color :pg.Color,
        function,
        target =None,
        text :pg.Surface =None
    ):

        pg.Surface.__init__(self, pixel_dimen)

        # fill button
        pg.draw.rect(self, color, (0, 0, pixel_dimen[0], pixel_dimen[1]))

        # store dimension/coordinate
        self.rect = pg.Rect(pixel_coord, pixel_dimen)

        self.function = function
        self.target = target

        # check if text is too big for button
        if text is not None and (text.get_width() > pixel_dimen[0] or text.get_height() > pixel_dimen[1]):
            print("NOTE: text is too big for button!")
            text = None
        
        # find where exactly to put the text in the button
        if text is not None:
            textx = pixel_coord[0] + (pixel_dimen[0] - text.get_width()) / 2
            texty = pixel_coord[1] + (pixel_dimen[1] - text.get_height()) / 2
            self.text_coord = textx, texty

        self.text = text

    def click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.function(self.target)

    def draw(self, surface):
        surface.blit(self, (self.rect.left, self.rect.top))
        if self.text is not None:
            surface.blit(self.text, self.text_coord)



### SMALL BUTTON FUNCTIONS ###
def toggle_looking(level):
    if type(level) == level: 
        level.toggle_looking()

def test_panel(gui):
    pass
    #popout_size = (gui.screen_size[0] - 60, gui.screen_size[1] - 60)
    #sample_popout = Popout((30, 30), popout_size)
    #gui.popout = sample_popout