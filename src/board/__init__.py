### IMPORTS ###
import pygame as pg


### CONSTANTS ###
# 256-tile spritesheet
TILESET_PATH = "data/tiles.png"


### GLOBALS ###
# create a global tileset object
tileset = pg.image.load(TILESET_PATH)

# tile dimension calculated on fact that spritesheet has 256 tiles
# divide width by 16 for tile_width
tile_width = tileset.get_size()[0] / 16


### BOARD CLASS ###
'''

'''
class Board():
    def __init__(self):
        # initialize our two sprite groups
        self.tiles, self.entities = pg.sprite.Group(), pg.sprite.Group()

    def draw(self, surface):
        self.tiles.draw(surface)
        self.entities.draw(surface)

    def update(self):
        for entity in self.entities.sprites():
            entity.set_bgc(self.get_tile(entity.tile_x, entity.tile_y).bgc)

        for sprite in (self.tiles.sprites() + self.entities.sprites()):
            sprite.rect.x = sprite.tile_x * tile_width
            sprite.rect.y = sprite.tile_y * tile_width

        self.entities.update()
        self.tiles.update()

    def get_tile(self, tile_x, tile_y):
        for tile in self.tiles.sprites():
            if tile.tile_x == tile_x and tile.tile_y == tile_y:
                return tile


### GLOBAL HELPERS ###
'''
Method which returns tile from given coord
based on spritesheet provided in constant above.

@param sheet_x, sheet_y -> x,y coordinates (in tiles)           : int
@param fgc              -> color to make image                  : pg.Color
@return                 -> pg surface containing tile graphic   : pg.Surface
'''
def crop_image(sheet_x, sheet_y, fgc) -> pg.surface.Surface:
    # adjust tile coordinates to match spritesheet coordinates
    sheet_x, sheet_y = sheet_x * tile_width, sheet_y * tile_width

    # crop and adjust the tileset to get the right tile of proper color
    crop = (sheet_x, sheet_y, tile_width, tile_width)
    tile_pixArr = pg.PixelArray(tileset.subsurface(crop))
    tile_pixArr.replace(pg.color.Color("white"), fgc)

    # convert from pixel array to surface, return
    return tile_pixArr.make_surface()
