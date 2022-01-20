from drawing import Drawing
from control import *
from minimap import Minimap
from menu import main_menu
from save import download_save

menu = main_menu

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('fps v1.0.0')

game_cycle = GAME_CYCLES.MAIN_MENU
# game_cycle = GAME_CYCLES.GAMEPLAY
# game_cycle = GAME_CYCLES.WIN

player = Player()
floor, current_level_number = download_save()
minimap = Minimap()
drawing = Drawing(clock, minimap, sc)

#   ▄              █▄     ▄█              ▄
#    ▀███▄       ▄█ ▄█   █▄ █▄       ▄███▀
#   ▄█    ▀ ▄  ▀██           ██▀  ▄ ▀    █▄
#  █▄    ▀▄  ▀█▄▄██▄  тз:  ▄██▄▄█▀  ▄▀    ▄█
#  ▄▀██▄█▀     ▀▀▀▀ ▀     ▀ ▀▀▀▀     ▀█▄██▀▄
#  ▀▄▄  ▄ requirements.txt         OK ▄  ▄▄▀
#    ▀██▀ стартовое окно           OK ▀██▀
#  ▄ █▀   Финальное окно           OK   ▀█ ▄
#   █▄  ▄ подсчет результатов      OK ▄  ▄█
#    ▀██  спрайты                  OK  ██▀
#         collide                  OK
#    ▄ ▀  анимация                 OK  ▀ ▄
#  ▄█ ▄   3+ уровней               OK   ▄ █▄
#  ▀█▄ ▀█ хранение данных          OK █▀ ▄█▀
#     ██    ▄  ▄▄▄  ▄     ▄  ▄▄▄  ▄    ██
#     ▀██  █ ▄██▀▀▀▄ █▄ ▄█ ▄▀▀▀██▄ █  ██▀
#     ▄▀██▄ █▀   ▀▄▀ ▄▀ ▀▄ ▀▄▀   ▀█ ▄██▀▄

start_lvl_time = None
finish_lvl_time = None
flicker_start_time = pygame.time.get_ticks()

while True:
    if game_cycle == GAME_CYCLES.MAIN_MENU:
        game_cycle, floor, player, menu, current_level_number = \
            menu.check_interaction(floor, player, menu, current_level_number)

        drawing.clear_screen()
        menu.draw(sc)
        drawing.draw_fps()

    elif game_cycle == GAME_CYCLES.GAMEPLAY:
        if start_lvl_time is None:
            start_lvl_time = pygame.time.get_ticks()

        game_cycle, floor, player, current_level_number, finish_lvl_time = \
            control(player, clock, minimap, floor, game_cycle, current_level_number, finish_lvl_time)

        control_mouce(player)

        drawing.clear_screen()
        drawing.draw_horizon(player, floor)
        drawing.draw_world(player, floor)
        drawing.draw_player(player, floor)
        drawing.draw_help(player, floor)
        drawing.draw_inventory(player, floor)
        drawing.draw_minimap(player, floor)
        drawing.draw_fps()
        drawing.draw_interface(player)

        floor, current_level_number, game_cycle, finish_lvl_time = \
            player.update_death(floor, current_level_number, game_cycle, finish_lvl_time)
        player.update(clock.get_fps())
        for obj in floor.object_list:
            if isinstance(obj, Enemy):
                obj.update(player, floor, clock.get_fps())

    elif game_cycle == GAME_CYCLES.WIN or game_cycle == GAME_CYCLES.DEATH:
        passage_time = finish_lvl_time - start_lvl_time
        flicker_start_time = drawing.draw_game_screen(game_cycle, flicker_start_time, passage_time)
        game_cycle, start_lvl_time = control_splash(game_cycle, start_lvl_time)

    pygame.display.update()
    clock.tick(FPS)

