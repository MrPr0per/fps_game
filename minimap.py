import pygame
from settings import *


class Minimap:
    def __init__(self):
        self.SCALE = MINIMAP_SCALE
        self.LINE_SCALE = self.SCALE
        self.WIDTH = WIDTH // 7
        self.HEIGHT = WIDTH // 7
        self.CENTER_W = self.WIDTH / 2
        self.CENTER_H = self.HEIGHT / 2
        self.POS = (WIDTH - self.WIDTH, HEIGHT - self.HEIGHT)

        self.sc = pygame.Surface((self.WIDTH, self.HEIGHT))
