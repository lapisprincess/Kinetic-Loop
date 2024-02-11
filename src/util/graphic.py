### IMPORTS ###
import pygame as pg

import sys


### CONSTANTS ###
# 256-tile spritesheet
TILESET_PATH = "data/tiles.png"

## GLOBALS ##
# create a global tileset object
tileset = pg.image.load(TILESET_PATH)

# tile dimension calculated on fact that spritesheet has 256 tiles
# divide width by 16 for tile_width
tile_width = tileset.get_size()[0] / 16


### GRAPHIC CLASS ###
'''
The Graphic class is my tool for handling tile graphics 
for anything that needs an affiliated tile.

Instance variables:
    - self.tile
'''
class Graphic(pg.Surface):
    def __init__(self, sheet_coord, bgc=None, fgc=None): 
        # initialize blank surface
        pg.Surface.__init__(self, (tile_width, tile_width))

        # adjust tile coordinates to match spritesheet dimensions
        # then crop full tileset by taking specified subsurface
        sheet_x = sheet_coord[0] * tile_width
        sheet_y = sheet_coord[1] * tile_width
        crop = (sheet_x, sheet_y, tile_width, tile_width)
        self.tile = tileset.subsurface(crop)

        # if fgc specified, use PixelArray to alter color
        if fgc != None:
            tile_pixArr = pg.PixelArray(self.tile)
            tile_pixArr.replace(pg.color.Color("white"), fgc)
            self.tile = tile_pixArr.make_surface()

        # if bgc is specified, set it; then add the tile
        if bgc != None: self.fill(bgc)
        self.blit(self.tile, (0,0))

    def set_bgc(self, color):
        self.fill(color)
        self.blit(self.tile, (0,0))







### TILE SAMPLER FUNCTION ###
'''
This is a quick little program I whipped up which samples the tilesheet.
It uses arrow keys to navigate, and starts at a location specified
in the command prompt. The current tile location gets printed.
'''
def tile_sampler(start_coord):
    x, y = start_coord[0], start_coord[1]

    pg.init()
    screen = pg.display.set_mode((tile_width*2, tile_width*2))
    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: running = False
            if event.type == pg.KEYDOWN:
                key = pg.key.get_pressed()
                if key[pg.K_UP]: y -= 1
                elif key[pg.K_DOWN]: y += 1
                elif key[pg.K_LEFT]: x -= 1
                elif key[pg.K_RIGHT]: x += 1
                else: running = False
                x %= 16
                y %= 16
                print(x, y)


        pg.display.flip()
        clock.tick(60)

        curr_tile = Graphic((x,y), bgc=pg.color.Color(0,0,0))
        screen.blit(curr_tile, (0,0))
    
    pg.quit()
    exit(0)

if 'tile_sampler' in sys.argv:
    if len(sys.argv) >= 4: 
        start_coord = (int(sys.argv[2]), int(sys.argv[3])) 
    else: start_coord = (0,0)
    tile_sampler(start_coord)


'''
Watching Leland Palmer dance with a printout of Laura rn
and it's freaking the shit out of me :(
'''
