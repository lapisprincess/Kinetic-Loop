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
class Player(Entity):
    def __init__(self, tile_coord, sheet_coord, bgc, fgc):
        self.id = "player"
        Entity.__init__(self, tile_coord, sheet_coord, bgc, fgc)

    # compares pressed keys to a list of viable controls,
    # then processes inputs.
    # for now, only accounts for movement
    def process_input(self, controls: dict[str, list[str]], board) -> bool:
        pressed_keys = pg.key.get_pressed()

        # cycle through all possible movements
        for move in PLAYER_MOVEMENTS:
            needed_controls = controls[move]
            check_controls = []

            # check if all key values are matched
            for key in needed_controls:
                if pressed_keys[eval("pg." + key)]: check_controls.append(True)
                else: check_controls.append(False)

            # if all keys that need to be pressed are pressed, success!
            if all(check_controls):
                self.move(move, board)
                return True

        # no control was made
        return False

    def update(self):
        Entity.update(self)
