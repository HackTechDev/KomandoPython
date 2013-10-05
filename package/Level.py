import pygame
from Ground import *
from Colour import * 
from Way import *
from Wall import *
from Item import *

class Level():
    # Constructor function
    def __init__(self, filename, way_list, ground_list, all_sprites_list, item_list):

        # Load level parameters
        file = open("maps/"+filename+"/level.txt", "r")
        line_list = file.readlines()
        file.close()


        for line in line_list:
            line = line[:-1]
            parameters = line.split("=")
            if parameters[0] == "way":
                ll = Way(parameters[1])
                way_list.append(ll)

        # Load background
        file = open("maps/"+filename+"/background.txt", "r")
        line_list = file.readlines()
        file.close()

        posx = 0 
        posy = 0
        for line in line_list:
            line = line[:-1]
            tiles = line.split(':')
            for tile in tiles:
                if tile == "01":
                    ground = Ground("brown_paving.png", posx, posy, 32, 32)
                    ground_list.add(ground)
                if tile == "02":
                    ground = Ground("floors_3.png", posx, posy, 32, 32)
                    ground_list.add(ground)
                posx = posx + 1
            posy = posy + 1
            posx = 0 
            
        # Load wall
        file = open("maps/"+filename+"/wall.txt", "r")
        line_list = file.readlines()
        file.close()

        posx = 0 
        posy = 0
        for line in line_list:
            line = line[:-1]
            tiles = line.split(':')
            for tile in tiles:
                if tile == "01":
                    wall = Wall("int_wall_bricks.png", posx, posy, 32, 32)
                    all_sprites_list.add(wall)
                posx = posx + 1
            posy = posy + 1
            posx = 0 
            
        # Load item
        file = open("maps/"+filename+"/item.txt", "r")
        line_list = file.readlines()
        file.close()

        posx = 0 
        posy = 0
        for line in line_list:
            line = line[:-1]
            tiles = line.split(':')
            for tile in tiles:
                if tile == "01":
                    item = Item("button.png", posx, posy, 32, 32)
                    item_list.add(item)
                    all_sprites_list.add(item)
                posx = posx + 1
            posy = posy + 1
            posx = 0 

    def empty(self, way_list, ground_list, all_sprites_list, item_list):

        del way_list[:]

        for sprite in all_sprites_list:
            all_sprites_list.remove(sprite)
       
        for item in item_list:
            item_list.remove(item)
    
        for ground in ground_list:
            ground_list.remove(ground)
