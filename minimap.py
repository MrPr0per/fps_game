import pygame
from settings import *


class Minimap:
    def __init__(self):
        self.SCALE = 10
        self.LINE_SCALE = self.SCALE
        self.WIDTH = 250
        self.HEIGHT = 250
        self.CENTER_W = self.WIDTH / 2
        self.CENTER_H = self.HEIGHT / 2
        self.POS = (WIDTH - self.WIDTH, HEIGHT - self.HEIGHT)

        self.sc = pygame.Surface((self.WIDTH, self.HEIGHT))
