import pygame
from settings import *

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

# textures
TEXT_ILLUSION_1 = 'TEXT_ILLUSION_1'
TEXT_1 = 'TEXT_1'
TEXT_2 = 'TEXT_2'
TEXT_MISSING = 'TEXT_MISSING'
TEXT_GRADIENT = 'TEXT_GRADIENT'
TEXT_A = 'TEXT_A'
TEXT_KILL = 'TEXT_KILL'
textures = {
    TEXT_ILLUSION_1:    pygame.image.load('resourses/textures/illusion1.png').convert(),
    TEXT_1:             pygame.image.load('resourses/textures/texture1.png').convert(),
    TEXT_2:             pygame.image.load('resourses/textures/texture2.png').convert(),
    TEXT_MISSING:       pygame.image.load('resourses/textures/missing_textuere.png').convert(),
    TEXT_GRADIENT:      pygame.image.load('resourses/textures/gradient.png').convert(),
    TEXT_A:             pygame.image.load('resourses/textures/a.png').convert(),
    TEXT_KILL:          pygame.image.load('resourses/textures/kill.png').convert(),
}

# objects
BASE_OBJECT = 'BASE_OBJECT'
ENEM_TOFLUND_FORWARD = 'TEXT_TOFLUND_FORWARD'

# названия категорий
ENEMIES = 'ENEMIES'
# названия врагов
TOFLUND = 'TOFLUND'
BAGGEBO = 'BAGGEBO'
# названия поз:
FRONT = 'FRONT'
REAR = 'REAR'
DEAD = 'DEAD'
# названия анимаций
ROTATION = 'ROTATION'
ATTACK = 'ATTACK'

objects_sprites = {
    BASE_OBJECT: pygame.image.load('resourses/objects/base_object.png').convert_alpha(),
    ENEMIES: {
        TOFLUND: {
            FRONT: pygame.image.load('resourses/objects/enemies/toflund/toflund_front.png').convert_alpha(),
            REAR: pygame.image.load('resourses/objects/enemies/toflund/toflund_rear.png').convert_alpha(),
            DEAD: pygame.image.load('resourses/objects/enemies/toflund/toflund_dead.png').convert_alpha(),
        },
        BAGGEBO: {
            ROTATION: [
                # возможно неправильная загрузка
                pygame.image.load(f'resourses/objects/enemies/baggebo/baggebo{i}.png').convert_alpha() for i in range(1, 9)
            ]
        }
    },
}