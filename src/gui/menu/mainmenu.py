""" main menu screen """

## IMPORTS ###
import pygame as pg

from gui.button import Button
from gui import Panel


## CONSTANTS ###
TREE_IMG = pg.image.load("data/tree.jpg")

class MainMenu(Panel):
    def __init__(self, screen_dimensions: tuple[int, int], fonts: pg.font.Font, system):
        Panel.__init__(self, (0, 0), screen_dimensions, fonts)

        # initialize static pieces
        self.blit(TREE_IMG, (0, -80))

        text = "Leaflings"
        y = 40
        for char in text:
            rendered_char = self.fonts["h1"].render(char, None, pg.Color(255, 255, 255))
            self.blit(rendered_char, (100, y))
            y += self.fonts["h1"].size(char)[1] # increase y by text height

        # set up buttons
        render = self.fonts["li"].render("Play game", None, (0, 0, 0))
        play_game_button = Button(
            pixel_coord= (860, 100),
            pixel_dimen= (100, 50),
            color= (255, 255, 255),
            target= system,
            function= play_game,
            text= render,
        )
        play_game_button.draw(self)
        self.buttons.append(play_game_button)

        render = self.fonts["li"].render("Controls", None, (0, 0, 0))
        controls_button = Button(
            pixel_coord= (860, 200),
            pixel_dimen= (100, 50),
            color= (255, 255, 255),
            target= system,
            function= view_controls,
            text= render,
        )
        controls_button.draw(self)
        self.buttons.append(controls_button)

def view_controls(game_obj):
    game_obj.menu = game_obj.controlsmenu

### PLAY GAME BUTTON ###
loading_screen = pg.image.load("data/loading_screen.png")
def play_game(game_obj):

    # pull up loading screen
    game_obj.screen.fill("black")
    game_obj.screen.blit(loading_screen, (0, 0))
    pg.display.flip()
    game_obj.clock.tick(30)

    # start loading game
    game_obj.setup_game(True, True)
    game_obj.mode = "game"
