import pygame
import random
import sys
import os
import webbrowser
import time
import sqlite3 as lite

sys.path.append('./package')

from GraphicSprite import *
from Item import *
from Player import *
from Wall import *
from Bullet import *
from Ground import *
from Level import *
from Way import *
from array import *
from Colour import *
from UserInterface import *
from lib import ezmenu
from SqliteDB import *

"""

Komando Python : Infiltration
By le Sanglier des Ardennes

"""

class Config(object):
    menu = None
    menuloop = True
    watched = 0
    result = "no game played yet"
    mission = False

def gameQuit():
    Config.menuloop = False
    
def viewMission():
   # Call this function so the Pygame package can initialize itself
    pygame.init()
 
    # 48*25
    screen_width=1200
    # 64*12
    screen_height=640
    screen=pygame.display.set_mode([screen_width,screen_height])

    # Background image
    titleScreenImage = pygame.image.load("images/fs.jpg").convert()

    # Font
    font = pygame.font.Font(None, 36)

    pygame.display.set_caption('Komando Python : Infiltration')

    background = pygame.Surface(screen.get_size())

    background = background.convert()

    background.fill(black)

    # Title screen

    titleScreen=font.render("View Mission", True, blue)
    titleScreenRect = titleScreen.get_rect()
    screen.blit(titleScreenImage, [120,0])
    screen.blit(titleScreen, [130,10])

    pygame.display.update()

    # Wait for enter to be pressed
    # The user can also quit
    waiting = True
    while waiting:
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             sys.exit()
          elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RETURN:
                waiting = False
                break

def viewCommando():
    # Call this function so the Pygame package can initialize itself
    pygame.init()
 
    # Commando 1
    commando1x = 171
    commando1y = 135

    # Commando 2
    commando2x = 419
    commando2y = 145

    # Commando 3
    commando3x = 733
    commando3y = 96

    # Commando 4
    commando4x = 1010
    commando4y = 135

    # 48*25
    screen_width = 1200
    # 64*12
    screen_height = 640
    screen=pygame.display.set_mode([screen_width,screen_height])

    # Background image
    titleScreenImage = pygame.image.load("images/fs.jpg").convert()

    # Font
    font = pygame.font.Font(None, 36)

    pygame.display.set_caption('Komando Python : Infiltration')

    background = pygame.Surface(screen.get_size())

    background = background.convert()

    background.fill(black)

    # Title screen

    titleScreen=font.render("View Commando", True, blue)
    titleScreenRect = titleScreen.get_rect()
    screen.blit(titleScreenImage, [120,0])
    screen.blit(titleScreen, [130,10])

    pygame.display.update()

    # Wait for enter to be pressed
    # The user can also quit
    waiting = True
    while waiting:
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             sys.exit()
          elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RETURN:
                waiting = False
                break
          if pygame.mouse.get_pressed()[0] == True: 
            screen.blit(titleScreenImage, [120,0])
            screen.blit(titleScreen, [130,10])

            mousex = pygame.mouse.get_pos()[0] 
            mousey = pygame.mouse.get_pos()[1] 
            if mousex > commando1x-30 and mousex < commando1x+30 and mousey > commando1y-30 and mousey < commando1y+30 :
                commandoName1 = font.render("Commando #1", True, blue)
                commandoName1Rect = commandoName1.get_rect()
                screen.blit(commandoName1, [commando1x-25, commando1y+30])
                pygame.display.update()

            if mousex > commando2x-30 and mousex < commando2x+30 and mousey > commando2y-30 and mousey < commando2y+30 :
                commandoName2 = font.render("Commando #2", True, blue)
                commandoName2Rect = commandoName2.get_rect()
                screen.blit(commandoName2, [commando2x-25, commando2y+30])
                pygame.display.update()

            if mousex > commando3x-30 and mousex < commando3x+30 and mousey > commando3y-30 and mousey < commando3y+30 :
                commandoName3 = font.render("Commando #3", True, blue)
                commandoName3Rect = commandoName3.get_rect()
                screen.blit(commandoName3, [commando3x-25, commando3y+30])
                pygame.display.update()

            if mousex > commando4x-30 and mousex < commando4x+30 and mousey > commando4y-30 and mousey < commando4y+30 :
                commandoName4 = font.render("Commando #4", True, blue)
                commandoName4Rect = commandoName4.get_rect()
                screen.blit(commandoName4, [commando4x-100, commando4y+30])
                pygame.display.update()

