import math
from settings import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)

    def get_pos(self):
        return self.x, self.y

    def __str__(self):
        return f'{self.x};{self.y}'

    def __repr__(self):
        return self.__str__()


class Column(Point):
    def __init__(self, x, y, h=3, h_down=0):
        self.h = h
        self.h_down = h_down
        super().__init__(x, y)


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
            k1 = 10 ** -6
        x = (b2 - b1) / (k1 - k2)
        left_border1, right_border1 = self.borders
        left_border2, right_border2 = other.borders
        if (left_border1 <= x <= right_border1) and (left_border2 <= x <= right_border2):
            y = k1 * x + b1
            return Point(x=x, y=y)
        else:
            return None


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
            dist_from_beginning = math.hypot(other.column1.x - x, other.column2.y - y)
        if type(other) == Wall:
            h = other.vertical_k * dist_from_beginning + other.vertical_b
            h_down = other.vertical_k_down * dist_from_beginning + other.vertical_b_down
            return Column(x=x, y=y, h=h, h_down=h_down)
        elif type(other) == Line_segment:
            return Point(x=x, y=y)
        elif type(other) == Line:
            return Point(x=x, y=y)




class Build:
    def __init__(self, column_list, closed=False):
        self.column_list = column_list
        self.closed = closed
        wall_list = []
        for i in range(len(column_list) - 1):
            p1, p2 = column_list[i], column_list[i + 1]
            wall_list.append(Wall(p1, p2))
        if closed and len(column_list) > 2:
            p1, p2 = column_list[-1], column_list[0]
            wall_list.append(Wall(p1, p2))
        self.wall_list = wall_list


class Floor:
    def __init__(self, build_list):
        self.build_list = build_list


