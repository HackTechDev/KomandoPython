import pygame
from Ground import *
from Colour import * 
from Way import *
from Wall import *
from Item import *
from NPC import *

class Level():
    # Constructor function
    def __init__(self, filename, way_list, ground_list, wall_list, all_sprites_list, item_list, npc_list):

        #print "*********"
        #print "* Level *"
        #print "*********"

        # Load ways
        #print "Load: ways"
        file = open("maps/default/1.w.txt", "r")
        line_list = file.readlines()
        file.close()


        for line in line_list:
            line = line[:-1]
            parameters = line.split("=")
            if parameters[0] == "way":
                ll = Way(parameters[1])
                way_list.append(ll)

        # Load background
        #print "Load: background"
        file = open("maps/" + str(filename) + ".b.txt", "r")
        line_list = file.readlines()
        file.close()

        posx = 0 
        posy = 0
        for line in line_list:
            line = line[:-1]
            tiles = line.split(':')
            for tile in tiles:
                if tile == "00":
                    ground = Ground("brown_paving.png", posx, posy, 32, 32)
                    ground_list.add(ground)
                if tile == "01":
                    ground = Ground("floors_3.png", posx, posy, 32, 32)
                    ground_list.add(ground)
                if tile == "02":
                    ground = Ground("floors_3.png", posx, posy, 32, 32)
                    ground_list.add(ground)
                posx = posx + 1
            posy = posy + 1
            posx = 0 
            
        # Load wall
        #print "Load: wall"
        file = open("maps/" + str(filename) + ".w.txt", "r")
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
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                posx = posx + 1
            posy = posy + 1
            posx = 0 
            
        # Load item
        #print "Load: item"
        try:
            file = open("maps/" + str(filename) + ".i.txt", "r")
        except IOError:
            file = open("maps/default/1.i.txt", "r")
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

        # Load NPC 
        #print "Load: npc"
        try:
            file = open("maps/" + str(filename) + ".npc.txt", "r")
        except IOError:
            file = open("maps/default/1.npc.txt", "r")
        line_list = file.readlines()
        file.close()
        

        posx = 0 
        posy = 0
        for line in line_list:
            line = line[:-1]
            tiles = line.split(':')
            for tile in tiles:
                if tile == "01":
                    #print "Add NPC: " + str(posx) + " " + str(posy)
                    npc = NPC("zombi.png", posx, posy, 48, 64)
                    npc_list.add(npc)
                    all_sprites_list.add(npc)
                posx = posx + 1
            posy = posy + 1
            posx = 0 



    def empty(self, way_list, ground_list, wall_list, all_sprites_list, item_list, npc_list):

        del way_list[:]

        for sprite in all_sprites_list:
            all_sprites_list.remove(sprite)
       
        for item in item_list:
            item_list.remove(item)
    
        for npc in npc_list:
            npc_list.remove(npc)

        for ground in ground_list:
            ground_list.remove(ground)

        for wall in wall_list:
            wall_list.remove(wall)
