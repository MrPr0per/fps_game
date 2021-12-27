import pygame
from pygame.locals import *

pygame.init()
display = pygame.display.set_mode((320, 240))

background = pygame.image.load("leaves.png").convert_alpha()
mask = pygame.image.load("mask-fuzzy.png").convert_alpha()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # draw
    display.fill(Color(255, 0, 255))
    masked = background.copy()
    masked.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
    display.blit(masked, (0, 0))
    pygame.display.flip()