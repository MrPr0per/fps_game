import math
import pygame
from settings import *
import debug
from enemy import objects_group, Enemy
from geometry import Column, Line_segment, Point
from geometry import find_dist, find_angle_point, is_the_point_in_the_field_of_view
import save


class Player(Column, pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, angle_w=90, h=1.8, h_down=0, angle_h=0):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 0.4 * COLLIDE_SCALE
        self.true_radius = 0.4
        self.rect = pygame.Rect(x * COLLIDE_SCALE, y * COLLIDE_SCALE, ALMOST_ZERO * COLLIDE_SCALE,
                                ALMOST_ZERO * COLLIDE_SCALE)
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

        self.speed = SPEED
        self.add_speed = 0
        self.fridge = 0.9

        self.angle_of_attack = 180
        self.max_xp = 30
        self.hp = self.max_xp
        self.damage = 10
        self.in_progress_of_hit = False
        self.hit_start_time = None
        # нужно, чтобы удар не засчитывался несколько раз за 1 кадр унамации
        # (урон производится во время определенного кадра анимации)
        self.already_hit_in_the_current_animation_cycle = False

        self.inventory_size = 6
        self.inventory = [None for i in range(self.inventory_size)]

    def turn(self, diff_w, diff_h):
        self.angle_w = (self.angle_w + diff_w) % 360
        self.left_angle = (self.angle_w + self.fov_w / 2) % 360
        self.right_angle = (self.angle_w - self.fov_w / 2) % 360

        if (self.angle_h + diff_h) % 360 <= (90 - self.fov_h / 2) or (
                self.angle_h + diff_h) % 360 >= (270 + self.fov_h / 2):
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
            else:
                dist = None

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

            if COLLISION:
                is_intersection = False
                for obj in floor.object_list:
                    if obj.is_collide:
                        d = find_dist(Point(self.x + delta_x, self.y + delta_y), obj)
                        if d <= self.true_radius + obj.true_radius:
                            is_intersection = True
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

    def start_hit(self):
        if self.in_progress_of_hit:
            return

        self.in_progress_of_hit = True
        self.hit_start_time = pygame.time.get_ticks()

    def hit(self, floor):
        for obj in floor.object_list:
            if isinstance(obj, Enemy):
                # чтобы объект был в зоне атаки, он должен быть:
                #   на достаточно близком расстоянии
                dist = find_dist(self, obj) - self.true_radius - obj.true_radius
                if not dist <= PLAYER_ATTACK_DIST:
                    continue

                #   попадать в зону угла атаки
                if not is_the_point_in_the_field_of_view(self, self.angle_w, self.angle_of_attack,
                                                         obj):
                    continue

                #   не должен находиться за стеной
                attack_vector = Line_segment(self, obj)
                is_intersection = False
                for build in floor.build_list:
                    for wall in build.wall_list:
                        intersection = attack_vector.find_intersection(wall)
                        if intersection:
                            # хз как просчитывать урон, если враг и игрок на разной высоте

                            # if (self.h_down <= intersection.column.h_down + intersection.column.h
                            # ) and (self.h_down + self.h >= intersection.column.h_down):
                            #     is_intersection = True
                            #     self.add_speed = 0
                            #     break
                            is_intersection = True
                            break
                    if is_intersection:
                        break
                if is_intersection:
                    continue

                obj.take_damage(self.damage)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0

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

    def update_death(self, floor, current_level_number, game_cycle, finish_lvl_time):
        if self.hp <= 0:
            floor, current_level_number = save.download_save()
            self.__init__()
            game_cycle = GAME_CYCLES.DEATH
            finish_lvl_time = pygame.time.get_ticks()
        return floor, current_level_number, game_cycle, finish_lvl_time

    def update(self, fps):
        if self.in_process_of_jumping:
            t = pygame.time.get_ticks() / 1000 - self.jump_start_time
            h_down = JUMP_SPEED * t - (g_const * t ** 2) / 2
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
        if self.add_speed > 20:
            self.add_speed = 20