def selectMission():

    # France-Paris
    FranceParisX = 608
    FranceParisY = 160

    # Call this function so the Pygame package can initialize itself
    pygame.init()
 
    # 48*25
    screen_width=1200
    # 64*12
    screen_height=640
    screen=pygame.display.set_mode([screen_width,screen_height])

    # Background image
    titleScreenImage = pygame.image.load("images/worldmap.png").convert()

    # Font
    font = pygame.font.Font(None, 36)

    pygame.display.set_caption('Komando Python : Infiltration')

    background = pygame.Surface(screen.get_size())

    background = background.convert()

    background.fill(black)

    # Title screen

    titleScreen=font.render("Mission Selection", True, blue)
    titleScreenRect = titleScreen.get_rect()
    screen.blit(titleScreenImage, [0,20])
    screen.blit(titleScreen, [20,20])

    pygame.display.update()

    # Wait for enter to be pressed
    # The user can also quit
    waiting = True
    while waiting:
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             sys.exit()
          elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RETURN:
                waiting = False
                break
          if pygame.mouse.get_pressed()[0] == True: 
            mousex = pygame.mouse.get_pos()[0] 
            mousey = pygame.mouse.get_pos()[1] 
            if mousex > FranceParisX-10 and mousex < FranceParisX+10 and mousey > FranceParisY-10 and mousey < FranceParisY+10 :
                missionName = font.render("France - Paris", True, blue)
                missionNameRect = missionName.get_rect()
                screen.blit(missionName, [mousex+10, mousey-10])
                pygame.display.update()
                time.sleep(2)
                waiting = False
                break

def gameUrl(url):
    print "KomandoPython.com"
    webbrowser.open_new_tab(url)

# Global variable declaration
mapIdGlobal = 217
playerPosxGlobal = 48
playerPosyGlobal = 32

def makeMenu(pos = 0):
    Config.menu = ezmenu.EzMenu(
        ["Go to the Mission", lambda: gotoMission(mapIdGlobal, playerPosxGlobal, playerPosyGlobal)],
        ["View Commando", viewCommando],
        ["Select Mission", selectMission],
        ["View Current Mission", viewMission],
        ["Visit Komado Python homepage", lambda: gameUrl("http://KomandoPython.com")],
        ["Quit Game", gameQuit] )
    
    Config.menu.center_at(320, 240)

    #Set the menu font (default is the pygame font)
    Config.menu.set_font(pygame.font.SysFont("Arial", 32))

    #Set the highlight color to green (default is red)
    Config.menu.set_highlight_color((255, 255, 0))

    #Set the normal color to white (default is black)
    Config.menu.set_normal_color((255, 255, 255))
    Config.menu.option = pos 

