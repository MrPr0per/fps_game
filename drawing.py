import pygame
import debug
from settings import *
from geometric_classes import Ray, Line_segment, Point, Line, Column
import math


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
        self.font_info = pygame.font.SysFont('Lucida Console', 15)

    def clear_screen(self):
        self.sc.fill((0, 0, 0))

    def draw_raycast_alt_version(self):
        # тут какой то странны баг с отрисовкой, когда находишься близко к стене
        for i in range(NUM_RAYS):
            cur_angle = self.player.left_angle - i * DELTA_ANGLE
            ray = Ray(self.player, cur_angle)
            min_dist = None
            nearest_intersection = None
            for build in self.floor.build_list:
                for wall in build.wall_list:
                    intersection = ray.find_intersection(wall)
                    if intersection:
                        dist = math.hypot(intersection.x - self.player.x,
                                          intersection.y - self.player.y)
                        if min_dist:
                            if dist < min_dist:
                                min_dist = dist
                                nearest_intersection = intersection
                        else:
                            min_dist = dist
                            nearest_intersection = intersection

            if min_dist and nearest_intersection:
                if debug.DEBUG:
                    print('debug')
                    debug.DEBUG = False
                # min_dist *= math.cos(math.radians(self.player.angle_w - cur_angle))

                #       в виде сбоку:

                # определяем отрезок экрана
                dist_to_border = 0.5 * WIDTH / math.sin(math.radians(FOW_W / 2))
                full_h = self.player.h_down + self.player.h
                top_border_point = Point(
                    0 + math.cos(math.radians(self.player.top_angle)) * dist_to_border,
                    full_h + math.sin(math.radians(self.player.top_angle)) * dist_to_border, )
                bott_border_point = Point(
                    0 + math.cos(math.radians(self.player.bott_angle)) * dist_to_border,
                    full_h + math.sin(math.radians(self.player.bott_angle)) * dist_to_border, )
                screen = Line(top_border_point, bott_border_point)

                # определяем лучи от головы игрока до верхней и нижней точек column
                ray_bott = Ray(Point(0, full_h), find_angle_point(Point(0, full_h), Point(min_dist,
                                                                                          nearest_intersection.h_down)))
                ray_top = Ray(Point(0, full_h), find_angle_point(Point(0, full_h), Point(min_dist,
                                                                                         nearest_intersection.h)))

                # определяем их пересечения с экраном
                intersection_bott = ray_bott.find_intersection(screen)
                intersection_top = ray_top.find_intersection(screen)

                # определяем расстояние от верхней точки экрана до пересечений
                dist_top = find_dist(top_border_point, intersection_top)
                dist_bott = find_dist(top_border_point, intersection_bott)

                # определяем знак
                angle_screen = find_angle_point(top_border_point, bott_border_point)
                angle_top = find_angle_point(top_border_point, intersection_top)
                angle_bott = find_angle_point(top_border_point, intersection_bott)
                if not (angle_top - 5 < angle_screen < angle_top + 5):
                    dist_top *= -1
                if not (angle_bott - 5 < angle_screen < angle_bott + 5):
                    dist_bott *= -1
                visual_height = dist_bott - dist_top

                # отрисовка
                color = pygame.Color(0)
                smooth = 5
                brightness = 100 * smooth / (min_dist + smooth)
                try:
                    color.hsva = (0, 0, brightness)
                except Exception:
                    print(brightness)

                pygame.draw.rect(self.sc, color, (
                    int(i / SCALE_N_RAYS), int(dist_top), int(WIDTH / NUM_RAYS),
                    int(visual_height)))

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
            color = find_color(dist, 228, 50)

            pygame.draw.rect(self.sc, color,
                             (0, HEIGHT - screen_h_down, WIDTH, screen_h_down - last_h + 1))
            last_h = screen_h_down

    def draw_raycast(self):
        debug.debug_first_ray = False
        for ray_number in range(NUM_RAYS):
            cur_angle = self.player.left_angle - ray_number * DELTA_ANGLE
            ray = Ray(self.player, cur_angle)
            min_dist = None
            nearest_intersection = None
            list_intersections = []
            for build in self.floor.build_list:
                for wall in build.wall_list:
                    intersection = ray.find_intersection(wall)
                    if intersection:
                        dist = math.hypot(intersection.x - self.player.x,
                                          intersection.y - self.player.y)
                        if DRAW_ALL_WALS:
                            list_intersections.append((dist, intersection))
                        if min_dist:
                            if dist < min_dist:
                                min_dist = dist
                                nearest_intersection = intersection
                        else:
                            min_dist = dist
                            nearest_intersection = intersection

            if min_dist and nearest_intersection:
                if DRAW_ALL_WALS:
                    list_intersections = sorted(list_intersections, key=lambda x: x[0],
                                                reverse=True)
                    for dist, intersection in list_intersections:
                        draw_column(dist=dist, intersection=intersection,
                                    player=self.player, cur_angle=cur_angle, sc=self.sc,
                                    ray_number=ray_number)
                else:
                    draw_column(dist=min_dist, intersection=nearest_intersection,
                                player=self.player, cur_angle=cur_angle, sc=self.sc,
                                ray_number=ray_number)

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

        # игрок
        screen_player_crd = convert_crds_to_scren(*self.player.pos, self.player, self.minimap)
        pygame.draw.circle(self.minimap.sc, (100, 200, 0), screen_player_crd, 7)
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
        for i in range(NUM_RAYS):
            angle = self.player.left_angle - i * DELTA_ANGLE
            pygame.draw.line(self.minimap.sc, (100, 100, 0), screen_player_crd,
                             convert_crds_to_scren(
                                 self.player.x + math.cos(math.radians(angle)) * MAX_DIST_RAY,
                                 self.player.y + math.sin(math.radians(angle)) * MAX_DIST_RAY,
                                 self.player, self.minimap))
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
            color = pygame.Color('blue')
        elif fps < 60:
            color = pygame.Color('cyan')
        elif fps >= 60:
            color = pygame.Color('green')

        render = self.font_fps.render(str(fps), False, color)
        self.sc.blit(render, FPS_POS)

    def draw_info(self):
        text_list = [
            f'add_speed = {self.player.add_speed}',
        ]
        for i in range(len(text_list)):
            render = self.font_info.render(text_list[i], False, (0, 200, 200))
            self.sc.blit(render, (0, 20 + 20 * i))


