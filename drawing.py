import pygame
import debug
from settings import *
from floor import Ray
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
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def clear_screen(self):
        self.sc.fill((0, 0, 0))

    def draw_raycast(self):
        for i in range(N_RAYS):
            angle = self.player.left_angle - i * DELTA_ANGLE
            if debug.DEBUG:
                print('debug')
                debug.DEBUG = False
            ray = Ray(self.player, angle)
            min_dist = None
            height = None
            for build in self.floor.build_list:
                for wall in build.wall_list:
                    crd_intersection = ray.find_intersection(wall)
                    if crd_intersection:
                        dist = math.hypot(crd_intersection.x - self.player.x,
                                          crd_intersection.y - self.player.y)
                        if min_dist is None:
                            min_dist = dist
                            height = crd_intersection.h
                        elif dist < min_dist:
                            min_dist = dist
                            height = crd_intersection.h
            if min_dist and height:
                min_dist *= math.cos(math.radians(self.player.angle_w - angle))
                proection_screen = math.tan(
                    math.radians(self.player.angle_h + FOW_H / 2)) * min_dist + math.tan(
                    math.radians(-self.player.angle_h + FOW_H / 2)) * min_dist
                visual_height = HEIGHT * height / proection_screen
                color = pygame.Color(0)
                smooth = 5
                brightness = 100 * smooth / (min_dist + smooth)
                try:
                    color.hsva = (0, 0, brightness)
                except Exception:
                    print(brightness)

                self.sc.fill(color, (i/SCALE_N_RAYS, HALF_HEIGHT - visual_height / 2, WIDTH/N_RAYS, visual_height))

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

        pygame.draw.line(self.minimap.sc, (100, 100, 100), (self.minimap.CENTER_W, 0), (self.minimap.CENTER_W, self.minimap.HEIGHT))
        pygame.draw.line(self.minimap.sc, (100, 100, 100), (0, self.minimap.CENTER_H), (self.minimap.WIDTH, self.minimap.CENTER_H))

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
        for i in range(N_RAYS):
            angle = self.player.left_angle - i * DELTA_ANGLE
            pygame.draw.line(self.minimap.sc, (100, 100, 0), screen_player_crd,
                             convert_crds_to_scren(
                                 self.player.x + math.cos(math.radians(angle)) * MAX_DIST_RAY,
                                 self.player.y + math.sin(math.radians(angle)) * MAX_DIST_RAY, self.player, self.minimap))
        # карта
        for build in self.floor.build_list:
            for point in build.column_list:
                x, y = convert_crds_to_scren(*point.pos, self.player, self.minimap)
                pygame.draw.circle(self.minimap.sc, (200, 200, 200), (x, y), 3)
            points = list(
                map(lambda a: convert_crds_to_scren(*a.pos, self.player, self.minimap), build.column_list))
            # points = list(map(lambda a: (a.x, a.y), build.point_list))
            pygame.draw.lines(self.minimap.sc, (200, 200, 200), build.closed, points)

        pygame.draw.rect(self.minimap.sc, (255, 255, 255), (0, 0, self.minimap.WIDTH, self.minimap.HEIGHT), 2)

        self.sc.blit(self.minimap.sc, self.minimap.POS)

    def draw_fps(self):
        fps = int(self.clock.get_fps())
        if fps < 30:
            color = pygame.Color('blue')
        elif fps < 60:
            color = pygame.Color('cyan')
        elif fps >= 60:
            color = pygame.Color('green')

        render = self.font.render(str(fps), False, color)
        self.sc.blit(render, FPS_POS)


def convert_crds_to_scren(x, y, player, minimap):
    return minimap.WIDTH / 2 + (x - player.x) * minimap.SCALE, minimap.HEIGHT / 2 - (
                y - player.y) * minimap.SCALE

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