def gotoMission(mapId, playerPosx, playerPosy):

    # Global variables

    global mapIdGlobal
    global playerPosxGlobal
    global playerPosyGlobal


    Config.mission = True
   # Setup mixer to avoid sound lag
    pygame.mixer.pre_init(44100, -16, 2, 2048)

    # Call this function so the Pygame package can initialize itself
    pygame.init()


    # Sounds
    shootsound = pygame.mixer.Sound(os.path.join('sound','shoot.wav'))
    boomsound = pygame.mixer.Sound(os.path.join('sound','boom.wav'))

    # 48*25
    screen_width=1200
    # 64*12
    screen_height=640
    screen=pygame.display.set_mode([screen_width,screen_height])

    # Font
    font = pygame.font.Font(None, 36)

    pygame.display.set_caption('Komando Python : Infiltration')


    # Panel
    image_fnscar = pygame.image.load("images/panel/gun_fnscar.png").convert()
    bar_bottom = pygame.image.load("images/panel/bar_bottom.png").convert()
    bar_right = pygame.image.load("images/panel/bar_right.png").convert()


    # Sprites
    player = Player(playerPosx, playerPosy)
    movingsprites = pygame.sprite.RenderPlain()
    movingsprites.add(player)

    all_sprites_list = pygame.sprite.RenderPlain()

    wall_list = pygame.sprite.RenderPlain()

    item_list = pygame.sprite.RenderPlain()

    ground_list = pygame.sprite.RenderPlain()
     
    # List of each bullet
    bullet_list = pygame.sprite.RenderPlain()

    # Load level
    way_list = list()
    currentlevel = Level(mapId, way_list, ground_list, wall_list, all_sprites_list, item_list)

    clock = pygame.time.Clock()

    gameloop = False

    speed = 4

    score = 0

    ammunition = 20

    direction = 8

    newLevel = False

    debug = False

    halfWidthPlayer  = 24
    halfHeightPlayer = 32

    # Main game loop

    while gameloop == False:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameloop=True
                mapIdGlobal = mapId
                playerPosxGlobal = player.rect.x
                playerPosyGlobal = player.rect.y

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    gameloop = True
                    Config.mission = False;
                    mapIdGlobal = mapId
                    playerPosxGlobal = player.rect.x
                    playerPosyGlobal = player.rect.y

                # Music
                if event.key == pygame.K_m:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play()
                # Sound
                # Silent Cloth
                if event.key == pygame.K_s:
                    player.setSilent("Silent Cloth")


                if event.key == pygame.K_d:
                    print "Debug:"
                    for item in item_list:
                        print item

                # Change level
                if event.key == pygame.K_n:
                    print "Current player position: " + str(mapId) + " " + str(player.rect.x) + " " + str(player.rect.y)

                    # Left border
                    if player.rect.x <= -(halfWidthPlayer) and newLevel == False:
                        mapId = mapId - 1
                        currentlevel.empty(way_list, ground_list, wall_list, all_sprites_list, item_list)
                        nextlevel = Level(mapId, way_list, ground_list, wall_list, all_sprites_list, item_list)
                        player.rect.x = (32 * 30) - halfWidthPlayer
                        newLevel = True;
                        #print "Left: Move to: " + str(mapId) + " " + str(player.rect.x) + " " + str(player.rect.y)
                        
                    # Right Border
                    if player.rect.x >= (30 * 32) - halfWidthPlayer and newLevel == False:
                        mapId = mapId + 1
                        currentlevel.empty(way_list, ground_list, wall_list, all_sprites_list, item_list)
                        nextlevel = Level(mapId, way_list, ground_list, wall_list, all_sprites_list, item_list)
                        player.rect.x = -(halfWidthPlayer)
                        newLevel = True;
                        #print "Right: Move to: " + str(mapId) + " " + str(player.rect.x) + " " + str(player.rect.y)

                    # Top border
                    if player.rect.y <= -(halfHeightPlayer) and newLevel == False:
                        mapId = mapId - 21 
                        currentlevel.empty(way_list, ground_list, wall_list, all_sprites_list, item_list)
                        nextlevel = Level(mapId, way_list, ground_list, wall_list, all_sprites_list, item_list)
                        player.rect.y = (32*15) - halfHeightPlayer
                        newLevel = True;
                        #print "Top: Move to: " + str(mapId) + " " + str(player.rect.x) + " " + str(player.rect.y)

                    # Bottom Border
                    if player.rect.y >= (32*15) - halfHeightPlayer and newLevel == False:
                        mapId = mapId + 21
                        currentlevel.empty(way_list, ground_list, wall_list, all_sprites_list, item_list)
                        nextlevel = Level(mapId, way_list, ground_list, wall_list, all_sprites_list, item_list)
                        player.rect.y = -(halfHeightPlayer)
                        newLevel = True;
                        #print "Bottom: Move to: " + str(mapId) + " " + str(player.rect.x) + " " + str(player.rect.y)

                # Player movement
                if event.key == pygame.K_LEFT:
                    player.changespeed(-speed, 0)
                    direction = 4
                    newLevel = False
                if event.key == pygame.K_RIGHT:
                    player.changespeed(speed, 0)
                    direction = 6
                    newLevel = False
                if event.key == pygame.K_UP:
                    player.changespeed(0, -speed)
                    direction = 8
                    newLevel = False
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, speed)
                    direction = 2
                    newLevel = False
                if event.key == pygame.K_SPACE :
                    if ammunition > 0:
                        shootsound.play()
                        if direction == 8:
                            bullet = BulletVertical()
                            bullet.direction = 8
                            bullet.rect.x = player.rect.x + 24
                            bullet.rect.y = player.rect.y
                        if direction == 6:
                            bullet = BulletHorizontal()
                            bullet.direction = 6
                            bullet.rect.x = player.rect.x + 48
                            bullet.rect.y = player.rect.y + 32
                        if direction == 4:
                            bullet = BulletHorizontal()
                            bullet.direction = 4
                            bullet.rect.x = player.rect.x 
                            bullet.rect.y = player.rect.y + 32
                        if direction == 2:
                            bullet = BulletVertical()
                            bullet.direction = 2
                            bullet.rect.x = player.rect.x + 24
                            bullet.rect.y = player.rect.y + 64

                        all_sprites_list.add(bullet)
                        bullet_list.add(bullet)
                        ammunition -=1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(speed,0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-speed,0)
                if event.key == pygame.K_UP:
                    player.changespeed(0,speed)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0,-speed)

        player.update(all_sprites_list)

        # Calculate mechanics for each bullet
        for bullet in bullet_list:
            if bullet.name == "vertical" :
                if bullet.direction == 8:
                    bullet.rect.y -= 5
                if bullet.direction == 2:
                    bullet.rect.y += 5
            if bullet.name == "horizontal" :
                if bullet.direction == 6:
                    bullet.rect.x += 5
                if bullet.direction == 4:
                    bullet.rect.x -= 5

            # See if it hit a wall

            if pygame.sprite.spritecollide(bullet, wall_list, False):
                boomsound.play()
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

            # See if it hit a item
            item_hit_list = pygame.sprite.spritecollide(bullet, item_list, True)

            # For each item hit, remove the bullet and add to the score
            for item in item_hit_list:
                boomsound.play()
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1

            # Remove the bullet if it flies up off the screen
            if bullet.rect.x > (30*32) or bullet.rect.x < 0 or bullet.rect.y > (15*32) or bullet.rect.y < 0:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        screen.fill(black)

        ground_list.draw(screen)

        movingsprites.draw(screen)

        all_sprites_list.draw(screen)

        # Panel
        textScore=font.render("Score : "+str(score), True, blue)
        screen.blit(textScore, [0, 32*16])

        textAmmunition=font.render("Ammunition : "+str(ammunition), True, blue)
        screen.blit(textAmmunition, [0, 32*17])

        screen.blit(bar_bottom, [0,480])
        screen.blit(bar_right, [960,0])
        screen.blit(image_fnscar, [960,10])

        # Display
        pygame.display.flip()

        clock.tick(40)


