import pygame
from Colour import *

class BulletHorizontal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = "horizontal"
        self.direction = 0
        self.image = pygame.Surface([10, 4])
        self.image.fill(red)

        self.rect = self.image.get_rect()

class BulletVertical(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = "vertical"
        self.direction = 0
        self.image = pygame.Surface([4, 10])
        self.image.fill(red)

        self.rect = self.image.get_rect()

