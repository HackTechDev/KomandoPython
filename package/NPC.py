import pygame
import GraphicSprite

class NPC(GraphicSprite.GraphicSprite):

    image = ""
    tilex = 0
    tiley = 0
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, image, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = "sprites/NPC/" + image
        self.tilex = 32 * 0
        self.tiley = 64 * 0
        self.x = x * 32
        self.y = y * 32
        self.width = width
        self.height = height

        self.setGraphic2(self.image, self.tilex, self.tiley, self.x,self.y, self.width, self.height)
