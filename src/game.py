""" overarching game system"""

## IMPORTS
import pygame as pg

from level import Level, connect_floors, level_gen
from gui import GUI
from tile import standard_tiles
from entity import player, trait

from util import pathfind, define_controls
from util.debug import debug
from util.graphic import tile_width


## CONSTANTS
SCREEN_DIMENSION = 1024, 512
PLAYER_BGC, PLAYER_FGC = pg.Color('green'), pg.Color('white')
DATA_PATH = "data/"
controls = define_controls(DATA_PATH)


## TEST LEVEL
test_level = Level(
    tile_width, (500, 500),
    name="test_level"
)
cobble_floor, cobble_wall = standard_tiles["cobble_floor"], standard_tiles["cobble_wall"]
grass, woodwall = standard_tiles["grass"], standard_tiles["woodwall"]
room1 = test_level.build_room((0, 5), (5, 10), cobble_floor, cobble_wall)
room2 = test_level.build_room((15, 5), (10, 10), cobble_floor, cobble_wall)
room3 = test_level.build_room((0, 15), (5, 15), cobble_floor, cobble_wall)
test_level.connect_rooms(room2, room1)
test_level.connect_rooms(room3, room1)

class Game:
    def __init__(self, setFOV, play_test_level):

        # game utilities
        self.screen = pg.display.set_mode(SCREEN_DIMENSION)
        self.clock = pg.time.Clock()

        # set up player
        player_colors = PLAYER_BGC, PLAYER_FGC
        self.player = player.Player((0,4), colors=player_colors)
        self.player.traits.add(trait.controllable)

        # set up full dungeon
        self.all_levels = [test_level]
        for i in range(1, 9):
            new_name = "level" + str(i)
            new_level = Level(
                tile_width, (500, 500),
                controls, visibility=setFOV,
                name=new_name
            )
            level_gen.generate_floor(new_level, 8, grass, woodwall)
            self.all_levels.append(new_level)
            if i >= 2:
                connect_floors(self.all_levels[i-1], self.all_levels[i])
        self.current_level = 1
        self.all_levels[self.current_level].add_gameobj(self.player)

        if play_test_level:
            self.current_level = 0

        # fonts
        li_font = pg.font.Font("data/font.otf", size=14)
        h1_font = pg.font.Font("data/font.otf", size=20)
        all_fonts = { 'li': li_font, 'h1': h1_font, }

        # gui initialization
        self.game_gui = GUI(SCREEN_DIMENSION, all_fonts, self.player.level)
        for level in self.all_levels: # link gui to levels
            level.log = self.game_gui.log

        # cursor stuffs
        cursor_img = pg.image.load("data/cursor.png")
        cursor_pressed_img = pg.image.load("data/cursor_pressed.png")
        self.cursor = pg.cursors.Cursor((0, 0), cursor_img)
        self.cursor_pressed = pg.cursors.Cursor((0, 0), cursor_pressed_img)
        pg.mouse.set_cursor(self.cursor)

        # general game variables
        self.mode = "game"


    def loop(self):
        running = True
        while running:
            match self.mode:
                case "game": running = self.run_game()
                case "menu": running = self.run_menu()


    def run_menu(self):
        pass


    def run_game(self):
        if pg.key.get_pressed()[pg.K_ESCAPE] and self.game_gui.popout is not None:
            self.game_gui.popout = None

        pg.display.flip()
        self.clock.tick(30)

        self.game_gui.change_level(self.player.level)

        check_input = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            # process keystrokes
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKQUOTE and not self.game_gui.log.typing:
                    self.game_gui.log.type_txt = "db> "
                    self.game_gui.log.typing = True
                if event.key == pg.K_RETURN and self.game_gui.log.typing:
                    debug(self.player, self.game_gui.log, self.all_levels)
                if self.game_gui.log.typing:
                    self.game_gui.log.type(event)
                check_input = True

            # register scrolling
            if event.type == pg.MOUSEWHEEL:
                if event.y >= 0:
                    direction = 'up'
                else:
                    direction = 'down'
                self.game_gui.scroll(direction)

            # manage mouse behavior
            if event.type == pg.MOUSEBUTTONDOWN:
                pg.mouse.set_cursor(self.cursor_pressed)

                # move player on mouseclick
                new_loc = self.game_gui.click_move()
                if new_loc is not None:
                    player_coord = (self.player.tile_x, self.player.tile_y)
                    player_level = self.player.level
                    path = pathfind(player_coord, new_loc, player_level)
                    self.player.travel_path = path

                # click on buttons
                self.game_gui.click_button()
                if self.game_gui.popout is None:
                    self.game_gui.menu.click()
            else: pg.mouse.set_cursor(self.cursor)

        self.screen.fill("black")
        if self.game_gui.popout is None and not self.game_gui.log.typing:
            self.player.level.update(check_input)
            self.game_gui.update()
        elif self.game_gui.popout is not None:
            self.game_gui.popout.update()

        if self.player.info["HP"] <= 0:
            self.game_gui.game_over = True

        self.game_gui.info.set_info(self.player.level.info)
        self.game_gui.draw(self.screen)

        return True