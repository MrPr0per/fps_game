import pygame
import math
from numba import njit, jit
import time

import debug
from settings import *
from geometry import Ray, Line_segment, Point, Line, Column
from geometry import find_dist, find_angle_point
from resourses import *
from enemy import *


class Object_to_draw:
    IMAGE = 'IMAGE'
    RECT = 'RECT'

    def __init__(self, obj, pos, dist, type_object=IMAGE):
        self.obj = obj
        self.pos = pos
        self.dist = dist
        self.type_object = type_object


class Drawing:
    def __init__(self, clock, player, floor, minimap):
        sc = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('fps v0.0.2')
        pygame.mouse.set_visible(False)
        self.player = player
        self.floor = floor
        self.minimap = minimap
        self.sc = sc
        self.clock = clock
        self.font_fps = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_info = pygame.font.SysFont('Lucida Console', 15, bold=True)
        self.all_object_to_draw = []

    def clear_screen(self):
        self.sc.fill((0, 0, 0))

    def draw_horizon(self):
        # dist =
        # n = 180
        # angle_point = find_angle_point(
        #     Point(0, self.player.h_down + self.player.h),
        #     Point(dist, 0))
        # if angle_point > n:
        #     angle_point -= 360
        #
        # angle_border_point = self.player.bott_angle
        # if angle_border_point > n:
        #     angle_border_point -= 360
        #
        # angular_size_h_down = angle_point - angle_border_point
        # screen_h_down = HEIGHT * angular_size_h_down / self.player.fov_h
        # color = pygame.Color(0)
        # smooth = 5
        # brightness = 100 * smooth / (dist + smooth)
        # try:
        #     color.hsva = (100, 70, brightness)
        # except Exception:
        #     print(brightness)
        #
        # pygame.draw.rect(self.sc, color,
        #                  (0, HEIGHT - screen_h_down, WIDTH, screen_h_down))
        step = 10
        for i in range(0, HEIGHT, step):
            color = (i / HEIGHT * 255, 50, (HEIGHT - i) / HEIGHT * 255)
            # print(color)
            self.sc.fill(color, (0, i, WIDTH, step))

        last_h = 0
        for i in range(MAX_DIST_HORIZON * SMOOTHING_HORIZON):
            # dist = ALMOST_INFINITY
            dist = i / SMOOTHING_HORIZON
            n = 180
            angle_point = find_angle_point(
                Point(0, self.player.h_down + self.player.h),
                Point(dist, 0))
            if angle_point > n:
                angle_point -= 360

            angle_border_point = self.player.bott_angle
            if angle_border_point > n:
                angle_border_point -= 360

            angular_size_h_down = angle_point - angle_border_point
            screen_h_down = HEIGHT * angular_size_h_down / self.player.fov_h
            color = find_color(dist, base_color=((110, 175, 219)))

            pygame.draw.rect(self.sc, color,
                             (0, HEIGHT - screen_h_down, WIDTH, screen_h_down - last_h + 1))
            last_h = screen_h_down

    def draw_world(self):
        self.calculate_raycast()
        self.calculate_objects()
        self.all_object_to_draw.sort(key=lambda x: x.dist, reverse=True)
        for obj in self.all_object_to_draw:
            self.sc.blit(obj.obj, obj.pos)
        self.all_object_to_draw.clear()

    def calculate_raycast(self):
        debug.debug_first_ray = False
        for ray_number in range(NUM_RAYS):
            cur_angle = self.player.left_angle - ray_number * DELTA_ANGLE
            ray = Ray(self.player, cur_angle)
            nearest_intersection = None
            list_intersections = []
            for build in self.floor.build_list:
                for wall in build.wall_list:
                    intersection = ray.find_intersection(wall)
                    if intersection:
                        intersection.texture_name = build.texture_name
                        if DRAW_ALL_WALS:
                            list_intersections.append(intersection)
                        if nearest_intersection:
                            if intersection.dist < nearest_intersection.dist:
                                nearest_intersection = intersection
                        else:
                            nearest_intersection = intersection
            if nearest_intersection:
                if DRAW_ALL_WALS:
                    # list_intersections = sorted(list_intersections, key=lambda x: x.dist,
                    #                             reverse=True)
                    for intersection in list_intersections:
                        obj = draw_column(dist=intersection.dist, column=intersection.column,
                                          texture_name=intersection.texture_name,
                                          offset=intersection.offset,
                                          player=self.player, cur_angle=cur_angle, sc=self.sc)
                        self.all_object_to_draw.append(obj)
                else:
                    obj = draw_column(dist=nearest_intersection.dist,
                                      column=nearest_intersection.column,
                                      texture_name=nearest_intersection.texture_name,
                                      offset=nearest_intersection.offset, player=self.player,
                                      cur_angle=cur_angle, sc=self.sc)
                    self.all_object_to_draw.append(obj)

    def calculate_objects(self):
        for obj in self.floor.object_list:
            angle = find_angle_point(self.player, obj)
            # неTODO добавить подсчет этого расширения по нормальному
            # я вообще это условие видимости вырубил лол)
            # а я его подчистую вырезал)
            # можно убирать туду
            dist = find_dist(self.player, obj)
            if dist < obj.true_radius + self.player.true_radius:
                dist = obj.true_radius + self.player.true_radius
            screen_h, screen_h_down = find_screen_h_and_h_down(dist, obj, self.player, self.sc)
            if isinstance(obj, Enemy):
                true_enemy_angle = (obj.angle - find_angle_point(self.player, obj)) % 360
                if obj.hp > 0:
                    if obj.in_progress_of_hit:
                        time_now = pygame.time.get_ticks()
                        delta_time = time_now - obj.hit_start_time
                        index = int(
                            delta_time / objects_sprites[ENEMIES][obj.name][ATTACK][FRAME_DELAY])
                        if index >= len(objects_sprites[ENEMIES][obj.name][ATTACK][FRAMES]):
                            obj.in_progress_of_hit = False
                            obj.hit_start_time = None
                        else:
                            image = objects_sprites[ENEMIES][obj.name][ATTACK][FRAMES][index]
                    if not obj.in_progress_of_hit:
                        n_positions_to_view = len(
                            objects_sprites[ENEMIES][obj.name][ROTATION][FRAMES])
                        angle_of_one_position_to_view = 360 / n_positions_to_view
                        true_enemy_angle = (true_enemy_angle - (
                                    180 - 360 / (2 * n_positions_to_view))) % 360
                        index = int(true_enemy_angle // angle_of_one_position_to_view)
                        image = objects_sprites[ENEMIES][obj.name][ROTATION][FRAMES][index]
                else:
                    image = objects_sprites[ENEMIES][obj.name][DEAD]
            else:
                image = obj.image

            screen_w = image.get_width() * screen_h / image.get_height()
            if self.player.left_angle < angle:
                x = ((self.player.left_angle + 180) % 360 - (
                        angle + 180) % 360) / self.player.fov_w * WIDTH
            else:
                x = (self.player.left_angle - angle) / self.player.fov_w * WIDTH
            y = HEIGHT - screen_h_down - screen_h
            obj_screen_crd = (x, y)
            obj_screen_crd = (obj_screen_crd[0] - image.get_width() / 2, obj_screen_crd[1])

            if not (y < HEIGHT or y + image.get_height() > 0 or
                    x + image.get_width() < 0 or x > WIDTH):
                continue

            image = pygame.transform.scale(image, (screen_w, screen_h))

            if SHADE_OBJECTS:
                brightness = find_brightness(dist)
                shade = pygame.Surface((image.get_width(), image.get_height())).convert_alpha()
                shade.fill((0, 0, 0, 255 * (1 - brightness)))
                mask = image
                shade.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
                image.blit(shade, (0, 0))

            self.all_object_to_draw.append(Object_to_draw(image, obj_screen_crd, dist))

    def draw_player(self):
        scale = 5
        if self.player.in_progress_of_hit:
            time_now = pygame.time.get_ticks()
            delta_time = time_now - self.player.hit_start_time
            index = int(delta_time / objects_sprites[PLAYER][ATTACK][FRAME_DELAY])
            if index >= len(objects_sprites[PLAYER][ATTACK][FRAMES]):
                self.player.in_progress_of_hit = False
                self.player.hit_start_time = None
                image = objects_sprites[PLAYER][DEFAULT]
                self.player.already_hit_in_the_current_animation_cycle = False
            else:
                if index == 4 and not self.player.already_hit_in_the_current_animation_cycle:
                    self.player.already_hit_in_the_current_animation_cycle = True
                    self.player.hit(self.floor)
                image = objects_sprites[PLAYER][ATTACK][FRAMES][index]
        else:
            image = objects_sprites[PLAYER][DEFAULT]
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        screen_pos = (HALF_WIDTH - image.get_width() / 2, HEIGHT - image.get_height())
        self.sc.blit(image, screen_pos)

    def draw_minimap(self):
        self.minimap.sc.fill((0, 0, 0))

        i = self.minimap.CENTER_W % self.minimap.LINE_SCALE
        while i < self.minimap.WIDTH:
            pygame.draw.line(self.minimap.sc, (50, 50, 50), (i, 0), (i, self.minimap.HEIGHT))
            i += self.minimap.LINE_SCALE
        i = self.minimap.CENTER_H % self.minimap.LINE_SCALE
        while i < self.minimap.WIDTH:
            pygame.draw.line(self.minimap.sc, (50, 50, 50), (0, i), (self.minimap.WIDTH, i))
            i += self.minimap.LINE_SCALE

        pygame.draw.line(self.minimap.sc, (100, 100, 100), (self.minimap.CENTER_W, 0),
                         (self.minimap.CENTER_W, self.minimap.HEIGHT))
        pygame.draw.line(self.minimap.sc, (100, 100, 100), (0, self.minimap.CENTER_H),
                         (self.minimap.WIDTH, self.minimap.CENTER_H))

        # объекты
        for obj in self.floor.object_list:
            # image = pygame.transform.scale(obj.image, (obj.w * self.minimap.SCALE,
            #                                            obj.h * self.minimap.SCALE))
            # obj_screen_crd = convert_crds_to_scren(*obj.pos, self.player, self.minimap)
            # obj_screen_crd = (obj_screen_crd[0] - image.get_width() / 2,
            #                   obj_screen_crd[1] - image.get_height() / 2)
            # self.minimap.sc.blit(image, obj_screen_crd)

            obj_screen_crd = convert_crds_to_scren(*obj.pos, self.player, self.minimap)
            if isinstance(obj, Enemy):
                if obj.hp > 0:
                    color = (240, 0, 0)
                else:
                    color = (100, 0, 10)
                pygame.draw.line(self.minimap.sc, color, obj_screen_crd,
                                 convert_crds_to_scren(
                                     obj.x + math.cos(math.radians(
                                         obj.angle)) * obj.radius / COLLIDE_SCALE * 1.5,
                                     obj.y + math.sin(math.radians(
                                         obj.angle)) * obj.radius / COLLIDE_SCALE * 1.5,
                                     self.player, self.minimap), 3)
            else:
                color = (150, 150, 50)
            pygame.draw.circle(self.minimap.sc, color, obj_screen_crd,
                               obj.w / 2 * self.minimap.SCALE)

        # игрок
        screen_player_crd = convert_crds_to_scren(*self.player.pos, self.player, self.minimap)
        pygame.draw.circle(self.minimap.sc, (100, 200, 0), screen_player_crd,
                           self.player.radius / COLLIDE_SCALE * self.minimap.SCALE)
        pygame.draw.line(self.minimap.sc, (100, 200, 0), screen_player_crd,
                         convert_crds_to_scren(
                             self.player.x + math.cos(
                                 math.radians(self.player.left_angle)) * MAX_DIST_RAY,
                             self.player.y + math.sin(
                                 math.radians(self.player.left_angle)) * MAX_DIST_RAY,
                             self.player, self.minimap))
        pygame.draw.line(self.minimap.sc, (100, 200, 0), screen_player_crd,
                         convert_crds_to_scren(
                             self.player.x + math.cos(
                                 math.radians(self.player.right_angle)) * MAX_DIST_RAY,
                             self.player.y + math.sin(
                                 math.radians(self.player.right_angle)) * MAX_DIST_RAY,
                             self.player, self.minimap))
        pygame.draw.line(self.minimap.sc, (200, 100, 0), screen_player_crd,
                         convert_crds_to_scren(
                             self.player.x + math.cos(
                                 math.radians(self.player.angle_w)) * MAX_DIST_RAY,
                             self.player.y + math.sin(
                                 math.radians(self.player.angle_w)) * MAX_DIST_RAY,
                             self.player, self.minimap))
        # for i in range(NUM_RAYS):
        #     angle = self.player.left_angle - i * DELTA_ANGLE
        #     pygame.draw.line(self.minimap.sc, (100, 100, 0), screen_player_crd,
        #                      convert_crds_to_scren(
        #                          self.player.x + math.cos(math.radians(angle)) * MAX_DIST_RAY,
        #                          self.player.y + math.sin(math.radians(angle)) * MAX_DIST_RAY,
        #                          self.player, self.minimap))
        # карта
        for build in self.floor.build_list:
            for point in build.column_list:
                x, y = convert_crds_to_scren(*point.pos, self.player, self.minimap)
                pygame.draw.circle(self.minimap.sc, (200, 200, 200), (x, y), 2)
            points = list(
                map(lambda a: convert_crds_to_scren(*a.pos, self.player, self.minimap),
                    build.column_list))
            # points = list(map(lambda a: (a.x, a.y), build.point_list))
            pygame.draw.lines(self.minimap.sc, (200, 200, 200), build.is_closed, points)

        pygame.draw.rect(self.minimap.sc, (255, 255, 255),
                         (0, 0, self.minimap.WIDTH, self.minimap.HEIGHT), 2)

        self.sc.blit(self.minimap.sc, self.minimap.POS)

    def draw_fps(self):
        fps = int(self.clock.get_fps())
        color = pygame.Color('white')
        if fps < 30:
            color = pygame.Color('red')
        elif fps < 60:
            color = pygame.Color('cyan')
        elif fps >= 60:
            color = pygame.Color('green')

        render = self.font_fps.render(str(fps), False, color)
        self.sc.blit(render, FPS_POS)

    def draw_interface(self):
        max_len_hp_bar = 300
        width_hp_bar = 15
        pygame.draw.rect(sc, (100, 0, 0), (30, 20, max_len_hp_bar, width_hp_bar))
        pygame.draw.rect(sc, (200, 50, 0), (30, 20, max_len_hp_bar * (self.player.hp / self.player.max_xp), width_hp_bar))

        text_list = [
            f'add_speed = {self.player.add_speed}',
            f'already_hit_in_the_current_animation_cycle = {self.player.already_hit_in_the_current_animation_cycle}'
        ]
        for i in range(len(text_list)):
            render = self.font_info.render(text_list[i], False, (0, 50, 50))
            self.sc.blit(render, (10, (HEIGHT - len(text_list) * 20 - 20) + 20 * i))


def convert_crds_to_scren(x, y, player, minimap):
    return minimap.WIDTH / 2 + (x - player.x) * minimap.SCALE, minimap.HEIGHT / 2 - (
            y - player.y) * minimap.SCALE


def find_color(dist, texture_name=None, base_color=(255, 255, 255)):
    brightness = find_brightness(dist)
    if texture_name:
        if texture_name != TEXT_MISSING:
            base_color = textures[texture_name].get_at((0, 0))
        else:
            base_color = (255, 255, 255)
    color = [int(brightness * base_color[i]) for i in range(3)]
    return color


def find_brightness(dist):
    smooth = 1 / 500
    brightness = 1 / (1 + smooth * dist ** 2)
    return brightness


def correcting_angle(angle):
    """эта функция нужна, чтобы значения угла были не от 0 до 360, а в нужном диапазоне
    (включая отрицательные значения и не включая большие положительные"""
    n = 180
    if angle > n:
        angle -= 360
    elif angle < -n:
        angle += 360

    return angle


def find_screen_h_and_h_down(dist, column, player, sc):
    # находим углы ключевых точек
    angle_top_point = find_angle_point(
        Point(0, player.h_down + player.h),
        Point(dist, column.h_down + column.h))

    angle_bott_point = -360 + find_angle_point(
        Point(0, player.h_down + player.h),
        Point(dist, column.h_down))

    angle_border_point = player.bott_angle

    # корректируем их
    angle_top_point = correcting_angle(angle_top_point)
    angle_bott_point = correcting_angle(angle_bott_point)
    angle_border_point = correcting_angle(angle_border_point)

    # дебажим
    if debug.debug_first_ray:
        print(int(angle_top_point), int(angle_bott_point), int(angle_border_point), sep='\t')
        pygame.draw.circle(sc, (255, 255, 255), (HALF_WIDTH, HALF_HEIGHT), 40, 2)
        for angle, color in [(angle_top_point, (255, 255, 0)),
                             (angle_bott_point, (255, 255, 255)),
                             (angle_border_point, (255, 0, 0)),
                             (player.top_angle, (0, 0, 255))]:
            pygame.draw.line(sc, color, (HALF_WIDTH, HALF_HEIGHT), (
                HALF_WIDTH + math.cos(math.radians(angle)) * 100,
                HALF_HEIGHT - math.sin(math.radians(angle)) * 100))
        debug.debug_first_ray = False

    # находим угловой размер h и h_down cтены
    angular_size_h = angle_top_point - angle_bott_point
    angular_size_h_down = angle_bott_point - angle_border_point

    # переводим угловые значения в экранные
    screen_h = HEIGHT * angular_size_h / player.fov_h
    screen_h_down = HEIGHT * angular_size_h_down / player.fov_h

    return screen_h, screen_h_down


def draw_column(dist, column, texture_name, offset, player, cur_angle, sc):
    # убираем эффект рыбьего глаза
    if not FISH_EYE:
        dist *= math.cos(math.radians(player.angle_w - cur_angle))

    # пусть это условие создает визуальные баги, если
    # уткнуться носом в стену, но зато фпс не падает до 15!
    if dist < player.true_radius + 1:
        dist = player.true_radius + 1

    # находим экранную высоту стены и ее экранное расстояние над землей
    screen_h, screen_h_down = find_screen_h_and_h_down(dist, column, player, sc)

    if player.left_angle < cur_angle:
        x = ((player.left_angle + 180) % 360 - (cur_angle + 180) % 360) / player.fov_w * WIDTH
    else:
        x = (player.left_angle - cur_angle) / player.fov_w * WIDTH
    y = HEIGHT - screen_h_down - screen_h

    if not TEXTURING:
        # определяем цвет в зависимости от расстояния
        color = find_color(dist, texture_name=texture_name)
        # print(color)
        texture = pygame.Surface((COLUMN_WIDTH + 1, screen_h))
        texture.fill(color)
        return Object_to_draw(texture, (x, y), dist)
    elif TEXTURING:
        brightness = find_brightness(dist)
        texture = textures[texture_name]
        texture_scale = texture.get_height() / screen_h
        width_texture = texture.get_width()
        screen_offset = screen_h * offset / column.h
        try:
            texture = texture.subsurface(
                (screen_offset * texture_scale) % (width_texture - COLUMN_WIDTH * texture_scale), 0,
                COLUMN_WIDTH * texture_scale + 1, texture.get_height())
            texture = pygame.transform.scale(texture, (COLUMN_WIDTH + 1, screen_h))
            if SHADE_TEXTURES:
                shade = pygame.Surface((texture.get_width(), texture.get_height())).convert_alpha()
                shade.fill((0, 0, 0, 255 * (1 - brightness)))
                texture.blit(shade, (0, 0))
            # sc.blit(texture, (x, HEIGHT - screen_h_down - screen_h))
        except ValueError as error:
            texture = pygame.Surface((COLUMN_WIDTH + 1, screen_h))
            texture.fill((255, 0, 255))
            print(error, texture.get_rect(), pygame.Rect(
                (screen_offset * texture_scale) % (width_texture - COLUMN_WIDTH * texture_scale), 0,
                COLUMN_WIDTH * texture_scale, texture.get_height()))
        return Object_to_draw(texture, (x, y), dist)

# def calculate_perspective(point_crds, player_crds, player_angle, player_fov, screen_border_angle,
#                           screen_size):
#     point_x, point_y = point_crds
#     player_x, player_y = player_crds
#
#     dist = math.hypot(point_x - player_x, point_y - player_y)
#     if dist == 0:
#         dist = 10 ** -10
#     sin_a = (point_y - player_y) / dist
#     cos_a = (point_x - player_x) / dist
#     point_angle = math.degrees(math.asin(sin_a))
#     if cos_a < 0:
#         point_angle = 180 - point_angle
#     # player_angle = player.angle_w
#
#     alpha = player_angle - point_angle
#     dist_to_screen = (0.5 * screen_size) / math.tan(math.radians(0.5 * player_fov))
#     dist_to_point_proections = dist_to_screen / math.cos(math.radians(alpha))
#
#     proect_x = math.cos(math.radians(point_angle)) * dist_to_point_proections
#     proect_y = math.sin(math.radians(point_angle)) * dist_to_point_proections
#
#     dist_to_border_screen_proection = (0.5 * screen_size) / math.sin(
#         math.radians(0.5 * player_fov))
#     border_screen_proection_x = dist_to_border_screen_proection * math.cos(
#         math.radians(screen_border_angle))
#     border_screen_proection_y = dist_to_border_screen_proection * math.sin(
#         math.radians(screen_border_angle))
#
#     point_screen_crd = math.hypot(proect_x - border_screen_proection_x,
#                                   proect_y - border_screen_proection_y)
#
#     # !!!ВНИМАНИЕ, КОСТЫЛЬ!!!
#
#     if point_angle > screen_border_angle:
#         point_screen_crd *= -1
#
#     # if dist_to_point_proections >= dist_to_border_screen_proection:
#     #     point_screen_crd *= -1
#     if dist_to_point_proections <= 0:
#         point_screen_crd = None
#
#     # ^^^ ПОВЫШЕННЫЙ РИСК БАГОВ ^^^
#
#     # магическая штука, убирающая эффект рыбьего глаза
#     dist *= math.cos(math.radians(player_angle - point_angle))
#
#     return dist, point_screen_crd
#
#
# def draw():
#     sc.fill((0, 0, 0))
#
#     # основная часть
#     for build in floor.build_list:
#         for point in build.point_list:
#             dist, point_screen_x = calculate_perspective(point_crds=point.pos,
#                                                          player_crds=player.pos,
#                                                          player_angle=player.angle_w,
#                                                          player_fov=player.fov_w,
#                                                          screen_border_angle=player.left_angle,
#                                                          screen_size=WIDTH
#                                                          )
#             # теперь определяем Y координату
#             _, point_screen_y1 = calculate_perspective(point_crds=(dist, point.h),
#                                                        player_crds=(0, player.h),
#                                                        player_angle=player.angle_h,
#                                                        player_fov=player.fov_h,
#                                                        screen_border_angle=player.top_angle,
#                                                        screen_size=HEIGHT
#                                                        )
#
#             _, point_screen_y2 = calculate_perspective(point_crds=(dist, point.h_down),
#                                                        player_crds=(0, player.h),
#                                                        player_angle=player.angle_h,
#                                                        player_fov=player.fov_h,
#                                                        screen_border_angle=player.top_angle,
#                                                        screen_size=HEIGHT
#                                                        )
#
#             if all((point_screen_x, point_screen_y1, point_screen_y2)):
#                 pygame.draw.line(sc, (200, 200, 200), (point_screen_x, point_screen_y1),
#                                  (point_screen_x, point_screen_y2))
#
#             # pygame.draw.line(sc, (200, 200, 200), (point_screen_x, screen_h / 2 - 100), (point_screen_x, screen_h / 2 + 100))
#
#     # fps
#     display_fps = str(int(clock.get_fps()))
#     font = pygame.font.SysFont('Arial', 36, bold=True)
#     render = font.render(display_fps, False, (200, 0, 0))
#     sc.blit(render, (WIDTH - 65, 5))
#
#     draw_map = False
#     if draw_map:
#         # игрок
#         if debug:
#             print('deb')
#         screen_player_crd = convert_crds_to_scren(*player.pos)
#         pygame.draw.circle(sc, (100, 200, 0), screen_player_crd, 7)
#         max_dist = 1000
#         pygame.draw.line(sc, (100, 200, 0), screen_player_crd,
#                          convert_crds_to_scren(
#                              player.x + math.cos(math.radians(player.left_angle)) * max_dist,
#                              player.y + math.sin(math.radians(player.left_angle)) * max_dist))
#         pygame.draw.line(sc, (100, 200, 0), screen_player_crd,
#                          convert_crds_to_scren(
#                              player.x + math.cos(math.radians(player.right_angle)) * max_dist,
#                              player.y + math.sin(math.radians(player.right_angle)) * max_dist))
#         pygame.draw.line(sc, (200, 100, 0), screen_player_crd,
#                          convert_crds_to_scren(
#                              player.x + math.cos(math.radians(player.angle_w)) * max_dist,
#                              player.y + math.sin(math.radians(player.angle_w)) * max_dist))
#
#         pygame.draw.line(sc, (0, 100, 200),
#                          convert_crds_to_scren(left_border_screen_proection_x,
#                                                left_border_screen_proection_y),
#                          convert_crds_to_scren(proect_x, proect_y))
#         pygame.draw.line(sc, (0, 100, 200), screen_player_crd,
#                          convert_crds_to_scren(proect_x, proect_y))
#         pygame.draw.circle(sc, (0, 150, 50),
#                            convert_crds_to_scren(left_border_screen_proection_x,
#                                                  left_border_screen_proection_y), 5)
#         pygame.draw.circle(sc, (0, 50, 150), convert_crds_to_scren(proect_x, proect_y), 5)
#
#         # карта
#         for build in floor.build_list:
#             # pygame.draw.lines(sc, (200, 200, 200), True,
#             #                   list(map(lambda x: convert_crds_to_scren(*x.crds), build.point_list)))
#             for point in build.point_list:
#                 x, y = convert_crds_to_scren(*point.pos)
#                 pygame.draw.circle(sc, (200, 200, 200), (x, y), 3)
