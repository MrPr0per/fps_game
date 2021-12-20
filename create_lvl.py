import pygame
import math
from geometric_classes import Floor, Build, Column
from floors import load_floor
import debug


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
    for build in FLOOR.build_list:
        for column in build.column_list:
            pygame.draw.circle(sc, (200, 200, 200), convert_crds_to_scren(column.x, column.y), 5)
        if len(build.column_list) >= 2:
            pygame.draw.lines(sc, (200, 200, 200), build.is_closed,
                              list(map(lambda a: convert_crds_to_scren(a.x, a.y),
                                       build.column_list)))


def draw_params():
    render = font.render(f'h       {H}', False, (100, 200, 0))
    sc.blit(render, (0, 10))
    render = font.render(f'h_down  {H_DOWN}', False, (100, 200, 0))
    sc.blit(render, (0, 30))

    text_list = [
        'space - поставить точку',
        'tab - создать новую группу точек',
        'с - изменить замкнутость группы',
        'del - удалить последнюю точку',
        'enter (numpad) - вывести уровень',
        '1 - увеличить h',
        '2 - уменьшить h',
        '9 - увеличить h_down и уменьшить h',
        '0 - уменьшить h_down и увеличить h',
        'm - отзеркалить все точки от OY',
    ]
    for i in range(len(text_list)):
        render = font.render(text_list[i], False, (100, 200, 0))
        sc.blit(render, (0, 60 + 20 * i))

    scale = 70
    margin = 15
    pygame.draw.line(sc, (100, 100, 0), (WIDTH - margin * 2, HEIGHT - margin), (WIDTH - margin * 2 , HEIGHT - margin - 1.8 * scale), 3)
    pygame.draw.line(sc, (100, 50, 100), (WIDTH - margin, HEIGHT - margin), (WIDTH - margin, HEIGHT - margin - H_DOWN * scale), 3)
    pygame.draw.line(sc, (200, 200, 100), (WIDTH - margin, HEIGHT - margin - H_DOWN * scale), (WIDTH - margin, HEIGHT - margin - (H_DOWN + H) * scale), 3)


def event_processing(CENTER_W, CENTER_H, SCALE, line_scale, H, H_DOWN):
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
                FLOOR.build_list.append(Build([], False))

            if event.key == pygame.K_SPACE:
                point_sc = pygame.mouse.get_pos()
                x = -1 * (CENTER_W - point_sc[0]) / SCALE
                y = (CENTER_H - point_sc[1]) / SCALE
                if abs(x - round(x)) < 0.2:
                    x = round(x)
                if abs(y - round(y)) < 0.2:
                    y = round(y)

                FLOOR.build_list[-1].column_list.append(Column(x, y, H, H_DOWN))

            if event.key == pygame.K_DELETE:
                if len(FLOOR.build_list[-1].column_list) != 0:
                    del FLOOR.build_list[-1].column_list[-1]
                else:
                    if len(FLOOR.build_list) > 1:
                        del FLOOR.build_list[-1]

            if event.key == pygame.K_c:
                FLOOR.build_list[-1].is_closed = not FLOOR.build_list[-1].is_closed

            if event.key == pygame.K_KP_ENTER:
                print()
                print('floor = Floor(build_list=[')
                for build in FLOOR.build_list:
                    print('\tBuild(column_list=[')
                    for column in build.column_list:
                        print(f'\t\tColumn{column},')
                    print(f'\t], is_closed={build.is_closed}),')
                print('])')

            if event.key == pygame.K_m:
                build_list = FLOOR.build_list.copy()
                for build in build_list:
                    FLOOR.build_list.append(Build([], build.is_closed))
                    for c in build.column_list:
                        FLOOR.build_list[-1].column_list.append(Column(-c.x, c.y, c.h, c.h_down))

            if event.key == pygame.K_1:
                H += 1
            if event.key == pygame.K_2:
                H -= 1
            if event.key == pygame.K_9:
                H_DOWN += 1
                H -= 1
            if event.key == pygame.K_0:
                H_DOWN -= 1
                H += 1

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

    return CENTER_W, CENTER_H, SCALE, line_scale, H, H_DOWN


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('редактор')
    WIDTH, HEIGHT = 1280, 720
    CENTER_W = WIDTH / 2
    CENTER_H = HEIGHT / 2
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    fps = 120
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Lucida Console', 15)

    SCALE = 100
    line_scale = SCALE

    H = 3
    H_DOWN = 0

    # build_list = [[False, []]]
    FLOOR = Floor(build_list=[Build(column_list=[], is_closed=False)])
    # FLOOR = load_floor(6)

    while True:
        CENTER_W, CENTER_H, SCALE, line_scale, H, H_DOWN = event_processing(CENTER_W, CENTER_H,
                                                                            SCALE,
                                                                            line_scale, H, H_DOWN)

        sc.fill(pygame.Color('black'))
        draw_grid(line_scale)
        draw_points()
        draw_params()

        clock.tick(fps)
        pygame.display.flip()
