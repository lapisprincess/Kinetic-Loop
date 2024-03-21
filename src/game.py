""" overarching game system"""

## IMPORTS
import json
import random
import pygame as pg

from level import Level, connect_floors, level_gen
from tile import standard_tiles
from entity import Entity, player, trait

from util import pathfind as pf, define_controls
from util.debug import debug
from util.graphic import tile_width
from util.fov import fov_los

from gui import GUI
from gui.menu.mainmenu import MainMenu
from gui.menu.gameover import GameOverMenu


## CONSTANTS
SCREEN_DIMENSION = 1024, 512
PLAYER_BGC, PLAYER_FGC = pg.Color('green'), pg.Color('white')
DATA_PATH = "data/"
ENTITY_DATA_PATH = open("data/gameobjects/entity.json")
controls = define_controls(DATA_PATH)

class Game:
    def __init__(self, setFOV, stg=False):

        # determine if we're jumping straight into the game (stg)
        self.mode = "menu"
        if stg:
            self.mode = "game"

        # game utilities
        self.screen = pg.display.set_mode(SCREEN_DIMENSION)
        self.clock = pg.time.Clock()

        # fonts
        li_font = pg.font.Font("data/font.otf", size=14)
        h1_font = pg.font.Font("data/font.otf", size=20)
        self.all_fonts = { 'li': li_font, 'h1': h1_font, }

        # make main menu
        self.mainmenu = MainMenu(SCREEN_DIMENSION, self.all_fonts)
        self.gameovermenu = GameOverMenu(SCREEN_DIMENSION, self.all_fonts)
        self.menu = self.mainmenu

        # cursor stuffs
        cursor_img = pg.image.load("data/cursor.png")
        cursor_pressed_img = pg.image.load("data/cursor_pressed.png")
        self.cursor = pg.cursors.Cursor((0, 0), cursor_img)
        self.cursor_pressed = pg.cursors.Cursor((0, 0), cursor_pressed_img)
        pg.mouse.set_cursor(self.cursor)

        # jump straight into generating a level
        if self.mode == "game":
            self._setup_game(setFOV)

    def _setup_game(self, setFOV):
        """ detailed 8-level dungeon generator """

        # set up player
        player_colors = PLAYER_BGC, PLAYER_FGC
        self.player = player.Player((0,4), colors=player_colors)
        self.player.traits.add(trait.controllable)

        # set up full dungeon
        self.all_levels = []
        for i in range(1, 8):
            new_name = "level" + str(i)

            # loop until we generate a fully connected floor
            # takes a while... but these rooms need to be clean
            valid = False
            while not valid:
                new_level = Level(
                    tile_width, (500, 500),
                    controls, visibility=setFOV,
                    name=new_name
                )
                standard_tiles
                level_gen.generate_floor(new_level, 8, standard_tiles["grass"], standard_tiles["woodwall"])
                new_level.kill_orphans()
                valid = new_level.validate()
                if not valid:
                    continue
                valid &= len(new_level.get_all_rooms()) > 3 # at least 4 rooms

            self.all_levels.append(new_level)
            if i >= 2:
                connect_floors(self.all_levels[i-2], self.all_levels[i-1])

        self.current_level = 0
        self.all_levels[self.current_level].add_gameobj(self.player)
        self.player.fov = fov_los(self.all_levels[self.current_level], self.player)

        # gui initialization
        self.game_gui = GUI(SCREEN_DIMENSION, self.all_fonts, self.player.level)
        for level in self.all_levels: # link gui to levels
            level.log = self.game_gui.log

        # collect all entity data
        entity_templates = parse_entity_data(self.all_levels)

        # populate dungeon
        entities_so_far = []
        for i, level in enumerate(self.all_levels):
            entities_so_far += entity_templates[i]
            for room in level.get_all_rooms():
                if random.randint(0, 5) == 0:
                    continue # 1/5 chance the room is empty
                random_entity = entities_so_far[random.randint(0, len(entities_so_far)-1)]
                random_tile = room.get_random_floor()
                random_coord = random_tile.tile_x, random_tile.tile_y
                while level.get_game_object(random_coord[0], random_coord[1]) != None:
                    random_tile = room.get_random_floor()
                    random_coord = random_tile.tile_x, random_tile.tile_y
                level.add_gameobj(random_entity.clone(), random_coord)


    def loop(self):
        """ main game loop which runs everything """
        running = True
        while running:
            pg.display.flip()
            self.clock.tick(30)

            match self.mode:
                case "game": running = self.run_game()
                case "menu": running = self.run_menu()


    def run_menu(self): # TODO
        """ run the game menu """

        self.screen.fill("black")
        self.menu.update()
        self.menu.draw(self.screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            # manage mouse behavior
            if event.type == pg.MOUSEBUTTONDOWN:
                pg.mouse.set_cursor(self.cursor_pressed)

                # click on buttons
                self.menu.click_button()
            else: pg.mouse.set_cursor(self.cursor)

        return True


    def run_game(self):
        """ main game loop """
        if pg.key.get_pressed()[pg.K_ESCAPE] and self.game_gui.menu is not None:
            self.game_gui.menu = None

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
                    path = pf.pathfind(player_coord, new_loc, player_level)
                    self.player.travel_path = path

                # click on buttons
                self.game_gui.click_button()
                if self.game_gui.menu is None:
                    self.game_gui.menu.click()
            else: pg.mouse.set_cursor(self.cursor)

        self.screen.fill("black")
        #if self.game_gui.menu is None and not self.game_gui.log.typing:
        self.player.level.update(check_input)
        self.game_gui.update()
        #elif self.game_gui.menu is not None:
        #    self.game_gui.menu.update()

        if self.player.info["hp"] <= 0:
            self.mode = "menu"
            self.menu = self.gameovermenu
            self.game_gui.game_over = True

        self.game_gui.info.set_info(self.player.level.info)
        self.game_gui.draw(self.screen)

        return True

def parse_entity_data(all_levels):
    """ transform json data into entity templates """
    level_entities = [[]]

    # initialize output list
    for i in all_levels:
        level_entities.append([])

    entities_data = json.load(ENTITY_DATA_PATH)["entities"]
    for raw_entity_data in entities_data:

        # gather preliminary data
        entity_info = {}
        entity_info["name"] = raw_entity_data["name"]
        entity_info["description"] = raw_entity_data["description"]
        entity_info["hp"] = raw_entity_data["hp"]
        entity_sheet_coord = raw_entity_data["tile"]

        # create entity
        new_entity = Entity(
            sheet_coord =entity_sheet_coord,
            tile_coord =None,
            level =all_levels[raw_entity_data["level"]],
            info_intake =entity_info
        )

        # handle traits
        entity_traits = raw_entity_data["traits"]
        for entity_trait in entity_traits:
            new_trait = trait.all_traits[entity_trait]
            new_entity.traits.add(new_trait)

        # stow entity
        level_entities[raw_entity_data["level"]-1].append(new_entity)

    return level_entities