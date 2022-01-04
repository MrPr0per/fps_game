import pygame
from geometric_classes import Column
from resourses import *

objects_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()


class Object(Column, pygame.sprite.Sprite):
    def __init__(self, x, y, h, h_down, name=BASE_OBJECT):
        Column.__init__(self, x, y, h, h_down)
        self.name = name
        if name in objects_sprites[ENEMIES].keys():
            image = objects_sprites[ENEMIES][name][ROTATION][0]
        else:
            image = objects_sprites[BASE_OBJECT]
        self.w = image.get_width() * h / image.get_height()
        pygame.sprite.Sprite.__init__(self, objects_group)
        self.image = image
        self.radius = self.w / 2 * COLLIDE_SCALE
        self.true_radius = self.w / 2
        self.rect = pygame.Rect(x * COLLIDE_SCALE, y * COLLIDE_SCALE, ALMOST_ZERO * COLLIDE_SCALE,
                                ALMOST_ZERO * COLLIDE_SCALE)


class Enemy(Object):
    def __init__(self, x, y, h, h_down, angle, hp, damage, name):
        super().__init__(x=x, y=y, h=h, h_down=h_down, name=name)
        enemies_group.add(self)
        self.angle = angle
        self.hp = hp
        self.damage = damage

    def set_angle(self, angle):
        self.angle = angle

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            # при смерти:
            #   меняется спрайт                                       OK
            #   отключается ии                                        .
            #   отключается коллизия (чтобы не застревать  трупах)    .
            objects_group.remove(self)
            #   враг падает на землю                                  OK
            self.h_down = 0


class Toflund(Enemy):
    def __init__(self, x, y, angle):
        h = 3
        h_down = 0
        hp = 1
        damage = 10
        name = TOFLUND
        super().__init__(x=x, y=y, h=h, h_down=h_down, angle=angle, hp=hp, damage=damage, name=name)


class Baggebo(Enemy):
    def __init__(self, x, y, angle):
        h = 1.5
        h_down = 0
        hp = 1
        damage = 10
        name = BAGGEBO
        super().__init__(x=x, y=y, h=h, h_down=h_down, angle=angle, hp=hp, damage=damage, name=name)
