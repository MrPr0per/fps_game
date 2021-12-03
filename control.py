import pygame
import debug
from settings import *


def control(player, clock, minimap, floor):
    sensitivity = 0.06

    if pygame.mouse.get_focused():
        difference_w = pygame.mouse.get_pos()[0] - WIDTH / 2
        # difference_h = pygame.mouse.get_pos()[1] - HEIGHT / 2
        pygame.mouse.set_pos([WIDTH / 2, HEIGHT / 2])
        # player.turn(-difference_w * sensitivity, -difference_h * sensitivity)
        player.turn(-difference_w * sensitivity, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_SPACE:
                debug.DEBUG = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s]:
        delta_x, delta_y = 0, 0
        if keys[pygame.K_w]:
            delta_x, delta_y = player.run(FORWARD, clock.get_fps(), floor)
        if keys[pygame.K_a]:
            delta_x, delta_y = player.run(LEFT, clock.get_fps(), floor)
        if keys[pygame.K_d]:
            delta_x, delta_y = player.run(RIGHT, clock.get_fps(), floor)
        if keys[pygame.K_s]:
            delta_x, delta_y = player.run(BACK, clock.get_fps(), floor)
        # TODO: повиксить баг движения сетки когда не надо
        minimap.CENTER_W -= delta_x * minimap.SCALE
        minimap.CENTER_H += delta_y * minimap.SCALE

    if keys[pygame.K_SPACE]:
        player.fly(UP, clock.get_fps())
    if keys[pygame.K_LSHIFT]:
        player.fly(DOWN, clock.get_fps())