#Main script
def main():

    # Komando Database
    komandodb = SqliteDB()

    komandodb.initializeDB("kommando")
    komandodb.insertMembers()
    #komandodb.listMembers()

    # Call this function so the Pygame package can initialize itself
    pygame.init()
 
    # 48*25
    screen_width=1200
    # 64*12
    screen_height=640
    screen=pygame.display.set_mode([screen_width,screen_height])

    # Background image
    titleScreenImage = pygame.image.load("images/fs.jpg").convert()

    # Font
    font = pygame.font.Font(None, 36)

    pygame.display.set_caption('Komando Python : Infiltration')

    background = pygame.Surface(screen.get_size())

    background = background.convert()

    background.fill(black)

    # Music
    pygame.mixer.music.load(os.path.join('music', 'an-turr.ogg'))

    # Title screen

    titleScreen=font.render("Komando Python : Infiltration", True, blue)
    titleScreenRect = titleScreen.get_rect()
    screen.blit(titleScreenImage, [120,0])
    screen.blit(titleScreen, [130,10])

    pygame.display.update()

    # play music non-stop
    #pygame.mixer.music.play(-1)

    # Wait for enter to be pressed
    # The user can also quit
    waiting = True
    while waiting:
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             sys.exit()
          elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RETURN:
                waiting = False
                break

    # Set codename
    codename = setCodename(screen, "Codename")

    # Make menu
    makeMenu(0)

    while Config.menuloop:
        events = pygame.event.get()

        #...and update the menu which needs access to those events
        Config.menu.update(events)

        #Let's quit when the Quit button is pressed
        for e in events:
            if e.type == pygame.QUIT:
                Config.menuloop = False
                
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                     Config.menuloop = False

        screen.blit(background, (0,0))
        Config.menu.draw(screen)
        pygame.display.flip()

    # End title screen

    titleScreen=font.render("Komando Python : Infiltration", True, blue)
    titleScreenRect = titleScreen.get_rect()
    screen.fill(black)
    screen.blit(titleScreenImage, [120,0])
    screen.blit(titleScreen, [130,10])

    pygame.display.update()

    # Wait for enter to be pressed
    # The user can also quit
    waiting = True
    while waiting:
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             waiting = False
             break
          elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RETURN:
                waiting = False
                break

    pygame.quit()

    return                

#Run the script if executed
if __name__ == "__main__":
    main()
