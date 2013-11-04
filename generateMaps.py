#!/usr/bin/python
# -*- coding:utf-8 -*-  

import os
import math
import string
import Image

def generateMap(mapx, mapy, world):
    mapWidth = 30
    mapHeight = 15
    
    posX = 0
    posY = 0
    posZ = 0

    mapWorld = ""

    posYStart = ( ( 640 * mapHeight ) * mapy ) + (mapWidth * mapx)

    for y in range(0, mapHeight):
        posY = posYStart + (640 * y)   
        for x in range(0, mapWidth):
            posX = x
            posZ = posY + posX
        
            if world[posZ] == ".":
                mapWorld = mapWorld + "00:"
            else: 
                mapWorld = mapWorld + "01:";


    return mapWorld[:-1]


def saveMap(mapId, mapData):
    
    
    fp = open("./maps/" + str(mapId) + ".b.txt", "w+")
    dataList = mapData.split(":")
    count = 0
    mapTmp = ""

    for data in dataList:
        tile = "00"
        
        mapTmp = mapTmp + tile    
 
        if count == 29:
            mapTmp = mapTmp + "\n"
            count = 0
        else:
            mapTmp = mapTmp + ":"
            count = count + 1     
    fp.write(mapTmp)            


    fp = open("./maps/" + str(mapId) + ".w.txt", "w+")
    dataList = mapData.split(":")
    count = 0
    mapTmp = ""

    for data in dataList:
        
        mapTmp = mapTmp + data    
 
        if count == 29:
            mapTmp = mapTmp + "\n"
            count = 0
        else:
            mapTmp = mapTmp + ":"
            count = count + 1     
    fp.write(mapTmp)            

"""
 Tile size  = 
      width  : 32px 
      height : 32px

 Map image size =
      width  : 32 * 30 = 960
      height : 32 * 15 = 480
"""

def saveMapImage(mapId, mapData):
    tiles = mapData.split(":")

    imageTmp = Image.new("RGB", (960, 480))
    imageTmpMini = Image.new("RGB", (960 / 10, 480 / 10))

    r = 0
    c = 0
    
    imageTmpX = 0
    imageTmpY = 0

    for i in range(0, 15 * 30):
        if tiles[i] == "00":
            source = Image.open("./sprites/ground/floors_3.png")
        if tiles[i] == "01":
            source = Image.open("./sprites/wall/int_wall_bricks.png")

        if i % 30 == 0:
            imageTmpY = r * 32
            r = r + 1
            c = 0

        imageTmpX = c * 32
        c = c + 1
        
        imageTmp.paste(source, (imageTmpX, imageTmpY))

	mapImage = "./maps/" + str(mapId) + ".png"
    imageTmp.save(mapImage)

    mapImage = "./maps/" + str(mapId) + "_mini.png"
    imageTmp.thumbnail((960 / 10, 480 / 10), Image.ANTIALIAS)
    imageTmp.save(mapImage)

def main():

    # Initialize the world
    # 640 / 30 = (30 * 21) + 10
    # 480 / 15 = (15 * 32)

    world = []
    width  = 640
    height = 480

    world = [0 for i in range(width * height)]

    for h in range(0, height):
        for w in range(0, width):
            world[(h * width) + w] = "."

    file = open("world.raw", "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        pos = line.split(":")
        position = width * int(pos[2]) + int(pos[1])
        
        world[position] = "@"
        if pos[0] == "h":
            world[position + 1] = "@"
            world[position + 2] = "@"       
        if pos[0] == "v":
            world[position + width] = "@"
            world[position + width * 2] = "@"       
            world[position + width * 3] = "@"

    # Generate whole world

    # Height of world in map = 32 
    # Width of world in map = 21

    heightWorldTile = 32
    widthWorldTile = 21

    for y in range(0, heightWorldTile):
        for x in range(0, widthWorldTile):
            mapx = x
            mapy = y

            mapId = mapy * widthWorldTile + mapx
            mapData = generateMap(mapx, mapy, world)
            saveMap(mapId, mapData)
            saveMapImage(mapId, mapData)

if __name__ == "__main__":
    main()
