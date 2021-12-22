import pygame
import math

from settings import *
from player import Player
from drawing import Drawing
from control import control
from minimap import Minimap
import floors


pygame.init()
clock = pygame.time.Clock()

player = Player()
floor = floors.load_floor(10)
minimap = Minimap()
drawing = Drawing(clock, player, floor, minimap)

while True:

    control(player, clock, minimap, floor)

    drawing.clear_screen()
    drawing.draw_horizon()
    drawing.draw_raycast()
    drawing.draw_minimap()
    drawing.draw_fps()
    drawing.draw_info()

    player.update(clock.get_fps())

    pygame.display.update()
    clock.tick(FPS)


