import pygame
import math

from settings import *
from player import Player
from drawing import Drawing
from control import control
from minimap import Minimap
import floor


pygame.init()
clock = pygame.time.Clock()

player = Player(x=0, y=0)
floor = floor.load_floor(5)
minimap = Minimap()
drawing = Drawing(clock, player, floor, minimap)

while True:

    control(player, clock, minimap, floor)

    drawing.clear_screen()
    drawing.draw_raycast()
    drawing.draw_minimap()
    drawing.draw_fps()

    pygame.display.update()
    clock.tick(FPS)


