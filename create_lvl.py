import pygame
import math
import random
from geometric_classes import Floor, Build, Column, Point
from resourses import *
from enemy import *
from drawing import find_angle_point
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
    for build in editable_floor.build_list:
        for column in build.column_list:
            pygame.draw.circle(sc, (200, 200, 200), convert_crds_to_scren(column.x, column.y), 5)
        if len(build.column_list) >= 2:
            pygame.draw.lines(sc, (200, 200, 200), build.is_closed,
                              list(map(lambda a: convert_crds_to_scren(a.x, a.y),
                                       build.column_list)))

    if ENABLE_HEIGHTS:
        for build in editable_floor.build_list:
            i = 0
            for wall in build.wall_list:
                i += 1
                color = tuple(0.5 * 255 * i / len(build.wall_list) + 0.25 * 255 for j in range(3))
                # print(color)
                pygame.draw.polygon(sc, color, (
                    convert_crds_to_scren(wall.column1.x + wall.column1.h_down,
                                          wall.column1.y + wall.column1.h_down),
                    convert_crds_to_scren(wall.column2.x + wall.column2.h_down,
                                          wall.column2.y + wall.column2.h_down),
                    convert_crds_to_scren(wall.column2.x + wall.column2.h_down + wall.column2.h,
                                          wall.column2.y + wall.column2.h_down + wall.column2.h),
                    convert_crds_to_scren(wall.column1.x + wall.column1.h_down + wall.column1.h,
                                          wall.column1.y + wall.column1.h_down + wall.column1.h),
                ))


def draw_objects():
    for obj in editable_floor.object_list:
        obj_screen_crd = convert_crds_to_scren(*obj.pos)
        if isinstance(obj, Enemy):
            color = (240, 0, 0)
            if obj.angle:
                pygame.draw.line(sc, color, obj_screen_crd,
                                 convert_crds_to_scren(
                                     obj.x + math.cos(math.radians(
                                         obj.angle)) * obj.radius / COLLIDE_SCALE * 1.5,
                                     obj.y + math.sin(math.radians(
                                         obj.angle)) * obj.radius / COLLIDE_SCALE * 1.5), 3)
        else:
            color = (150, 150, 0)
        pygame.draw.circle(sc, color, obj_screen_crd,
                           obj.w / 2 * SCALE)

        image = pygame.transform.scale(obj.image, (obj.w * SCALE * 0.75, obj.h * SCALE * 0.75))
        obj_screen_crd = convert_crds_to_scren(*obj.pos)
        obj_screen_crd = (obj_screen_crd[0] - image.get_width() / 2,
                          obj_screen_crd[1] - image.get_height() / 2)
        sc.blit(image, obj_screen_crd)


def draw_params():
    groups = {
        'important_text': {
            'text_list': [
                'СТАВИТЬ СТЕНЫ ПО ЧАСОВОЙ СТРЕЛКЕ ДЛЯ КОРРЕКТНОГО ОТОБРАЖЕНИЯ ТЕКСТУР'
            ],
            'color': (255, 100, 100),
        },

        'variables': {
            'text_list': [
                f'h       {H}',
                f'h_down  {H_DOWN}',
                f'brush   {brush}',
            ],
            'color': (0, 200, 200),
        },

        'keys': {
            'text_list': [
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
                's - скалировать все точки от центра',
                'h - настроить высоты',
                'l - включить отображение высот',
                'b - сменить кисть',
            ],
            'color': (100, 200, 0),
        },
    }

    group_iter = 0
    line_iter = 0
    margin_top = 10
    mergin_left = 10
    for group in groups.keys():
        color = groups[group]['color']
        for line in groups[group]['text_list']:
            render = font.render(line, False, color)
            sc.blit(render, (mergin_left, 20 * (line_iter + group_iter) + margin_top))
            line_iter += 1
        group_iter += 1

    scale = 70
    margin = 15
    pygame.draw.line(sc, (100, 100, 0), (WIDTH - margin * 2, HEIGHT - margin),
                     (WIDTH - margin * 2, HEIGHT - margin - 1.8 * scale), 3)
    if len(editable_floor.build_list[-1].column_list) != 0:
        p_h = editable_floor.build_list[-1].column_list[-1].h
        p_h_down = editable_floor.build_list[-1].column_list[-1].h_down
        pygame.draw.line(sc, (200, 200, 200),
                         (WIDTH - margin * 3, HEIGHT - margin - p_h_down * scale),
                         (WIDTH - margin * 3, HEIGHT - margin - (p_h_down + p_h) * scale), 3)
    pygame.draw.line(sc, (100, 50, 100), (WIDTH - margin, HEIGHT - margin),
                     (WIDTH - margin, HEIGHT - margin - H_DOWN * scale), 3)
    pygame.draw.line(sc, (200, 200, 100), (WIDTH - margin, HEIGHT - margin - H_DOWN * scale),
                     (WIDTH - margin, HEIGHT - margin - (H_DOWN + H) * scale), 3)


