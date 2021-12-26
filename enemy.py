import pygame
from geometric_classes import Column
from resourses import *

objects_group = pygame.sprite.Group()


class Object(Column, pygame.sprite.Sprite):
    def __init__(self, x, y, h, h_down, image=objects_sprites[BASE_OBJECT]):
        Column.__init__(self, x, y, h, h_down)
        self.w = image.get_width() * h / image.get_height()
        pygame.sprite.Sprite.__init__(self, objects_group)
        self.image = image
        self.radius = self.w / 2 * COLLIDE_SCALE
        self.rect = pygame.Rect(x * COLLIDE_SCALE, y * COLLIDE_SCALE, ALMOST_ZERO * COLLIDE_SCALE, ALMOST_ZERO * COLLIDE_SCALE)


class Enemy(Object):
    def __init__(self, x, y, h, h_down):
        super().__init__(x=x, y=y, h=h, h_down=h_down)


class Toflund(Enemy):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, h=2, h_down=0)
        self.hp = 1
        self.damage = 10

        self.angle = 270
