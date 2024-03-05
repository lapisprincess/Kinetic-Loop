import pygame as pg
import graphic as graphic

tile_width = 16

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

        curr_tile = graphic.Graphic((x,y), bgc=pg.color.Color(0,0,0))
        screen.blit(curr_tile, (0,0))
    
    pg.quit()
    exit(0)

tile_sampler((0, 0))
if len(sys.argv) >= 3: start_coord = (int(sys.argv[2]), int(sys.argv[3])) 
else: start_coord = (0, 0)
tile_sampler(start_coord)


'''
Watching Leland Palmer dance with a printout of Laura rn
and it's freaking the shit out of me :(
'''
