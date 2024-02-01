### IMPORTS ###
import pygame as pg

from entity import Entity


### CONSTANTS ###
# NOTE: movements that use multiple keys must come first to work!
PLAYER_MOVEMENTS = [
    'north-east', 'north-west', 'south-east', 'south-west',
    'north', 'south', 'west', 'east',
]


### PLAYER CLASS ###
'''

'''
class Player(Entity):
    def __init__(
        self,
        tile_coord,     # entity coord          : int
        sheet_coord,    # sprite loc in tileset : int
        bgc, fgc        # entity color          : pg.Color
    ):
        self.id = "player"
        Entity.__init__(self, tile_coord, sheet_coord, bgc, fgc)

    def process_input(self, controls, board):
        pressed_keys = pg.key.get_pressed()
        for move in PLAYER_MOVEMENTS:
            needed_controls = controls[move]
            check_controls = []
            for key in needed_controls:
                if pressed_keys[eval("pg." + key)]: check_controls.append(True)
                else: check_controls.append(False)
            if all(check_controls):
                self.move(move, board)
                return True
        return False
