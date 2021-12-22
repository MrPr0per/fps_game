import math
from settings import *
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
        return f'({self.x}, {self.y}, {self.h}, {self.h_down})'

    def __repr__(self):
        return self.__str__()


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
        k1, b1 = self.k, self.b
        k2, b2 = other.k, other.b
        if k1 - k2 == 0:
            k1 = ALMOST_ZERO
        x = (b2 - b1) / (k1 - k2)
        if type(other) != Line:
            left_border1, right_border1 = self.borders
            left_border2, right_border2 = other.borders
            if not ((left_border1 <= x <= right_border1) and (left_border2 <= x <= right_border2)):
                return None
        y = k1 * x + b1
        if type(other) != Line:
            dist_from_beginning = math.hypot(other.column1.x - x, other.column1.y - y)
        if type(other) == Wall:
            h = other.vertical_k * dist_from_beginning + other.vertical_b
            h_down = other.vertical_k_down * dist_from_beginning + other.vertical_b_down
            return Column(x=x, y=y, h=h, h_down=h_down)
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
    def __init__(self, column_list, is_closed=False):
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
    def __init__(self, build_list):
        self.build_list = build_list
