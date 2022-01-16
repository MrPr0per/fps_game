import math

from settings import *
from resourses import *
import debug


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)

    def get_pos(self):
        return self.x, self.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()


class Column(Point):
    def __init__(self, x, y, h=3, h_down=0):
        self.h = h
        self.h_down = h_down
        super().__init__(x, y)

    def __str__(self):
        return f'(x={self.x}, y={self.y}, h={self.h}, h_down{self.h_down})'

    def __repr__(self):
        return self.__str__()


class Intersection:
    def __init__(self, column, offset, dist, texture_name=TEXT_MISSING):
        self.column = column
        self.offset = offset
        self.texture_name = texture_name
        self.dist = dist


class Line_segment:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

        x1, y1 = point1.get_pos()
        x2, y2 = point2.get_pos()
        if x1 == x2:
            x2 += 10 ** -6
        self.k = (y2 - y1) / (x2 - x1)
        self.b = y1 - self.k * x1
        self.left_border = min(x1, x2)
        self.right_border = max(x1, x2)
        self.borders = (self.left_border, self.right_border)

    def find_intersection(self, other):
        def find_x(k1, b1, k2, b2):
            if k1 - k2 == 0:
                k1 = ALMOST_ZERO
            x = (b2 - b1) / (k1 - k2)
            return x

        k1, b1 = self.k, self.b
        k2, b2 = other.k, other.b

        x = find_x(k1, b1, k2, b2)

        if type(other) != Line:
            left_border1, right_border1 = self.borders
            left_border2, right_border2 = other.borders
            if not ((left_border1 <= x <= right_border1) and (left_border2 <= x <= right_border2)):
                return None

        y = k1 * x + b1
        if type(other) == Wall:
            dist_from_beginning = math.hypot(other.column1.x - x, other.column1.y - y)
            h = other.vertical_k * dist_from_beginning + other.vertical_b
            h_down = other.vertical_k_down * dist_from_beginning + other.vertical_b_down
            dist_to_intersection = math.hypot(x - self.point1.x, y - self.point1.y)
            column = Column(x=x, y=y, h=h, h_down=h_down)
            return Intersection(column, dist_from_beginning, dist_to_intersection)
        elif type(other) == Line_segment:
            return Point(x=x, y=y)
        elif type(other) == Line:
            return Point(x=x, y=y)


class Line:
    def __init__(self, point1, point2):
        x1, y1 = point1.get_pos()
        x2, y2 = point2.get_pos()
        if x1 == x2:
            x2 += 10 ** -6
        self.k = (y2 - y1) / (x2 - x1)
        self.b = y1 - self.k * x1


class Wall(Line_segment):
    def __init__(self, column1, column2):
        self.column1 = column1
        self.column2 = column2
        d = math.hypot(column1.x - column2.x, column1.y - column2.y)
        h1 = column1.h
        h2 = column2.h
        self.vertical_b = h1
        if d == 0:
            d = ALMOST_ZERO
        self.vertical_k = (h2 - h1) / d
        h1_down = column1.h_down
        h2_down = column2.h_down
        self.vertical_b_down = h1_down
        self.vertical_k_down = (h2_down - h1_down) / d
        super().__init__(Point(*column1.get_pos()), Point(*column2.get_pos()))


class Ray(Line_segment):
    def __init__(self, point1, angle):
        x2 = point1.x + math.cos(math.radians(angle)) * MAX_DIST_RAY
        y2 = point1.y + math.sin(math.radians(angle)) * MAX_DIST_RAY
        point2 = Point(x2, y2)
        super().__init__(point1, point2)


class Build:
    def __init__(self, column_list, is_closed=False, texture_name=TEXT_MISSING):
        self.texture_name = texture_name
        self.column_list = column_list
        self.is_closed = is_closed
        wall_list = []
        for i in range(len(column_list) - 1):
            p1, p2 = column_list[i], column_list[i + 1]
            wall_list.append(Wall(p1, p2))
        if is_closed and len(column_list) > 2:
            p1, p2 = column_list[-1], column_list[0]
            wall_list.append(Wall(p1, p2))
        self.wall_list = wall_list

    def update_walls(self):
        wall_list = []
        for i in range(len(self.column_list) - 1):
            p1, p2 = self.column_list[i], self.column_list[i + 1]
            wall_list.append(Wall(p1, p2))
        if self.is_closed and len(self.column_list) > 2:
            p1, p2 = self.column_list[-1], self.column_list[0]
            wall_list.append(Wall(p1, p2))
        self.wall_list = wall_list


class Floor:
    def __init__(self, build_list, object_list=[], ground_color=(110, 175, 219), sky_text_num=0):
        self.build_list = build_list
        self.object_list = object_list
        self.ground_color = ground_color
        self.sky_text_num = sky_text_num


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


def is_the_point_in_the_field_of_view(viewer, viewer_angle, field_of_view, point):
    angle = find_angle_point(viewer, point)
    delta_angle = min(
        max(angle, viewer_angle) - min(angle, viewer_angle),
        360 - (max(angle, viewer_angle) - min(angle, viewer_angle)),
    )
    if delta_angle <= field_of_view / 2:
        return True
    else:
        return False


def is_there_a_dot_behind_the_wall(point1, point2, build_list):
    view_vector = Line_segment(point1, point2)
    for build in build_list:
        for wall in build.wall_list:
            intersection = view_vector.find_intersection(wall)
            if intersection:
                return True
    return False
