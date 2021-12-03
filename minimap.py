import pygame
from settings import *


class Minimap:
    def __init__(self):
        self.SCALE = 10
        self.LINE_SCALE = 10
        self.WIDTH = 200
        self.HEIGHT = 200
        self.CENTER_W = self.WIDTH / 2
        self.CENTER_H = self.HEIGHT / 2
        self.POS = (0, HEIGHT - self.HEIGHT)

        self.sc = pygame.Surface((self.WIDTH, self.HEIGHT))