def event_processing(CENTER_W, CENTER_H, SCALE, line_scale, H, H_DOWN, ENABLE_HEIGHTS, brush,
                     NEED_SECOND_POINT):
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
                editable_floor.build_list.append(Build([], False))

            if event.key == pygame.K_SPACE:
                point_sc = pygame.mouse.get_pos()
                x = -1 * (CENTER_W - point_sc[0]) / SCALE
                y = (CENTER_H - point_sc[1]) / SCALE

                if brush == COLUMN:
                    if abs(x - round(x)) < 0.3:
                        x = round(x)
                    if abs(y - round(y)) < 0.3:
                        y = round(y)
                    editable_floor.build_list[-1].column_list.append(Column(x, y, H, H_DOWN))
                    editable_floor.build_list[-1].update_walls()
                elif brush in list(objects_sprites[ENEMIES].keys()):
                    if not NEED_SECOND_POINT:
                        NEED_SECOND_POINT = True
                        if brush == TOFLUND:
                            editable_floor.object_list.append(Toflund(x, y, None))
                        if brush == BAGGEBO:
                            editable_floor.object_list.append(Baggebo(x, y, None))
                    elif NEED_SECOND_POINT:
                        NEED_SECOND_POINT = False
                        angle = find_angle_point(editable_floor.object_list[-1], Point(x, y))
                        editable_floor.object_list[-1].set_angle(angle)

            if event.key == pygame.K_DELETE:
                if brush == COLUMN:
                    if len(editable_floor.build_list[-1].column_list) != 0:
                        del editable_floor.build_list[-1].column_list[-1]
                    else:
                        if len(editable_floor.build_list) > 1:
                            del editable_floor.build_list[-1]
                    editable_floor.build_list[-1].update_walls()
                elif brush in list(objects_sprites[ENEMIES].keys()):
                    del editable_floor.object_list[-1]

            if event.key == pygame.K_c:
                editable_floor.build_list[-1].is_closed = not editable_floor.build_list[
                    -1].is_closed
                editable_floor.build_list[-1].update_walls()

            if event.key == pygame.K_KP_ENTER:
                print()
                print('floor = Floor(build_list=[')
                for build in editable_floor.build_list:
                    print('\tBuild(column_list=[')
                    for column in build.column_list:
                        print(
                            f'\t\tColumn{(round(column.x, 2), round(column.y, 2), round(column.h, 2), round(column.h_down, 2))},')
                    print(f'\t], is_closed={build.is_closed}, texture_name={build.texture_name}),')
                print('], object_list=[')
                for obj in editable_floor.object_list:
                    # type() возвращает строку типа <class '__main__.Aboba'>
                    # эти 2 строки ниже вытаскивают само название класса
                    type_obj = str(type(obj))
                    type_obj = type_obj[type_obj.rfind('.') + 1:type_obj.rfind('\'')]
                    print(f'\t{type_obj}(x={round(obj.x, 2)}, y={round(obj.y, 2)}, angle={round(obj.angle) % 360}),')
                print('])')

                # ], is_closed=False, texture_name=TEXT_KILL),
                #             # Build(column_list=[
                #             #     Column(0, 10, 2, 0),
                #             #     Column(1.9, 10, 2, 0),
                #             # ], is_closed=False, texture_name=TEXT_GRADIENT),
                #         ], object_list=[
                #             Object(0, 18, 1, 0.5),
                #             Baggebo(x=0, y=13, angle=270),
                #
                #         ])

            if event.key == pygame.K_m:
                build_list = editable_floor.build_list.copy()
                for build in build_list:
                    editable_floor.build_list.append(Build([], build.is_closed))
                    for c in build.column_list:
                        editable_floor.build_list[-1].column_list.append(
                            Column(-c.x, c.y, c.h, c.h_down))
                    editable_floor.build_list[-1].update_walls()

            if event.key == pygame.K_s:
                k = eval(input('введите выражение, равное коэффициенту скалирования: '))
                for b in range(len(editable_floor.build_list)):
                    for c in range(len(editable_floor.build_list[b].column_list)):
                        editable_floor.build_list[b].column_list[c].x *= k
                        editable_floor.build_list[b].column_list[c].y *= k
                    editable_floor.build_list[-1].update_walls()

            if event.key == pygame.K_h:
                print('введите, что вы хотите сделать с высотами\n'
                      '(первый знак - оператор, далее выражение)\n'
                      'пример: *3/2+1')
                inp = input()
                oper = inp[0]
                k = eval(inp[1:])
                f = None
                if oper == '*':
                    f = lambda x: x * k
                elif oper == '/':
                    f = lambda x: x / k
                elif oper == '+':
                    f = lambda x: x + k
                elif oper == '-':
                    f = lambda x: x - k

                if f:
                    for b in range(len(editable_floor.build_list)):
                        for c in range(len(editable_floor.build_list[b].column_list)):
                            if oper == '*' or oper == '/':
                                editable_floor.build_list[b].column_list[c].h = f(
                                    editable_floor.build_list[b].column_list[c].h)
                                editable_floor.build_list[b].column_list[c].h_down = f(
                                    editable_floor.build_list[b].column_list[c].h_down)
                            if oper == '+' or oper == '-':
                                editable_floor.build_list[b].column_list[c].h_down = f(
                                    editable_floor.build_list[b].column_list[c].h_down)
                        editable_floor.build_list[-1].update_walls()

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

            if event.key == pygame.K_l:
                ENABLE_HEIGHTS = not ENABLE_HEIGHTS

            if event.key == pygame.K_b:
                print('выберите, что вы хотите ставить сейчас:')
                for i in range(len(brush_list)):
                    print(f'\t{i}.\t{brush_list[i]}')

                answer = int(input())
                if 0 <= answer < len(brush_list):
                    brush = brush_list[answer]

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

    return CENTER_W, CENTER_H, SCALE, line_scale, H, H_DOWN, ENABLE_HEIGHTS, brush, NEED_SECOND_POINT


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
    ENABLE_HEIGHTS = False
    NEED_SECOND_POINT = False

    H = 3
    H_DOWN = 0

    # кисти
    COLUMN = 'COLUMN'
    brush_list = [COLUMN]
    brush_list.extend(list(objects_sprites[ENEMIES].keys()))
    brush = brush_list[0]

    # build_list = [[False, []]]
    editable_floor = Floor(build_list=[Build(column_list=[], is_closed=False)], object_list=[])
    # editable_floor = load_floor(17)

    while True:
        CENTER_W, CENTER_H, \
        SCALE, line_scale, \
        H, H_DOWN, \
        ENABLE_HEIGHTS, \
        brush, \
        NEED_SECOND_POINT = event_processing(CENTER_W, CENTER_H,
                                             SCALE, line_scale,
                                             H, H_DOWN,
                                             ENABLE_HEIGHTS,
                                             brush,
                                             NEED_SECOND_POINT)

        sc.fill(pygame.Color('black'))
        draw_grid(line_scale)
        draw_points()
        draw_objects()
        draw_params()

        clock.tick(fps)
        pygame.display.flip()
