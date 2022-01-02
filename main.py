import pygame
import math
import time

from settings import *
from player import Player
from drawing import Drawing
from control import control
from minimap import Minimap
import floors


pygame.init()
clock = pygame.time.Clock()

player = Player()
floor = floors.load_floor(15)
minimap = Minimap()
drawing = Drawing(clock, player, floor, minimap)

#             тз:
#
# requirements.txt          .
# стартовое окно            .
# Финальное окно            .
# подсчет результатов       .
# спрайты                   OK
# collide                   OK
# анимация                  .
# 3+ уровней                .
# хранение данных           .

while True:

    control(player, clock, minimap, floor)

    drawing.clear_screen()
    drawing.draw_horizon()
    drawing.draw_world()
    drawing.draw_minimap()
    drawing.draw_fps()
    drawing.draw_info()

    player.update(clock.get_fps())

    pygame.display.update()
    clock.tick(FPS)


