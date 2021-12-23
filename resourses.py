import pygame
from settings import *

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

textures = {
    ILLUSION_1: pygame.image.load('textures/illusion1.png').convert(),
}