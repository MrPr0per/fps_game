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
TEXT_STONE = 'TEXT_STONE'
TEXT_FIN = 'TEXT_FIN'
TEXT_SAUSAGE = 'TEXT_SAUSAGE'
textures = {
    TEXT_ILLUSION_1:    pygame.image.load('resourses/textures/illusion1.png').convert(),
    TEXT_1:             pygame.image.load('resourses/textures/texture1.png').convert(),
    TEXT_2:             pygame.image.load('resourses/textures/texture2.png').convert(),
    TEXT_MISSING:       pygame.image.load('resourses/textures/missing_textuere.png').convert(),
    TEXT_GRADIENT:      pygame.image.load('resourses/textures/gradient.png').convert(),
    TEXT_A:             pygame.image.load('resourses/textures/a.png').convert(),
    TEXT_KILL:          pygame.image.load('resourses/textures/kill256.png').convert(),
    TEXT_STONE:         pygame.image.load('resourses/textures/stone.png').convert(),
    TEXT_FIN:           pygame.image.load('resourses/textures/fin.png').convert(),
    TEXT_SAUSAGE:       pygame.image.load('resourses/textures/kolbasa4.png').convert(),
}

num_skys = 3
SKYS = [pygame.image.load(f'resourses/textures/sky{i}.png').convert() for i in range(1, num_skys + 1)]

# названия категорий
ENEMIES = 'ENEMIES'
PLAYER = 'PLAYER'
ITEMS = 'ITEMS'

# названия врагов
BASE_OBJECT = 'BASE_OBJECT'
TOFLUND = 'TOFLUND'
BAGGEBO = 'BAGGEBO'
# названия предметов
END_LVL_CRYSTAL = 'END_LVL_CRYSTAL'

# названия поз:
DEAD = 'DEAD'
DEFAULT = 'DEFAULT'
# названия анимаций
ROTATION = 'ROTATION'
ATTACK = 'ATTACK'
# разделы
FRAMES = 'FRAMES'
FRAME_DELAY = 'FRAME_DELAY'

objects_sprites = {
    BASE_OBJECT: pygame.image.load('resourses/objects/base_object.png').convert_alpha(),
    ENEMIES: {
        TOFLUND: {
            ROTATION: {
                FRAMES: [
                    pygame.image.load('resourses/objects/enemies/toflund/toflund_front.png').convert_alpha(),
                    pygame.image.load('resourses/objects/enemies/toflund/toflund_rear.png').convert_alpha(),
                ],
                FRAME_DELAY: 1000 / 2
            },
            ATTACK: {
                FRAMES: [
                    pygame.image.load(
                        f'resourses/objects/enemies/toflund/toflund_front.png').convert_alpha()
                ],
                FRAME_DELAY: 1000 / 5
            },
            DEAD: pygame.image.load('resourses/objects/enemies/toflund/toflund_dead.png').convert_alpha(),
        },
        BAGGEBO: {
            ROTATION: {
                FRAMES: [
                    pygame.image.load(f'resourses/objects/enemies/baggebo/rotation/baggebo{i}.png').convert_alpha() for i in range(1, 9)
                ],
                FRAME_DELAY: 1000 / 24
            },
            ATTACK: {
                FRAMES: [
                    pygame.image.load(f'resourses/objects/enemies/baggebo/attack/baggebo{i}.png').convert_alpha() for i in range(1, 10)
                ],
                FRAME_DELAY: 1000 / 15
            },
            DEAD: pygame.image.load(f'resourses/objects/enemies/baggebo/baggebo_dead.png').convert_alpha()
        },
    },
    PLAYER: {
        DEFAULT: pygame.image.load(f'resourses/objects/player/hand.png').convert_alpha(),
        ATTACK: {
            FRAMES: [
                pygame.image.load(f'resourses/objects/player/attack/hand{i}.png').convert_alpha() for i in range(3, 11)
            ],
            FRAME_DELAY: 1000 / 20
        },
    },
    ITEMS: {
        END_LVL_CRYSTAL: {
            DEFAULT: pygame.image.load('resourses/objects/items/end_lvl_crystal/base5.png').convert_alpha()
        }
    },
}


class Main_menu_sprites:
    background = pygame.image.load('resourses/menu/background2.png').convert()
    logo = pygame.image.load('resourses/menu/logo.png').convert_alpha()
    cursor = pygame.image.load('resourses/menu/cursor2.png').convert_alpha()