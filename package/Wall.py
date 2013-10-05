import pygame
import GraphicSprite

class Wall(GraphicSprite.GraphicSprite):
    def __init__(self,image, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        image = "sprites/wall/" + image
        tilex=32*1
        tiley=32*1
        x = x*32
        y = y*32
        self.setGraphic2(image, tilex,tiley,x,y,width,height)
