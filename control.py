import pygame
import debug
from settings import *
import save
from player import Player
from enemy import *
from geometry import *


def control_mouce(player):
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


def control(player, clock, minimap, floor, game_cycle, current_level_number, finish_lvl_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_cycle = GAME_CYCLES.MAIN_MENU
                # pygame.quit()
                # quit()
            if event.key == pygame.K_BACKQUOTE:  # бахропкъюуркалорукаие - это кнопка тильда
                debug.DEBUG = True
            if not FLY_MOD:
                if event.key == pygame.K_SPACE:
                    if not player.in_process_of_jumping:
                        player.jump()
                if event.key == pygame.K_LSHIFT:
                    if player.h_down == 0:
                        player.dash()
            if event.key == pygame.K_F5:
                save.upload_save(params={'num_floor': current_level_number})
            if event.key == pygame.K_F8:
                for obj in floor.object_list:
                    obj.kill()
                floor, current_level_number = save.download_save()
                player = Player()
            if event.key == pygame.K_e:
                for obj in floor.object_list:
                    if isinstance(obj, Item):
                        if is_the_object_available_for_interaction(player, obj, floor):
                            if type(obj) == End_lvl_crystal:
                                next_level_number = obj.interaction(floor, player)
                                save.upload_save(params={'num_floor': next_level_number})
                                floor, current_level_number = save.download_save()
                                player = Player()
                                game_cycle = GAME_CYCLES.WIN
                                finish_lvl_time = pygame.time.get_ticks()
                            else:
                                obj.interaction(floor, player)
                            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            player.start_hit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s]:
        delta_x_all, delta_y_all = 0, 0
        if keys[pygame.K_w]:
            delta_x, delta_y = player.run(FORWARD, clock.get_fps(), floor)
            delta_x_all += delta_x
            delta_y_all += delta_y
        if keys[pygame.K_a]:
            delta_x, delta_y = player.run(LEFT, clock.get_fps(), floor)
            delta_x_all += delta_x
            delta_y_all += delta_y
        if keys[pygame.K_d]:
            delta_x, delta_y = player.run(RIGHT, clock.get_fps(), floor)
            delta_x_all += delta_x
            delta_y_all += delta_y
        if keys[pygame.K_s]:
            delta_x, delta_y = player.run(BACK, clock.get_fps(), floor)
            delta_x_all += delta_x
            delta_y_all += delta_y
        minimap.CENTER_W -= delta_x_all * minimap.SCALE
        minimap.CENTER_H += delta_y_all * minimap.SCALE

    if FLY_MOD:
        if keys[pygame.K_SPACE]:
            player.fly(UP, clock.get_fps())
        if keys[pygame.K_LSHIFT]:
            player.fly(DOWN, clock.get_fps())
    return game_cycle, floor, player, current_level_number, finish_lvl_time


def control_splash(game_cycle, start_lvl_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            game_cycle = GAME_CYCLES.GAMEPLAY
            start_lvl_time = pygame.time.get_ticks()

    return game_cycle, start_lvl_time
