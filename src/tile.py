""" Tile class """


### IMPORTS ###
import pygame as pg

from util import graphic
from gameobj import GameObj


### GLOBALS ###
tile_types = ['floor', 'wall']
default_type = tile_types[0]


### TILE CLASS ###
class Tile(GameObj):
    """ Todo! """
    def __init__(
            self, tile_id,
            tile_coord, sheet_coord,
            tile_type, colors
        ):

        GameObj.__init__(self, sheet_coord, tile_coord, colors)

        self.tile_x, self.tile_y = tile_coord[0], tile_coord[1]
        self.sheet_x, self.sheet_y = sheet_coord[0], sheet_coord[1]
        self.colors = colors

        if tile_type not in tile_types:
            print("illegal tile type used!")
            print("given: " + tile_type)
            print("defaulting to: " + default_type)
            tile_type = default_type
        else: self.tile_type = tile_type

        self.visible = True
        if self.tile_type == 'wall':
            self.seethrough = False
            self.traversable = False
        else:
            self.seethrough = True
            self.traversable = True

        self.info["Name"] = tile_id
        self.info["Image"] = self.image

        # preliminary update for accuracy
        self.update()

    def update(self):
        self.rect.x = self.tile_x * graphic.tile_width
        self.rect.y = self.tile_y * graphic.tile_width


    def clone(self, tile_x=None, tile_y=None):
        """ Clone current tile """
        if tile_x is None:
            tile_x = self.tile_x
        if tile_y is None:
            tile_y = self.tile_y
        return Tile(
            tile_id = self.info["Name"],
            tile_coord  = (tile_x, tile_y),
            sheet_coord = (self.sheet_x, self.sheet_y),
            tile_type   = self.tile_type,
            colors = (self.colors[0], self.colors[1])
        )

    def pixel_collide(self, pixelx, pixely) -> bool:
        """ OLD DON't USE! 
        use self.rect.collide_point instead!
        """
        if self.rect.collide_point(pixelx, pixely):
            return True
        return False

    def get_info(self):
        if "Name" not in self.info:
            self.info["Name"] = "Unknown Tile"
        if "Image" not in self.info:
            self.info["Image"] = self.image

        return self.info


### SAMPLE TILES ###
# colors
dark1 = pg.color.Color(80, 98, 58)
dark2 = pg.color.Color(41, 75, 41)
light1 = pg.color.Color(209, 241, 191)
light2 = pg.color.Color(120, 148, 97)

# tiles
woodwall = Tile('Weirdwood bark', (0,0), (3, 1), 'wall', (dark1, dark2))
grass = Tile('Shimmergrass', (0,0), (2, 2), 'floor', (dark2, light1))



# old ones
grey       = pg.color.Color(100, 100, 100)
black      = pg.color.Color(0,   0,   0)
white      = pg.color.Color(255, 255, 255)
cobble_floor = Tile('Cobble floor', (0,0), (9, 15), 'floor', (grey, black))
cobble_wall  = Tile('Cobble wall', (0,0), (0, 11), 'wall', (grey, black))

standard_tiles = {
    "cobble_floor": Tile('Cobble floor', (0,0), (9, 15), 'floor', (grey, black)),
    "cobble_wall": Tile('Cobble wall', (0,0), (0, 11), 'wall', (grey, black)),
    "woodwall": Tile('Weirdwood bark', (0,0), (3, 1), 'wall', (dark1, dark2)),
    "grass": Tile('Shimmergrass', (0,0), (2, 2), 'floor', (dark2, light1))
}