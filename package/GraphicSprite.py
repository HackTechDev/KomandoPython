import pygame
from Colour import *

class GraphicSprite(pygame.sprite.Sprite):

    def setGraphic(self,tilex,tiley,tilewidth,tileheight,x,y,width,height):
        myimage = pygame.image.load("sprites/wall/int_wall_bricks.png").convert()

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])

        for row in range(height//tileheight+1):
            for column in range(width//tilewidth+1):
                self.image.blit(myimage,(column*tilewidth,row*tileheight),(tilex,tiley,tilewidth,tileheight))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.image.set_colorkey(black)

    def setGraphic2(self,image, tilex,tiley,x,y,width,height):
        myimage = pygame.image.load(image).convert()

        self.image = pygame.Surface([width, height])

        self.image.blit(myimage,(0,0),(tilex,tiley,32,32))
        for column in range(width//32-2):
            self.image.blit(myimage,((column+1)*32,0),(tilex+32,tiley,32,32))
        self.image.blit(myimage,( (width//32-1)*32,0),(tilex+64,tiley,32,32))

        for row in range(height//32+1):
            self.image.blit(myimage,(0,(row+1)*32),(tilex,tiley+32,32,32))
            for column in range(width//32+1):
                self.image.blit(myimage,((column+1)*32,(row+1)*32),(tilex+32,tiley+32,32,32))
            self.image.blit(myimage,((width//32-1)*32,(row+1)*32),(tilex+64,tiley+32,32,32))

        self.image.blit(myimage,(0,(height//32-1)*32),(tilex,tiley+64,32,32))
        for column in range(width//32-2):
            self.image.blit(myimage,((column+1)*32,(height//32-1)*32),(tilex+32,tiley+64,32,32))
        self.image.blit(myimage,( (width//32-1)*32,(height//32-1)*32),(tilex+64,tiley+64,32,32))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.image.set_colorkey(black)