def convert_crds_to_scren(x, y, player, minimap):
    return minimap.WIDTH / 2 + (x - player.x) * minimap.SCALE, minimap.HEIGHT / 2 - (
            y - player.y) * minimap.SCALE


def find_angle_point(player, point):
    dist = find_dist(player, point)
    if dist == 0:
        dist = ALMOST_ZERO
    sin_angle = (point.y - player.y) / dist
    cos_angle = (point.x - player.x) / dist
    angle = math.degrees(math.acos(cos_angle))
    if sin_angle < 0:
        angle = 360 - angle
    return angle


def find_dist(point1, point2):
    return math.hypot(point1.x - point2.x, point1.y - point2.y)


def find_color(dist, hue=0, value=0):
    color = pygame.Color(0)
    smooth = 10
    brightness = 100 - 100 * smooth / (dist + smooth)
    try:
        color.hsva = (hue, value, brightness)
    except Exception:
        print(brightness)

    return color


def correcting_angle(angle):
    """эта функция нужна, чтобы значения угла были не от 0 до 360, а в нужном диапазоне
    (включая отрицательные значения и не включая большие положительные"""
    n = 180
    if angle > n:
        angle -= 360
    elif angle < -n:
        angle += 360

    return angle


def find_screen_h_and_h_down(dist, intersection, player, sc):
    # находим углы ключевых точек
    angle_top_point = find_angle_point(
        Point(0, player.h_down + player.h),
        Point(dist, intersection.h_down + intersection.h))

    angle_bott_point = -360 + find_angle_point(
        Point(0, player.h_down + player.h),
        Point(dist, intersection.h_down))

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


def draw_column(dist, intersection, player, cur_angle, sc, ray_number):
    # убираем эффект рыбьего глаза
    if not FISH_EYE:
        dist *= math.cos(math.radians(player.angle_w - cur_angle))

    # находим экранную высоту стены и ее экранное расстояние над землей
    screen_h, screen_h_down = find_screen_h_and_h_down(dist, intersection, player, sc)

    # определяем цвет в зависимости от расстояния
    color = find_color(dist)

    # отрисовка
    pygame.draw.rect(sc, color, (
        ray_number / SCALE_N_RAYS, HEIGHT - screen_h_down - screen_h, WIDTH / NUM_RAYS,
        screen_h))

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
