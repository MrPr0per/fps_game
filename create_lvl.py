import pygame
import math
from floor import load_floor


def convert_crds_to_scren(x, y):
    return CENTER_W + x * SCALE, CENTER_H - y * SCALE,


def draw_grid(line_scale):
    if line_scale < 20:
        line_scale *= 5
    if line_scale > HEIGHT / 2:
        line_scale /= 5
    i = CENTER_W % line_scale
    while i < WIDTH:
        pygame.draw.line(sc, (50, 50, 50), (i, 0), (i, HEIGHT))
        i += line_scale
    i = CENTER_H % line_scale
    while i < WIDTH:
        pygame.draw.line(sc, (50, 50, 50), (0, i), (WIDTH, i))
        i += line_scale

    pygame.draw.line(sc, (100, 100, 100), (CENTER_W, 0), (CENTER_W, HEIGHT))
    pygame.draw.line(sc, (100, 100, 100), (0, CENTER_H), (WIDTH, CENTER_H))


def draw_points():
    for b in build_list:
        # print(b)
        for p in b[1]:
            # print(p)
            pygame.draw.circle(sc, (200, 200, 200), convert_crds_to_scren(p[0], p[1]), 5)
        if len(b[1]) >= 2:
            # print(b)
            pygame.draw.lines(sc, (200, 200, 200), b[0],
                              list(map(lambda x: convert_crds_to_scren(x[0], x[1]), b[1])))


def event_processing(CENTER_W, CENTER_H, SCALE, line_scale):
    # TODO: добавить возможность создавать столбы разной высоты
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if event.key == pygame.K_TAB:
                build_list.append([False, []])

            if event.key == pygame.K_SPACE:
                point_sc = pygame.mouse.get_pos()
                x = -1 * (CENTER_W - point_sc[0]) / SCALE
                y = (CENTER_H - point_sc[1]) / SCALE
                # print(x)
                # print(abs(x - round(x)))
                if abs(x - round(x)) < 0.2:
                    x = round(x)
                # print(x)
                if abs(y - round(y)) < 0.2:
                    y = round(y)

                # print()
                point_crd = (x, y)
                build_list[-1][1].append(point_crd)

            if event.key == pygame.K_DELETE:
                if len(build_list[-1][1]) != 0:
                    del build_list[-1][1][-1]
                else:
                    if len(build_list) > 1:
                        del build_list[-1]
            if event.key == pygame.K_c:
                build_list[-1][0] = not build_list[-1][0]

            if event.key == pygame.K_KP_ENTER:
                print('floor = Floor(build_list=[')
                for build in build_list:
                    print('\tBuild(column_list=[')
                    for point in build[1]:
                        print(f'\t\tColumn{point},')
                    print(f'\t], closed={build[0]}),')
                print('])')

        if event.type == pygame.MOUSEBUTTONDOWN:
            no_move_point_sc = pygame.mouse.get_pos()
            no_move_point_crd = [-1 * (CENTER_W - no_move_point_sc[0]) / SCALE,
                                 (CENTER_H - no_move_point_sc[1]) / SCALE]

            scale_speed = 1.1
            if event.button == 4:
                SCALE *= scale_speed
                line_scale *= scale_speed
            if event.button == 5:
                SCALE /= scale_speed
                line_scale /= scale_speed

            no_move_point_crd_2 = [-1 * (CENTER_W - no_move_point_sc[0]) / SCALE,
                                   (CENTER_H - no_move_point_sc[1]) / SCALE]
            CENTER_W = CENTER_W - (no_move_point_crd[0] - no_move_point_crd_2[0]) * SCALE
            CENTER_H = CENTER_H + (no_move_point_crd[1] - no_move_point_crd_2[1]) * SCALE
    delta_x, delta_y = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        CENTER_W += delta_x
        CENTER_H += delta_y

    return CENTER_W, CENTER_H, SCALE, line_scale


def convert_floor(n):
    build_list_creator = []
    floor = load_floor(n)
    for build in floor.build_list:
        build_creator = [build.closed, []]
        for column in build.column_list:
            build_creator[1].append((column.x, column.y))
        build_list_creator.append(build_creator)
    return build_list_creator

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('aaaaaaaaaaa')
    WIDTH, HEIGHT = 1280, 720
    CENTER_W = WIDTH / 2
    CENTER_H = HEIGHT / 2
    sc = pygame.display.set_mode((WIDTH, HEIGHT))

    fps = 120
    clock = pygame.time.Clock()

    SCALE = 100
    line_scale = SCALE

    # build_list = [[False, []]]
    build_list = convert_floor(6)

    while True:
        CENTER_W, CENTER_H, SCALE, line_scale = event_processing(CENTER_W, CENTER_H, SCALE,
                                                                 line_scale)

        sc.fill(pygame.Color('black'))
        draw_grid(line_scale)
        draw_points()

        clock.tick(fps)
        pygame.display.flip()
