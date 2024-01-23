### IMPORTS ###
import pygame as pg

from board.entity import Entity

### CONSTANTS ###
# directory of controls file
CONTROLS = ""


### PLAYER CLASS ###
'''

'''
class Player(Entity):
    def __init__(
        self,
        sheet_coord,    # sprite loc in tileset : int
        bgc, fgc,       # entity color          : pg.Color
        tile_coord      # entity coord          : int
    ):
        self.id = "player"
        Entity.__init__(self, sheet_coord, bgc, fgc, tile_coord)

    def process_input(self, keys, board):
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            if keys[pg.K_UP]:
                self.move('north-east', board)
                return True
            if keys[pg.K_LEFT]:
                self.move('north-west', board)
                return True
            if keys[pg.K_RIGHT]:
                self.move('south-east', board)
                return True
            if keys[pg.K_DOWN]:
                self.move('south-west', board)
                return True
        else:
            if keys[pg.K_UP]:
                self.move('north', board)
                return True
            if keys[pg.K_DOWN]:
                self.move('south', board)
                return True
            if keys[pg.K_LEFT]:
                self.move('west', board)
                return True
            if keys[pg.K_RIGHT]:
                self.move('east', board)
                return True

        return False
