import pygame
import random
import sys
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

"""
Komando Python : Infiltration

"""

# Call this function so the Pygame package can initialize itself
pygame.init()

# 48*25
screen_width=1200
# 64*12
screen_height=640
screen=pygame.display.set_mode([screen_width,screen_height])

way_list = list()

pygame.display.set_caption('Komando Python : Infiltration')

background = pygame.Surface(screen.get_size())

background = background.convert()

background.fill(black)

# Panel
image_fnscar = pygame.image.load("images/panel/gun_fnscar.png").convert()
bar_bottom = pygame.image.load("images/panel/bar_bottom.png").convert()
bar_right = pygame.image.load("images/panel/bar_right.png").convert()
titleScreenImage = pygame.image.load("images/fs.jpg").convert()

# Sprites
player = Player(48, 64)
movingsprites = pygame.sprite.RenderPlain()
movingsprites.add(player)

all_sprites_list = pygame.sprite.RenderPlain()

item_list = pygame.sprite.RenderPlain()

ground_list = pygame.sprite.RenderPlain()
 
# List of each bullet
bullet_list = pygame.sprite.RenderPlain()

# Load level
currentlevel = Level("01", way_list, ground_list, all_sprites_list, item_list)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

done = False

speed = 4

score = 0

ammunition = 20

direction = 8

newLevel = False

# Title screen

titleScreen=font.render("Komando Python : Infiltration", True, blue)
titleScreenRect = titleScreen.get_rect()
#titleScreenRect.centerx = screen.get_rect().centerx
#titleScreenRect.y = 150
screen.blit(titleScreenImage, [120,0])
#screen.blit(titleScreen, titleScreenRect)
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

# Main game loop

while done == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done=True

            if event.key == pygame.K_n:
                # Todo: Check the placement of the player on the map
                for way in way_list:
                    """
                    print "****"
                    print "from: " + str(way.fromx) + " " + str(way.fromy)
                    print "to: " + str(way.tox) + " " + str(way.toy)
                    print "level: " + way.level
                    print "player: " + str(player.rect.x) + " " + str(player.rect.y)
                    print "player: " + str((player.rect.x+24)/32) + " " + str((player.rect.y + 64)/32)
                    """
                    if ((player.rect.x+24)/32) == way.fromx and ((player.rect.y + 64)/32) == way.fromy:
                        newLevel = True;
                        break;

                if newLevel == True:
                        currentlevel.empty(way_list, ground_list, all_sprites_list, item_list)
                        nextlevel = Level(way.level, way_list, ground_list, all_sprites_list, item_list)
                        player.rect.x = way.tox  * 32
                        player.rect.y = (way.toy - 2) * 32
                        newLevel = False;

            if event.key == pygame.K_LEFT:
                player.changespeed(-speed,0)
                direction = 4
            if event.key == pygame.K_RIGHT:
                player.changespeed(speed,0)
                direction = 6
            if event.key == pygame.K_UP:
                player.changespeed(0,-speed)
                direction = 8
            if event.key == pygame.K_DOWN:
                player.changespeed(0,speed)
                direction = 2
            if event.key == pygame.K_SPACE :
                if ammunition > 0:
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

        # See if it hit a item
        item_hit_list = pygame.sprite.spritecollide(bullet, item_list, True)

        # For each item hit, remove the bollet and add to the score
        for item in item_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1

        # Remove the bullet if it flies up off the screen
        if bullet.rect.x > (29*32) or bullet.rect.x < (1*32) or bullet.rect.y > (15*32) or bullet.rect.y < (1*32):
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

pygame.quit()
