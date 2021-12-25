import pygame
from settings import *

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

# texture_names
TEXT_ILLUSION_1 = 'TEXT_ILLUSION_1'
TEXT_1 = 'TEXT_1'
TEXT_2 = 'TEXT_2'
TEXT_MISSING = 'TEXT_MISSING'
TEXT_GRADIENT = 'TEXT_GRADIENT'
TEXT_A = 'TEXT_A'

textures = {
    TEXT_ILLUSION_1:    pygame.image.load('textures/illusion1.png').convert(),
    TEXT_1:             pygame.image.load('textures/texture1.png').convert(),
    TEXT_2:             pygame.image.load('textures/texture2.png').convert(),
    TEXT_MISSING:       pygame.image.load('textures/missing_textuere.png').convert(),
    TEXT_GRADIENT:      pygame.image.load('textures/gradient.png').convert(),
    TEXT_A:             pygame.image.load('textures/a.png').convert(),
}