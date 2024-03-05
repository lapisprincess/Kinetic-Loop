### IMPORTS ###
import pygame as pg

import util.graphic as graphic
import util.direction as directionality
from util.fov import fov_los

### CONSTANTS ###
UNARMED_DMG = 5
FOV_WIDTH = 6



### ENTITY CLASS ###
class Entity(pg.sprite.Sprite):
    def __init__(self, tile_coord, sheet_coord, bgc, fgc, board):
        self.tile_x, self.tile_y = tile_coord[0], tile_coord[1]

        self.inventory = []
        self.equipped = {
            "helmet" : None,
            "Armor" : None,
            "Weapon" : None,
        }
        self.target = None

        self.image = graphic.Graphic(sheet_coord, bgc, fgc)
        self.rect = self.image.get_rect()
        self.board = board

        self.visible = True
        self.seethrough = True
        self.traversable = False
        self.fov = fov_los(self.board, self, FOV_WIDTH * self.board.tile_width)

        self.info = {"HP": 0, "Name": "Sprout"}
        self.traits = set()

        pg.sprite.Sprite.__init__(self)
        
        #self.update()


    # every entity should adjust their rectangles accordingly
    def update(self): 
        self.rect.x = self.tile_x * graphic.tile_width
        self.rect.y = self.tile_y * graphic.tile_width

        self.fov = fov_los(self.board, self, FOV_WIDTH * self.board.tile_width)

        if self.info["HP"] <= 0: 
            self.board.log_message(self.get_info()["Name"] + " dies!!")
            self.kill()

    def take_turn(self):
        for trait in self.traits:
            if trait.priority != 1: continue
            if trait.act(self) == True: 
                return True
        for trait in self.traits:
            if trait.priority != 2: continue
            if trait.act(self) == True: 
                return True
        for trait in self.traits:
            if trait.priority != 3: continue
            if trait.act(self) == True: 
                return True
        return False


    # universal move method, usable by any entity to move one tile at a time
    # returns True if any action taken
    def move(self, direction, full=False):

        # get new coordinates
        mods = directionality.necessary_movement(direction)
        if mods == None: return False
        x, y = mods[0], mods[1]
        x_coord, y_coord = self.tile_x + x, self.tile_y + y

        # check if entity at new coords, auto-interact if so
        entity = self.board.get_entity(x_coord, y_coord)
        if entity != None and full == False:
            self.attack(entity)
            return False

        # see if anything is in the way
        things = self.board.get_anything(x_coord, y_coord)
        if things == None: return False
        for thing in things:
            if thing.traversable == False and not full: return False
        self.tile_x, self.tile_y = x_coord, y_coord
        return True


    # default info provider, filling in missing key info
    def get_info(self):
        if "Name" not in self.info:
            self.info["Name"] = "Leafling"
        if "Image" not in self.info:
            self.info["Image"] = self.image

        return self.info


    def damage(self, dmg):
        self.info["HP"] -= dmg

    def attack(self, target):
        if self.equipped["Weapon"] != None:
            None
        else:
            message = self.get_info()["Name"] 
            message += " attacked " + target.get_info()["Name"]
            message += " for " + str(UNARMED_DMG) + " damage!"
            self.board.log_message(message)
            target.damage(UNARMED_DMG)
            target.update()
