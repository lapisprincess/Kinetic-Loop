### IMPORTS ###
# other people's stuff
import pygame as pg

# my stuff
import graphic


### GLOBALS ###
tile_types = ['floor', 'wall']


### TILE CLASS ###
'''
Tiles are sprites which can both be rendered and which
contain data which make up the structure of the map.

Instance variables:
    - tile_type         # type of tile (floor/wall)     : str
    - bgc               # background color for entities : pg.Color
    - tile_x, tile_y    # tile x/y coordinates          : int
    - image             # tile image                    : pg.Surface
    - rect              # tile coord/dimensions         : pg.Rect
'''
class Tile(pg.sprite.Sprite):
    def __init__(
        self,
        tile_type,          # type of tile          : str
        sheet_coord,        # sprite loc in tileset : int
        bgc, fgc,           # tile colors           : pg.Color
        tile_coord=(0,0)    # tile coord            : int
    ):
        # define instance variables
        self.tile_x,    self.tile_y     =   tile_coord[0],    tile_coord[1]
        self.sheet_x,   self.sheet_y    =   sheet_coord[0],   sheet_coord[1]
        self.bgc,       self.fgc        =   bgc,              fgc

        # ensure proper tile_type is used
        if tile_type not in tile_types: 
            print("illegal tile type used! " + tile_type)
            tile_type = 'floor'
        else: self.tile_type = tile_type

        self.image = graphic.Graphic(sheet_coord, bgc, fgc)

        # create rect and set at adjusted coordinates for render
        self.rect = self.image.get_rect()

        pg.sprite.Sprite.__init__(self)


    '''
    For now, updating the tile doesn't do anything.
    '''
    def update(self): None


    '''
    Create a duplicate of this tile at a given location.
    @param tile_x, tile_y   # where to place this clone : int
    '''
    def clone(self, tile_x, tile_y):
        return Tile(
            sheet_coord = (self.sheet_x, self.sheet_y), 
            tile_coord  = (tile_x, tile_y),
            tile_type   = self.tile_type, 
            bgc = self.bgc, fgc = self.fgc
        )


### SAMPLE TILES ###
# colors
lime_green  = pg.color.Color(50,  250, 50)
dark_green  = pg.color.Color(0,   150, 0)
grey        = pg.color.Color(100, 100, 100)
black       = pg.color.Color(0,   0,   0)
white       = pg.color.Color(255, 255, 255)
# tiles
grass           = Tile('floor', (12, 2), lime_green, dark_green)
hedge           = Tile('wall', (10, 2), dark_green, lime_green)
cobble_floor    = Tile('floor', (9, 15), grey, black)
cobble_wall     = Tile('wall', (0, 11), grey, black)
