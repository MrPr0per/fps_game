import pygame
import math
import time

from settings import *
from player import Player
from enemy import enemies_group
from drawing import Drawing
from control import control
from minimap import Minimap
import floors
from menu import main_menu

menu = main_menu

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('fps v0.1.0')

# game_cycle = GAME_CYCLES.MAIN_MENU
game_cycle = GAME_CYCLES.GAMEPLAY

current_level_number = 20

player = Player()
floor = floors.load_floor(current_level_number)
minimap = Minimap()
drawing = Drawing(clock, minimap, sc)

#   ▄              █▄     ▄█              ▄
#    ▀███▄       ▄█ ▄█   █▄ █▄       ▄███▀
#   ▄█    ▀ ▄  ▀██           ██▀  ▄ ▀    █▄
#  █▄    ▀▄  ▀█▄▄██▄  тз:  ▄██▄▄█▀  ▄▀    ▄█
#  ▄▀██▄█▀     ▀▀▀▀ ▀     ▀ ▀▀▀▀     ▀█▄██▀▄
#  ▀▄▄  ▄ requirements.txt         .  ▄  ▄▄▀
#    ▀██▀ стартовое окно           .  ▀██▀
#  ▄ █▀   Финальное окно           .    ▀█ ▄
#   █▄  ▄ подсчет результатов      .  ▄  ▄█
#    ▀██  спрайты                  OK  ██▀
#         collide                  OK
#    ▄ ▀  анимация                 OK  ▀ ▄
#  ▄█ ▄   3+ уровней               .    ▄ █▄
#  ▀█▄ ▀█ хранение данных          .  █▀ ▄█▀
#     ██    ▄  ▄▄▄  ▄     ▄  ▄▄▄  ▄    ██
#     ▀██  █ ▄██▀▀▀▄ █▄ ▄█ ▄▀▀▀██▄ █  ██▀
#     ▄▀██▄ █▀   ▀▄▀ ▄▀ ▀▄ ▀▄▀   ▀█ ▄██▀▄

while True:
    if game_cycle == GAME_CYCLES.MAIN_MENU:
        game_cycle, floor, player, menu = menu.check_interaction(floor, player, menu)

        drawing.clear_screen()
        menu.draw(sc)
        drawing.draw_fps()

    elif game_cycle == GAME_CYCLES.GAMEPLAY:
        game_cycle = control(player, clock, minimap, floor, game_cycle)

        drawing.clear_screen()
        drawing.draw_horizon(player)
        drawing.draw_world(player, floor)
        drawing.draw_player(player, floor)
        drawing.draw_minimap(player, floor)
        drawing.draw_fps()
        drawing.draw_interface(player)

        player.update(clock.get_fps())
        enemies_group.update(player, floor, clock.get_fps())

    pygame.display.update()
    clock.tick(FPS)
