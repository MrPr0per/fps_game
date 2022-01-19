import pygame
import math
import time
import random

import debug
from settings import *
from geometry import Ray, Line_segment, Point, Line, Column
from geometry import *
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
    def __init__(self, clock, minimap, sc):
        # sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        # sc = pygame.display.set_mode((WIDTH, HEIGHT))
        # pygame.display.set_caption('fps v0.0.2')
        pygame.mouse.set_visible(False)
        self.minimap = minimap
        self.sc = sc
        self.clock = clock
        self.font_fps = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_info = pygame.font.SysFont('Lucida Console', 15, bold=True)
        self.pixel_font_size = WIDTH // 50
        self.pixel_font = pygame.font.Font('resourses/fonts/font1.ttf', self.pixel_font_size)
        self.big_pixel_font_size = WIDTH // 30
        self.big_pixel_font = pygame.font.Font('resourses/fonts/font1.ttf', self.big_pixel_font_size)

        self.all_object_to_draw = []

    def clear_screen(self):
        self.sc.fill((0, 0, 0))
        self.minimap.sc.fill((0, 0, 0))

    def draw_horizon(self, player, floor):
        # неважно, что это за строки
        # важно, что они находят экранную высоту горизонта
        dist = ALMOST_INFINITY
        n = 180
        angle_point = find_angle_point(
            Point(0, player.h_down + player.h),
            Point(dist, 0))
        if angle_point > n:
            angle_point -= 360
        angle_border_point = player.bott_angle
        if angle_border_point > n:
            angle_border_point -= 360
        angular_size_h_down = angle_point - angle_border_point
        screen_h_down = HEIGHT * angular_size_h_down / player.fov_h
        screen_pos_horizon = HEIGHT - screen_h_down

        #

        texture = SKYS[floor.sky_text_num]
        crop_width = texture.get_width() * (player.fov_w / 360)
        crop_height = HEIGHT * (crop_width / WIDTH)

        offset_x = (1 - (player.angle_w / 360)) * texture.get_width()

        angle = player.angle_h
        if 0 <= angle <= 90:
            angle_h = 90 - angle
        if 90 < angle < 270:
            angle_h = 0
        if 270 <= angle <= 360:
            angle_h = 90 - angle + 360
        offset_y = (texture.get_height() - crop_height) / 180 * angle_h

        # корректируем значение вертикального смещения:
        h1 = texture.get_height() / 2
        h2 = screen_pos_horizon / (WIDTH / crop_width) + offset_y
        dh = h2 - h1
        offset_y -= dh

        # почему то экран все рано улетает за пределы всех измерений,
        # но не слишком сильно, так что просто оставим эту корректировку
        if offset_y < 0:
            offset_y = 0
        if offset_y > texture.get_height() - crop_height:
            offset_y = texture.get_height() - crop_height

        # отрисовываем картинку
        if crop_width < texture.get_width() - offset_x:
            texture1 = texture.subsurface(offset_x, offset_y, crop_width, crop_height)
            texture1 = pygame.transform.scale(texture1, (WIDTH, HEIGHT))
            sc.blit(texture1, (0, 0))
        else:
            texture1 = texture.subsurface(offset_x, offset_y, texture.get_width() - offset_x,
                                          crop_height)
            texture2 = texture.subsurface(0, offset_y,
                                          crop_width - (texture.get_width() - offset_x),
                                          crop_height)

            scale = WIDTH / crop_width
            texture1 = pygame.transform.scale(texture1, (texture1.get_width() * scale + 2, HEIGHT))
            texture2 = pygame.transform.scale(texture2, (texture2.get_width() * scale, HEIGHT))

            sc.blit(texture1, (0, 0))
            sc.blit(texture2, ((texture.get_width() - offset_x) * scale, 0))

        #

        # дэбаг
        # мне жалко его стирать, так что пусть пока будет
        show_debug_info = False
        if show_debug_info:
            scale_screen = 1 / 5
            # схематично отрисовывем текстуру неба
            pygame.draw.rect(sc, (255, 0, 255), (
                0, 0, texture.get_width() * scale_screen, texture.get_height() * scale_screen), 3)
            # схематично отрисовывем используемую ее часть
            pygame.draw.rect(sc, (255, 255, 0), (
                offset_x * scale_screen, offset_y * scale_screen, crop_width * scale_screen,
                crop_height * scale_screen), 3)

            # схематично отрисовываем горизонт на текстуре
            h1 = texture.get_height() / 2
            pygame.draw.line(sc, (200, 0, 200), (0, h1 * scale_screen),
                             (texture.get_width() * scale_screen, h1 * scale_screen), 3)
            # схематично отрисовываем горизонт на деле
            h2 = screen_pos_horizon / (WIDTH / crop_width) + offset_y
            pygame.draw.line(sc, (200, 200, 0), (0, h2 * scale_screen),
                             (texture.get_width() * scale_screen, h2 * scale_screen), 3)
            # калькулируем их разницу
            dh = h2 - h1

            # отрисовываем линию горизонта
            color = find_color(dist, base_color=(200, 50, 50))
            pygame.draw.rect(self.sc, color,
                             (0, screen_pos_horizon, WIDTH, 5))
            # (если она совпала с линией горизонта на тектуре, поздравляю, вы молодец)
            # сам себя не похвалишь...

        #

        draw_ground = True
        if draw_ground:
            pygame.draw.rect(self.sc, (0, 0, 0),
                             (0, screen_pos_horizon, WIDTH, screen_h_down))
            last_h = 0
            for i in range(MAX_DIST_HORIZON * SMOOTHING_HORIZON):
                # dist = ALMOST_INFINITY
                dist = i / SMOOTHING_HORIZON
                n = 180
                angle_point = find_angle_point(
                    Point(0, player.h_down + player.h),
                    Point(dist, 0))
                if angle_point > n:
                    angle_point -= 360

                angle_border_point = player.bott_angle
                if angle_border_point > n:
                    angle_border_point -= 360

                angular_size_h_down = angle_point - angle_border_point
                screen_h_down = HEIGHT * angular_size_h_down / player.fov_h
                # color = find_color(dist, base_color=(110, 175, 219))
                color = find_color(dist, base_color=floor.ground_color)

                pygame.draw.rect(self.sc, color,
                                 (0, HEIGHT - screen_h_down, WIDTH, screen_h_down - last_h + 1))
                last_h = screen_h_down

    def draw_world(self, player, floor):
        self.calculate_raycast(player, floor)
        self.calculate_objects(player, floor)
        self.all_object_to_draw.sort(key=lambda x: x.dist, reverse=True)
        for obj in self.all_object_to_draw:
            self.sc.blit(obj.obj, obj.pos)
        self.all_object_to_draw.clear()

    def calculate_raycast(self, player, floor):
        debug.debug_first_ray = False
        for ray_number in range(NUM_RAYS):
            cur_angle = player.left_angle - ray_number * DELTA_ANGLE
            ray = Ray(player, cur_angle)
            nearest_intersection = None
            list_intersections = []
            for build in floor.build_list:
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
                    for intersection in list_intersections:
                        obj = draw_column(dist=intersection.dist, column=intersection.column,
                                          texture_name=intersection.texture_name,
                                          offset=intersection.offset,
                                          player=player, cur_angle=cur_angle, sc=self.sc)
                        self.all_object_to_draw.append(obj)
                else:
                    obj = draw_column(dist=nearest_intersection.dist,
                                      column=nearest_intersection.column,
                                      texture_name=nearest_intersection.texture_name,
                                      offset=nearest_intersection.offset, player=player,
                                      cur_angle=cur_angle, sc=self.sc)
                    self.all_object_to_draw.append(obj)

    def calculate_objects(self, player, floor):
        for obj in floor.object_list:
            angle = find_angle_point(player, obj)
            # неTODO добавить подсчет этого расширения по нормальному
            # я вообще это условие видимости вырубил лол)
            # а я его подчистую вырезал)
            # можно убирать туду
            # ок, теперь без этого условия у меня лагает, придется писать
            # написал, все равно лагает >:/
            left_offset_angle = (find_angle_point(player, obj) + 90) % 360
            inaccuracy = 0.2
            left_border_point = Point(
                obj.x + math.cos(math.radians(left_offset_angle)) * (obj.true_radius + inaccuracy),
                obj.y + math.sin(math.radians(left_offset_angle)) * (obj.true_radius + inaccuracy))
            right_border_point = Point(
                obj.x - math.cos(math.radians(left_offset_angle)) * (obj.true_radius + inaccuracy),
                obj.y - math.sin(math.radians(left_offset_angle)) * (obj.true_radius + inaccuracy))

            if not (is_the_point_in_the_field_of_view(
                    player, player.angle_w, player.fov_w, left_border_point) or
                    is_the_point_in_the_field_of_view(
                        player, player.angle_w, player.fov_w, right_border_point)):
                continue
            if not DRAW_ALL_OBJECTS:
                is_left_behind_wall = is_there_a_dot_behind_the_wall(player, left_border_point,
                                                                     floor.build_list)
                is_right_behind_wall = is_there_a_dot_behind_the_wall(player, right_border_point,
                                                                      floor.build_list)
                if is_left_behind_wall and is_right_behind_wall:
                    continue

            # pygame.draw.circle(self.minimap.sc, (0, 255, 255),
            #                    convert_crds_to_scren(*obj.pos, player, self.minimap),
            #                    obj.w / 2 * self.minimap.SCALE * 2)

            dist = find_dist(player, obj)
            if not FISH_EYE:
                dist *= math.cos(math.radians(player.angle_w - find_angle_point(player, obj)))

            # ограничиваем дистанцию, чтобы объекты не были слишком большими и не лагало
            if dist < obj.true_radius + player.true_radius:
                dist = obj.true_radius + player.true_radius

            screen_h, screen_h_down = find_screen_h_and_h_down(dist, obj, player, self.sc)

            if isinstance(obj, Enemy):
                true_enemy_angle = (obj.angle - find_angle_point(player, obj)) % 360
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
            elif isinstance(obj, Item):
                image = objects_sprites[ITEMS][obj.name][DEFAULT]
            else:
                image = obj.image

            screen_w = image.get_width() * screen_h / image.get_height()
            if player.left_angle < angle:
                x = ((player.left_angle + 180) % 360 - (
                        angle + 180) % 360) / player.fov_w * WIDTH
            else:
                x = (player.left_angle - angle) / player.fov_w * WIDTH
            x -= screen_w / 2
            y = HEIGHT - screen_h_down - screen_h
            obj_screen_crd = (x, y)

            image = pygame.transform.scale(image, (screen_w, screen_h))

            if SHADE_OBJECTS:
                brightness = find_brightness(dist)
                shade = pygame.Surface((image.get_width(), image.get_height())).convert_alpha()
                shade.fill((0, 0, 0, 255 * (1 - brightness)))
                mask = image
                shade.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
                image.blit(shade, (0, 0))

            self.all_object_to_draw.append(Object_to_draw(image, obj_screen_crd, dist))

    def draw_player(self, player, floor):
        if player.in_progress_of_hit:
            time_now = pygame.time.get_ticks()
            delta_time = time_now - player.hit_start_time
            index = int(delta_time / objects_sprites[PLAYER][ATTACK][FRAME_DELAY])
            if index >= len(objects_sprites[PLAYER][ATTACK][FRAMES]):
                player.in_progress_of_hit = False
                player.hit_start_time = None
                image = objects_sprites[PLAYER][DEFAULT]
                player.already_hit_in_the_current_animation_cycle = False
            else:
                if index == 4 and not player.already_hit_in_the_current_animation_cycle:
                    player.already_hit_in_the_current_animation_cycle = True
                    player.hit(floor)
                image = objects_sprites[PLAYER][ATTACK][FRAMES][index]
        else:
            image = objects_sprites[PLAYER][DEFAULT]
        scale = (2 / 3 * WIDTH) / image.get_width()
        image = pygame.transform.scale(image,
                                       (image.get_width() * scale, image.get_height() * scale))
        screen_pos = (HALF_WIDTH - image.get_width() / 2, HEIGHT - image.get_height())
        self.sc.blit(image, screen_pos)

    def draw_help(self, player, floor):
        for obj in floor.object_list:
            if isinstance(obj, Item):
                if is_the_object_available_for_interaction(player, obj, floor):
                    label_h = HEIGHT * 0.70
                    render = self.pixel_font.render(obj.name_for_player, False, (200, 200, 200))
                    self.sc.blit(render, (WIDTH / 2 - render.get_width() / 2,
                                          label_h + self.pixel_font_size * 1.1 * 0))
                    render = self.pixel_font.render('нажмите E чтобы взять', False, (200, 200, 200))
                    self.sc.blit(render, (WIDTH / 2 - render.get_width() / 2,
                                          label_h + self.pixel_font_size * 1.1 * 1))

    def draw_inventory(self, player, floor):
        cell_size = 80
        for i in range(player.inventory_size):
            background = pygame.Surface((cell_size, cell_size)).convert_alpha()
            background.fill((0, 0, 0, 100))
            self.sc.blit(background, (i * cell_size, HEIGHT - cell_size))
            pygame.draw.rect(self.sc, (200, 200, 200),
                             (i * cell_size, HEIGHT - cell_size, cell_size, cell_size), 2)
            if player.inventory[i] is not None:
                image = objects_sprites[ITEMS][player.inventory[i].name][ICON]
                image = pygame.transform.scale(image, (cell_size, cell_size))
                self.sc.blit(image, (i * cell_size, HEIGHT - cell_size))

    def draw_minimap(self, player, floor):
        # self.minimap.sc.fill((0, 0, 0))

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
        for obj in floor.object_list:
            # image = pygame.transform.scale(obj.image, (obj.w * self.minimap.SCALE,
            #                                            obj.h * self.minimap.SCALE))
            # obj_screen_crd = convert_crds_to_scren(*obj.pos, self.player, self.minimap)
            # obj_screen_crd = (obj_screen_crd[0] - image.get_width() / 2,
            #                   obj_screen_crd[1] - image.get_height() / 2)
            # self.minimap.sc.blit(image, obj_screen_crd)

            obj_screen_crd = convert_crds_to_scren(*obj.pos, player, self.minimap)
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
                                     player, self.minimap), 3)
            elif isinstance(obj, Item):
                color = (200, 200, 0)
            else:
                color = (50, 50, 50)
            pygame.draw.circle(self.minimap.sc, color, obj_screen_crd,
                               obj.w / 2 * self.minimap.SCALE)

        # игрок
        screen_player_crd = convert_crds_to_scren(*player.pos, player, self.minimap)
        pygame.draw.circle(self.minimap.sc, (100, 200, 0), screen_player_crd,
                           player.radius / COLLIDE_SCALE * self.minimap.SCALE)
        pygame.draw.line(self.minimap.sc, (100, 200, 0), screen_player_crd,
                         convert_crds_to_scren(
                             player.x + math.cos(
                                 math.radians(player.left_angle)) * MAX_DIST_RAY,
                             player.y + math.sin(
                                 math.radians(player.left_angle)) * MAX_DIST_RAY,
                             player, self.minimap))
        pygame.draw.line(self.minimap.sc, (100, 200, 0), screen_player_crd,
                         convert_crds_to_scren(
                             player.x + math.cos(
                                 math.radians(player.right_angle)) * MAX_DIST_RAY,
                             player.y + math.sin(
                                 math.radians(player.right_angle)) * MAX_DIST_RAY,
                             player, self.minimap))
        pygame.draw.line(self.minimap.sc, (200, 100, 0), screen_player_crd,
                         convert_crds_to_scren(
                             player.x + math.cos(
                                 math.radians(player.angle_w)) * MAX_DIST_RAY,
                             player.y + math.sin(
                                 math.radians(player.angle_w)) * MAX_DIST_RAY,
                             player, self.minimap))
        # карта
        for build in floor.build_list:
            for point in build.column_list:
                x, y = convert_crds_to_scren(*point.pos, player, self.minimap)
                pygame.draw.circle(self.minimap.sc, (200, 200, 200), (x, y), 2)
            points = list(
                map(lambda a: convert_crds_to_scren(*a.pos, player, self.minimap),
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

    def draw_interface(self, player):
        max_len_hp_bar = 300
        width_hp_bar = 15
        pygame.draw.rect(sc, (100, 0, 0), (30, 20, max_len_hp_bar, width_hp_bar))
        pygame.draw.rect(sc, (200, 50, 0), (
            30, 20, max_len_hp_bar * (player.hp / player.max_xp), width_hp_bar))

        text_list = [
            f'add_speed = {player.add_speed}',
            # f'already_hit_in_the_current_animation_cycle = {player.already_hit_in_the_current_animation_cycle}'
        ]
        for i in range(len(text_list)):
            render = self.font_info.render(text_list[i], False, (200, 200, 200))
            # self.sc.blit(render, (10, (HEIGHT - len(text_list) * 20 - 20) + 20 * i))
            self.sc.blit(render, (30, 50 + 20 * i))

    def draw_game_screen(self, game_cycle, flicker_start_time, passage_time):

        time_now = pygame.time.get_ticks()
        delta_time = time_now - flicker_start_time
        if delta_time > 800:
            brigtness = 100
            r = random.randint(brigtness, brigtness)
            g = random.randint(0, brigtness)
            b = random.randint(0, brigtness)
            k = brigtness * 3 / sum((r, g, b))
            r *= k
            g *= k
            b *= k
            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255

            self.sc.fill((r, g, b))
            flicker_start_time = time_now

        if game_cycle == GAME_CYCLES.DEATH:
            # back = Game_screens_sprites.win_back
            image = Game_screens_sprites.death
        if game_cycle == GAME_CYCLES.WIN:
            # back = Game_screens_sprites.death_back
            image = Game_screens_sprites.win
            render = self.big_pixel_font.render(f'{passage_time // 1000} sec', True, (0, 0, 0))

        # back = pygame.transform.scale(back, (WIDTH, HEIGHT))
        scale = WIDTH / image.get_width() * 0.9
        image = pygame.transform.scale(image,
                                       (image.get_width() * scale, image.get_height() * scale))
        # self.sc.blit(back, (0, 0))
        self.sc.blit(image,
                     (HALF_WIDTH - image.get_width() / 2, HALF_HEIGHT - image.get_height() / 2))
        if game_cycle == GAME_CYCLES.WIN:
            self.sc.blit(render, (HALF_WIDTH - render.get_width() / 2, HEIGHT * 0.65 - render.get_height() / 2))

        return flicker_start_time


def convert_crds_to_scren(x, y, player, minimap):
    screen_x = minimap.WIDTH / 2 + (x - player.x) * minimap.SCALE
    screen_y = minimap.HEIGHT / 2 - (y - player.y) * minimap.SCALE
    return screen_x, screen_y


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
    if not FISH_EYE:
        dist *= math.cos(math.radians(player.angle_w - cur_angle))

    # пусть это условие создает визуальные баги, если
    # уткнуться носом в стену, но зато фпс не падает до 15!
    # if dist < player.true_radius + 5:
    #     dist = player.true_radius + 5

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
            texture.fill((0, 0, 0))
            # print(error, texture.get_rect(), pygame.Rect(
            #     (screen_offset * texture_scale) % (width_texture - COLUMN_WIDTH * texture_scale), 0,
            #     COLUMN_WIDTH * texture_scale, texture.get_height()))
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
