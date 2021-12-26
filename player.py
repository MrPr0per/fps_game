import math
import pygame
from settings import *
import debug
from enemy import objects_group
from geometric_classes import Column, Line_segment, Point


class Player(Column, pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, angle_w=90, h=1.8, h_down=0, angle_h=0):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 0.4 * COLLIDE_SCALE
        self.rect = pygame.Rect(x * COLLIDE_SCALE, y * COLLIDE_SCALE, ALMOST_ZERO * COLLIDE_SCALE, ALMOST_ZERO * COLLIDE_SCALE)
        Column.__init__(self, x=x, y=y, h=h, h_down=h_down)
        self.angle_w = angle_w % 360
        self.fov_w = FOW_W
        self.left_angle = (angle_w + FOW_W / 2) % 360
        self.right_angle = (angle_w - FOW_W / 2) % 360

        self.angle_h = angle_h
        self.fov_h = FOW_H
        self.bott_angle = angle_h - FOW_H / 2
        self.top_angle = angle_h + FOW_H / 2

        self.in_process_of_jumping = False
        self.jump_start_time = None

        self.in_process_of_vertical_inertia = False
        self.vertical_inertia_start_time = None
        self.in_process_of_pre_jump = False

        # self.dash_start_time = None

        self.speed = SPEED
        self.add_speed = 0
        self.fridge = 0.92

    def turn(self, diff_w, diff_h):
        self.angle_w = (self.angle_w + diff_w) % 360
        self.left_angle = (self.angle_w + self.fov_w / 2) % 360
        self.right_angle = (self.angle_w - self.fov_w / 2) % 360

        self.angle_h = (self.angle_h + diff_h) % 360
        self.top_angle = (self.angle_h + self.fov_h / 2) % 360
        self.bott_angle = (self.angle_h - self.fov_h / 2) % 360

    def run(self, direction, fps, floor):
        if fps != 0:
            time = 1 / fps
            # при движении вбок добавочная скорость меньше:
            if direction == FORWARD or direction == BACK:
                dist = (self.speed + self.add_speed) * time
            elif direction == LEFT or direction == RIGHT:
                dist = (self.speed + self.add_speed * 0.5) * time

            angle = None
            if direction == FORWARD:
                angle = self.angle_w
            if direction == LEFT:
                angle = (self.angle_w + 90) % 360
            if direction == RIGHT:
                angle = (self.angle_w - 90) % 360
            if direction == BACK:
                angle = (self.angle_w + 180) % 360

            delta_x = math.cos(math.radians(angle)) * dist
            delta_y = math.sin(math.radians(angle)) * dist

            move_vector = Line_segment(self, Point(self.x + delta_x, self.y + delta_y))

            if debug.DEBUG:
                print('ddddddddddddd')
                debug.DEBUG = False
            if COLLISION:
                is_intersection = False
                # print(pygame.sprite.spritecollide(self, objects_group, False, pygame.sprite.collide_circle))
                # print(self.rect)
                # print(floor.object_list[0].rect)
                # print()
                self.rect.x += delta_x * COLLIDE_SCALE
                self.rect.y += delta_y * COLLIDE_SCALE
                if pygame.sprite.spritecollide(self, objects_group, False, pygame.sprite.collide_circle):
                    is_intersection = True
                self.rect.x -= delta_x * COLLIDE_SCALE
                self.rect.y -= delta_y * COLLIDE_SCALE
                if not is_intersection:
                    for build in floor.build_list:
                        for wall in build.wall_list:
                            intersection = move_vector.find_intersection(wall)
                            if intersection:
                                if self.h_down <= intersection.column.h_down + intersection.column.h and self.h_down + self.h >= intersection.column.h_down:
                                    is_intersection = True
                                    self.add_speed = 0
                                    break
                        if is_intersection:
                            break

                if is_intersection:
                    return 0, 0

            self.x += delta_x
            self.y += delta_y
            self.pos = (self.x, self.y)
            self.rect.x += delta_x * COLLIDE_SCALE
            self.rect.y += delta_y * COLLIDE_SCALE

            return delta_x, delta_y
        return 0, 0

    def fly(self, direction, fps):
        if fps != 0:
            time = 1 / fps
            dist = SPEED * time
            if direction == UP:
                self.h_down += dist
            if direction == DOWN:
                self.h_down -= dist

    def true_jump(self):
        self.jump_start_time = pygame.time.get_ticks() / 1000
        self.in_process_of_jumping = True
        self.add_speed += 2

    def jump(self):
        if self.in_process_of_vertical_inertia:
            self.true_jump()
        else:
            self.vertical_inertia()
            self.in_process_of_pre_jump = True

    def vertical_inertia(self):
        self.vertical_inertia_start_time = pygame.time.get_ticks() / 1000
        self.in_process_of_vertical_inertia = True

    def dash(self):
        # self.dash_start_time = pygame.time.get_ticks() / 1000
        self.add_speed += 5

    def update(self, fps):
        if self.in_process_of_jumping:
            t = pygame.time.get_ticks() / 1000 - self.jump_start_time
            h_down = JUMP_SPEED * t - (g_const * t ** 2) / 2
            # h = math.sin(math.radians())
            if h_down < 0:
                h_down = 0
                self.in_process_of_jumping = False
                self.jump_start_time = None
                self.vertical_inertia()
            self.h_down = h_down

        if self.in_process_of_vertical_inertia:
            t = pygame.time.get_ticks() / 1000 - self.vertical_inertia_start_time
            if self.in_process_of_pre_jump:
                add_h = -1 * math.sin(math.radians(360 * t * 2.5)) * 0.25
            else:
                add_h = -1 * math.sin(math.radians(360 * t * 1.5)) * 0.25
            if add_h > 0:
                add_h = 0
                self.in_process_of_vertical_inertia = False
                self.vertical_inertia_start_time = None
                if self.in_process_of_pre_jump:
                    self.in_process_of_pre_jump = False
                    self.true_jump()
            self.h = 1.8 + add_h

        # if self.dash_start_time:
        #     t = pygame.time.get_ticks() / 1000 - self.dash_start_time
        #     self.add_speed = (math.sin(math.radians(360 * t - 90)) + 1) * 10
        #     if t > 0.5:
        #         self.dash_start_time = None

        if self.h_down == 0 and not self.in_process_of_vertical_inertia:
            if fps != 0:
                self.add_speed *= self.fridge
        if self.add_speed < 1:
            self.add_speed = 0