def load_floor(num_floor):
    floor = None
    if num_floor == 1:
        point_list = [
            Point(-1, 0),
            Point(1, 0),
        ]
        build = Build(column_list=point_list, closed=False)
        floor = Floor(build_list=[build])
    if num_floor == 2:
        floor = Floor(build_list=[
            Build(column_list=[
                Point(0, 0),
                Point(1, 0),
                Point(1, 1),
                Point(0, 1),
            ], closed=True),
            Build(column_list=[
                Point(2, 0),
                Point(4, 0),
                Point(3, -2),
            ], closed=True),
            Build(column_list=[
                Point(5, 1),
                Point(5, 0),
                Point(10, 0),
                Point(10, 5),
                Point(5, 5),
                Point(5, 4),
            ], closed=False),
        ])
    if num_floor == 3:
        build_list = []
        for i in range(-20, 20):
            i *= 4
            build = Build(column_list=[
                Point(i, 0),
                Point(i + 2, 0),
                Point(i + 2, 2),
                Point(i, 2),
            ], closed=True)
            build_list.append(build)
        floor = Floor(build_list)
    if num_floor == 4:
        floor = Floor(build_list=[
            Build(column_list=[
                Point(-1, 0),
                Point(-1, -1),
                Point(1, -1),
                Point(1, 0),
                Point(2, 0),
                Point(4, 1),
                Point(5, 2),
                Point(6, 4),
                Point(6, 6),
                Point(8.8747526, 6),
                Point(9, 8),
                Point(2, 8),
                Point(2, 6),
                Point(4.8967929, 6),
                Point(5, 4),
                Point(4, 2),
                Point(2, 1),
                Point(1, 1),
                Point(1, 2),
                Point(-1, 2),
                Point(-1, 1),
            ], closed=False),
            Build(column_list=[
                Point(-1, 1),
                Point(-2, 1),
                Point(-2, 3),
                Point(-1, 3),
                Point(-1, 5),
                Point(-3, 5),
                Point(-3, 3),
                Point(-2.5598684000000023, 3),
                Point(-2.543763300000002, 1),
                Point(-2.5598684000000023, 0),
                Point(-1, 0),
            ], closed=False),
        ])
    if num_floor == 5:
        floor = Floor(build_list=[
            Build(column_list=[
                Column(-1, 3),
                Column(-4, 3),
                Column(-4, -3.158609382000001),
                Column(4.871746100000002, -3),
                Column(5, 3),
                Column(1, 3),
                Column(1, 6),
                Column(4.554145636501002, 8.180376635282004),
                Column(4.683832759506002, 10),
                Column(6.266015660167003, 10),
            ], closed=False),
            Build(column_list=[
                Column(6.381598826237731, 13.152590148725595),
                Column(4.759031355472972, 13.152590148725595),
                Column(4.275713385457938, 14.809680331634285),
                Column(0.3056014889058689, 18.33099697031525),
                Column(-5.252555166267028, 15.569179998800767),
                Column(-4.803759908395924, 13),
                Column(-7.116781622039304, 13),
            ], closed=False),
            Build(column_list=[
                Column(-7, 10),
                Column(-4.631146347676269, 10.149114192203594),
                Column(-4.424010074812683, 7.594433493552698),
                Column(-1, 6),
                Column(-1, 3),
            ], closed=False),
            Build(column_list=[
                Column(-7, 10),
                Column(-9.119098926387304, 9.251523676461387),
                Column(-11, 7.352774508545181),
                Column(-11.777347761469994, 5.454025340628974),
                Column(-12.157097595053235, 3.4862307484249047),
                Column(-12.32971115577289, 1.65652700479656),
                Column(-12.536847428636477, 0.10300495831966333),
            ], closed=False),
            Build(column_list=[
                Column(-7.254872470615028, 13),
                Column(-9.153621638531234, 12.876408451574147),
                Column(-11.501166064318545, 12.32404505727125),
                Column(-13, 11),
                Column(-14.124892187257304, 9),
                Column(-15.229618975863097, 5.730207037780422),
                Column(-15.471277960870614, 4),
                Column(-15.712936945878132, 1.4839134440769048),
                Column(-15.747459658022063, 0),
                Column(-18, 0),
                Column(-21.581798010346407, -7.1812873040497855),
                Column(-14.159414899401234, -13.36085277781344),
                Column(-6.806077212743925, -7.215810016193716),
                Column(-10.154780290705235, 0),
                Column(-12.571370140780408, 0.10300495831966333),
            ], closed=False),
            Build(column_list=[
                Column(-17, -3.5909252410809573),
                Column(-14.193937611545167, -10.737126654874682),
                Column(-11.777347761469994, -3.3147435439295094),
                Column(-18, -7.595559849776958),
                Column(-10.6726209728642, -8),
            ], closed=True),
            Build(column_list=[
                Column(6.312553401949869, 13.187112860869526),
                Column(6.485166962669524, 19),
                Column(4.862599491904765, 19.159542061769596),
            ], closed=False),
            Build(column_list=[
                Column(6.2435079776620075, 10),
                Column(6.6232578112452485, -3),
                Column(16.117003650826284, -2.4861984524751644),
                Column(15.461072120091593, 21.852313608996216),
                Column(4.586417794753317, 21.852313608996216),
                Column(2.7567140511249724, 22.473722427586974),
                Column(3, 23.751062776912423),
                Column(4.862599491904765, 24),
                Column(6.105417129086283, 23.854630913344216),
            ], closed=False),
            Build(column_list=[
                Column(4.862599491904765, 19.228587486057457),
                Column(0.4782150496255241, 20.64401868395863),
                Column(-0.3158073296848897, 23.57844921619277),
                Column(0, 26),
                Column(3.4816910061475244, 26.65097059700263),
                Column(7.279189341979938, 26.65097059700263),
                Column(7.451802902699593, 28.169969931335597),
                Column(15.633685680811249, 28.239015355623458),
                Column(15.115844998652284, 22.818949549026286),
                Column(6.347076114093801, 23),
                Column(6.105417129086283, 23.854630913344216),
            ], closed=False),
            Build(column_list=[
                Column(8.107734433434283, 24.372471595503182),
                Column(8.832711388456834, 27),
                Column(9.108893085608283, 24.510562444078907),
            ], closed=False),
            Build(column_list=[
                Column(10, 26.443834324139043),
                Column(10, 24.786744141230354),
                Column(10.69693784422911, 24.6141305805107),
                Column(11.421914799251663, 25.166493974813594),
                Column(11.249301238532007, 27.34142483988125),
                Column(10.524324283509456, 27.30690212773732),
            ], closed=True),
            Build(column_list=[
                Column(12.595687012145317, 24.510562444078907),
                Column(13.389709391455732, 27.410470264169113),
                Column(14, 24.545085156222836),
            ], closed=False),
            Build(column_list=[
                Column(15.392026695803732, 21.817790896852284),
                Column(11.66357378425918, 19.711905456072493),
                Column(15.599162968667319, 19),
                Column(12.69925514857711, 16.70842949955049),
                Column(15.737253817243042, 16.225111529535457),
                Column(12.733777860721041, 13.566862694452768),
                Column(15.875344665818766, 12.738317602998423),
                Column(12.492118875713524, 10.35625046506718),
                Column(15.771776529386972, 9.35509181289318),
                Column(12.630209724289248, 7.421819932833043),
                Column(16, 6.2135250077954565),
                Column(13, 4.521912112742836),
                Column(16.220571787258077, 3.31361718770525),
                Column(13, 1.760095141228353),
                Column(16.427708060121663, 0.5518002161907668),
                Column(13, 0.20657309475145644),
                Column(16.25509449940201, -2.3826303160433713),
                Column(13.320663967167869, -1),
                Column(13.389709391455732, -2.6242893010508883),
                Column(12.250459890706008, -1.139812678861854),
                Column(11.69809649640311, -2.5207211646190952),
                Column(11, -1.208858103149716),
                Column(9.626733767767249, -2.6933347253387505),
                Column(9.177938509896146, -0.8291082695664747),
                Column(7.1065757812602826, -2.865948286058406),
                Column(8.314870706297869, 0.7934592011982841),
                Column(6.519689674813455, 1.65652700479656),
                Column(8.3493934184418, 4.418343976311043),
                Column(6.554212386957387, 5.557593477060767),
                Column(8, 7.387297220689112),
                Column(6.347076114093801, 7.7670470542723535),
            ], closed=False),
        ])
    if num_floor == 6:
        floor = Floor(build_list=[
            Build(column_list=[
                Column(math.sin(math.radians(i)) * 10, math.cos(math.radians(i)) * 10) for i in range(0, 360, 10)
            ], closed=False),
        ])
    if num_floor == 7:
        floor = Floor(build_list=[
            Build(column_list=[
                Column(i, 0, i, 0),
                Column(i + 1, 0, i, 0),
            ], closed=False)
            for i in range(2,100)
        ])
    return floor
