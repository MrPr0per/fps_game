import pygame
import math
import time

import debug
from settings import *
from player import Player
from enemy import Enemy
from drawing import Drawing
from control import control
from minimap import Minimap
import floors
from menu import main_menu
from save import download_save

menu = main_menu

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('fps v0.1.0')

# game_cycle = GAME_CYCLES.MAIN_MENU
game_cycle = GAME_CYCLES.GAMEPLAY

player = Player()
# floor = floors.load_floor(current_level_number)
floor, current_level_number = download_save()
minimap = Minimap()
drawing = Drawing(clock, minimap, sc)

#   ▄              █▄     ▄█              ▄
#    ▀███▄       ▄█ ▄█   █▄ █▄       ▄███▀
#   ▄█    ▀ ▄  ▀██           ██▀  ▄ ▀    █▄
#  █▄    ▀▄  ▀█▄▄██▄  тз:  ▄██▄▄█▀  ▄▀    ▄█
#  ▄▀██▄█▀     ▀▀▀▀ ▀     ▀ ▀▀▀▀     ▀█▄██▀▄
#  ▀▄▄  ▄ requirements.txt         .  ▄  ▄▄▀
#    ▀██▀ стартовое окно           OK ▀██▀
#  ▄ █▀   Финальное окно           .    ▀█ ▄
#   █▄  ▄ подсчет результатов      .  ▄  ▄█
#    ▀██  спрайты                  OK  ██▀
#         collide                  OK
#    ▄ ▀  анимация                 OK  ▀ ▄
#  ▄█ ▄   3+ уровней               .    ▄ █▄
#  ▀█▄ ▀█ хранение данных          OK █▀ ▄█▀
#     ██    ▄  ▄▄▄  ▄     ▄  ▄▄▄  ▄    ██
#     ▀██  █ ▄██▀▀▀▄ █▄ ▄█ ▄▀▀▀██▄ █  ██▀
#     ▄▀██▄ █▀   ▀▄▀ ▄▀ ▀▄ ▀▄▀   ▀█ ▄██▀▄

while True:
    if game_cycle == GAME_CYCLES.MAIN_MENU:
        game_cycle, floor, player, menu, current_level_number = menu.check_interaction(floor, player, menu, current_level_number)

        drawing.clear_screen()
        menu.draw(sc)
        drawing.draw_fps()

    elif game_cycle == GAME_CYCLES.GAMEPLAY:
        game_cycle, floor, player, current_level_number = control(player, clock, minimap, floor, game_cycle, current_level_number)

        # аэээ не тройте этот кусок, если его выкинуть в control,
        # на некоторых компах не будет крутиться голова
        sensitivity = SENSITIVITY
        if pygame.mouse.get_focused():
            if VERTICAL_MOVE_HEAD:
                difference_w = pygame.mouse.get_pos()[0] - WIDTH / 2
                difference_h = pygame.mouse.get_pos()[1] - HEIGHT / 2
                pygame.mouse.set_pos([WIDTH / 2, HEIGHT / 2])
                player.turn(-difference_w * sensitivity, -difference_h * sensitivity)
            else:
                difference_w = pygame.mouse.get_pos()[0] - WIDTH / 2
                pygame.mouse.set_pos([WIDTH / 2, HEIGHT / 2])
                player.turn(-difference_w * sensitivity, 0)

        drawing.clear_screen()
        drawing.draw_horizon(player)
        drawing.draw_world(player, floor)
        drawing.draw_player(player, floor)
        drawing.draw_minimap(player, floor)
        drawing.draw_fps()
        drawing.draw_interface(player)

        player.update(clock.get_fps())
        for obj in floor.object_list:
            if isinstance(obj, Enemy):
                obj.update(player, floor, clock.get_fps())

    pygame.display.update()
    clock.tick(FPS)
