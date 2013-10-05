import pygame
import GraphicSprite

class Item(GraphicSprite.GraphicSprite):
    def __init__(self, image, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        image = "sprites/item/" + image
        tilex=32*0
        tiley=32*0
        x = x*32
        y = y*32
        self.setGraphic2(image, tilex,tiley,x,y,width,height)
