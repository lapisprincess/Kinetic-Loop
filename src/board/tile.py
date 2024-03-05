### IMPORTS ###
import pygame as pg

import util.graphic as graphic


### GLOBALS ###
tile_types = ['floor', 'wall']
default_type = tile_types[0]


### TILE CLASS ###
class Tile(pg.sprite.Sprite):
    def __init__(
            self, tile_id,
            tile_coord, sheet_coord, 
            tile_type, bgc, fgc
        ):
        self.tile_x, self.tile_y = tile_coord[0], tile_coord[1]
        self.sheet_x, self.sheet_y = sheet_coord[0], sheet_coord[1]
        self.bgc, self.fgc = bgc, fgc

        if tile_type not in tile_types:
            print("illegal tile type used!")
            print("given: " + tile_type)
            print("defaulting to: " + default_type)
            tile_type = default_type
        else: self.tile_type = tile_type

        self.visible = True
        self.seethrough = True
        self.traversable = True
        if self.tile_type == 'wall': 
            self.seethrough = False
            self.traversable = False

        self.image = graphic.Graphic(sheet_coord, bgc, fgc)
        self.rect = self.image.get_rect()
        pg.sprite.Sprite.__init__(self)

        self.info = {
            "Name": tile_id,
            "Image": self.image,
        }

        # preliminary update for accuracy
        self.update()

    def update(self):
        self.rect.x = self.tile_x * graphic.tile_width
        self.rect.y = self.tile_y * graphic.tile_width


    def clone(self, tile_x=None, tile_y=None):
        if tile_x == None: tile_x = self.tile_x
        if tile_y == None: tile_y = self.tile_y
        return Tile(
            tile_id = self.info["Name"],
            tile_coord  = (tile_x, tile_y),
            sheet_coord = (self.sheet_x, self.sheet_y),
            tile_type   = self.tile_type,
            bgc = self.bgc, fgc = self.fgc
        )

    def pixel_collide(self, pixelx, pixely) -> bool:
        tile_x_range = range(self.rect.left, self.rect.left + self.rect.width)
        tile_y_range = range(self.rect.top, self.rect.top + self.rect.height)
        if (pixelx in tile_x_range) and (pixely in tile_y_range): return True
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
woodwall = Tile('Weirdwood bark', (0,0), (3, 1), 'wall', dark1, dark2)
grass = Tile('Shimmergrass', (0,0), (2, 2), 'floor', dark2, light1)



# old ones
grey       = pg.color.Color(100, 100, 100)
black      = pg.color.Color(0,   0,   0)
white      = pg.color.Color(255, 255, 255)
cobble_floor = Tile('Cobble floor', (0,0), (9, 15), 'floor', grey, black)
cobble_wall  = Tile('Cobble wall', (0,0), (0, 11), 'wall', grey, black)
