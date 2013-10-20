import pygame
import os
from Colour import *

# Sprite size: width = 48 / height = 64
# Todo: Add more comments
class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x = 0
    change_y = 0

    # Silent
    silent = False;

    # This is a frame counter used to determing which image to draw
    frame = 0

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]

        # Number of sprite + 1 = 13
        for i in range(1,13):
            img = pygame.image.load("sprites/player/player"+str(i)+".png").convert_alpha()
            img.set_colorkey(white)
            self.images.append(img)

        # By default, use image 0
        self.image = self.images[0]

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.silent = False

        self.footstepsound = pygame.mixer.Sound("sound/footstep.wav")

    def setSilent(self, var):
        if var == "Silent Cloth":
            self.silent = True
        else:
            self.silent = False

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y

    # Find a new position for the player
    def update(self,walls):
        # Get the old position, in case we need to go back to it
        old_x=self.rect.x
        new_x=old_x+self.change_x
        self.rect.x = new_x

        # Check the right and left border of the map
        if self.rect.x  < 0 or self.rect.x >= ((30*32)-42):
            self.rect.x = old_x

        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            # Hit a wall. Go back to the old position
            self.rect.x=old_x

        old_y=self.rect.y
        new_y=old_y+self.change_y
        self.rect.y = new_y

        # Check the up and bottom border of the map
        if self.rect.y  < -32 or self.rect.y >= ((14*32)-32):
            self.rect.y = old_y

        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            # Hit a wall. Go back to the old position
            self.rect.y=old_y

        # Display images of the player

        # Moving right to left
        if self.change_y < 0:
            self.frame += 1

            # We go from 0...3. If we are above image 3, reset to 0
            # Multiply by 4 because we flip the image every 4 frames
            if self.frame > 2*3:
                self.frame = 0
                if self.silent == False:
                    self.footstepsound.play()
            # Grab the image, do floor division by 4 because we flip
            # every 4 frames.
            # Frames 0...3 -> image[0]
            # Frames 4...7 -> image[1]
            # etc.
            self.image = self.images[self.frame//3]

        # Move left to right. About the same as before, but use
        # images 4...7 instead of 0...3. Note that we add 4 in the last
        # line to do this.
        if self.change_x > 0:
            self.frame += 1
            if self.frame > 2*3:
                self.frame = 0
                if self.silent == False:
                    self.footstepsound.play()
            self.image = self.images[self.frame//3+3]

        # Move bottom to top
        if self.change_y > 0:
            self.frame += 1
            if self.frame > 2*3:
                self.frame = 0
                if self.silent == False:
                    self.footstepsound.play()
            self.image = self.images[self.frame//3+3+3]

        if self.change_x < 0:
            self.frame += 1
            if self.frame > 2*3:
                self.frame = 0
                if self.silent == False:
                    self.footstepsound.play()
            self.image = self.images[self.frame//3+3+3+3]
