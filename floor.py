import math
from settings import *


class Point:
    def __init__(self, x, y, h=5, h_down=0):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.h = h
        self.h_down = h_down

    def get_pos(self):
        return self.x, self.y

    def __str__(self):
        return f'{self.x};{self.y}'

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
        # поправить:
        self.h = point1.h


class Ray(Line_segment):
    def __init__(self, point1, angle):
        x2 = point1.x + math.cos(math.radians(angle)) * MAX_DIST_RAY
        y2 = point1.y + math.sin(math.radians(angle)) * MAX_DIST_RAY
        point2 = Point(x2, y2)
        super(Ray, self).__init__(point1, point2)

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
            # TODO: прикрутить опрежеление высоты
            return Point(x=x, y=y)
        else:
            return None


class Build:
    def __init__(self, point_list, closed=False):
        self.point_list = point_list
        self.closed = closed
        line_list = []
        for i in range(len(point_list) - 1):
            p1, p2 = point_list[i], point_list[i + 1]
            line_list.append(Line_segment(p1, p2))
        if closed and len(point_list) > 2:
            p1, p2 = point_list[-1], point_list[0]
            line_list.append(Line_segment(p1, p2))
        self.line_list = line_list


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
        build = Build(point_list=point_list, closed=False)
        floor = Floor(build_list=[build])
    if num_floor == 2:
        floor = Floor(build_list=[
            Build(point_list=[
                Point(0, 0),
                Point(1, 0),
                Point(1, 1),
                Point(0, 1),
            ], closed=True),
            Build(point_list=[
                Point(2, 0),
                Point(4, 0),
                Point(3, -2),
            ], closed=True),
            Build(point_list=[
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
            build = Build(point_list=[
                Point(i, 0),
                Point(i + 2, 0),
                Point(i + 2, 2),
                Point(i, 2),
            ], closed=True)
            build_list.append(build)
        floor = Floor(build_list)
    if num_floor == 4:
        floor = Floor(build_list=[
            Build(point_list=[
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
            Build(point_list=[
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
            Build(point_list=[
                Point(-1, 3),
                Point(-4, 3),
                Point(-4, -3.158609382000001),
                Point(4.871746100000002, -3),
                Point(5, 3),
                Point(1, 3),
                Point(1, 6),
                Point(4.554145636501002, 8.180376635282004),
                Point(4.683832759506002, 10),
                Point(6.266015660167003, 10),
            ], closed=False),
            Build(point_list=[
                Point(6.381598826237731, 13.152590148725595),
                Point(4.759031355472972, 13.152590148725595),
                Point(4.275713385457938, 14.809680331634285),
                Point(0.3056014889058689, 18.33099697031525),
                Point(-5.252555166267028, 15.569179998800767),
                Point(-4.803759908395924, 13),
                Point(-7.116781622039304, 13),
            ], closed=False),
            Build(point_list=[
                Point(-7, 10),
                Point(-4.631146347676269, 10.149114192203594),
                Point(-4.424010074812683, 7.594433493552698),
                Point(-1, 6),
                Point(-1, 3),
            ], closed=False),
            Build(point_list=[
                Point(-7, 10),
                Point(-9.119098926387304, 9.251523676461387),
                Point(-11, 7.352774508545181),
                Point(-11.777347761469994, 5.454025340628974),
                Point(-12.157097595053235, 3.4862307484249047),
                Point(-12.32971115577289, 1.65652700479656),
                Point(-12.536847428636477, 0.10300495831966333),
            ], closed=False),
            Build(point_list=[
                Point(-7.254872470615028, 13),
                Point(-9.153621638531234, 12.876408451574147),
                Point(-11.501166064318545, 12.32404505727125),
                Point(-13, 11),
                Point(-14.124892187257304, 9),
                Point(-15.229618975863097, 5.730207037780422),
                Point(-15.471277960870614, 4),
                Point(-15.712936945878132, 1.4839134440769048),
                Point(-15.747459658022063, 0),
                Point(-18, 0),
                Point(-21.581798010346407, -7.1812873040497855),
                Point(-14.159414899401234, -13.36085277781344),
                Point(-6.806077212743925, -7.215810016193716),
                Point(-10.154780290705235, 0),
                Point(-12.571370140780408, 0.10300495831966333),
            ], closed=False),
            Build(point_list=[
                Point(-17, -3.5909252410809573),
                Point(-14.193937611545167, -10.737126654874682),
                Point(-11.777347761469994, -3.3147435439295094),
                Point(-18, -7.595559849776958),
                Point(-10.6726209728642, -8),
            ], closed=True),
            Build(point_list=[
                Point(6.312553401949869, 13.187112860869526),
                Point(6.485166962669524, 19),
                Point(4.862599491904765, 19.159542061769596),
            ], closed=False),
            Build(point_list=[
                Point(6.2435079776620075, 10),
                Point(6.6232578112452485, -3),
                Point(16.117003650826284, -2.4861984524751644),
                Point(15.461072120091593, 21.852313608996216),
                Point(4.586417794753317, 21.852313608996216),
                Point(2.7567140511249724, 22.473722427586974),
                Point(3, 23.751062776912423),
                Point(4.862599491904765, 24),
                Point(6.105417129086283, 23.854630913344216),
            ], closed=False),
            Build(point_list=[
                Point(4.862599491904765, 19.228587486057457),
                Point(0.4782150496255241, 20.64401868395863),
                Point(-0.3158073296848897, 23.57844921619277),
                Point(0, 26),
                Point(3.4816910061475244, 26.65097059700263),
                Point(7.279189341979938, 26.65097059700263),
                Point(7.451802902699593, 28.169969931335597),
                Point(15.633685680811249, 28.239015355623458),
                Point(15.115844998652284, 22.818949549026286),
                Point(6.347076114093801, 23),
                Point(6.105417129086283, 23.854630913344216),
            ], closed=False),
            Build(point_list=[
                Point(8.107734433434283, 24.372471595503182),
                Point(8.832711388456834, 27),
                Point(9.108893085608283, 24.510562444078907),
            ], closed=False),
            Build(point_list=[
                Point(10, 26.443834324139043),
                Point(10, 24.786744141230354),
                Point(10.69693784422911, 24.6141305805107),
                Point(11.421914799251663, 25.166493974813594),
                Point(11.249301238532007, 27.34142483988125),
                Point(10.524324283509456, 27.30690212773732),
            ], closed=True),
            Build(point_list=[
                Point(12.595687012145317, 24.510562444078907),
                Point(13.389709391455732, 27.410470264169113),
                Point(14, 24.545085156222836),
            ], closed=False),
            Build(point_list=[
                Point(15.392026695803732, 21.817790896852284),
                Point(11.66357378425918, 19.711905456072493),
                Point(15.599162968667319, 19),
                Point(12.69925514857711, 16.70842949955049),
                Point(15.737253817243042, 16.225111529535457),
                Point(12.733777860721041, 13.566862694452768),
                Point(15.875344665818766, 12.738317602998423),
                Point(12.492118875713524, 10.35625046506718),
                Point(15.771776529386972, 9.35509181289318),
                Point(12.630209724289248, 7.421819932833043),
                Point(16, 6.2135250077954565),
                Point(13, 4.521912112742836),
                Point(16.220571787258077, 3.31361718770525),
                Point(13, 1.760095141228353),
                Point(16.427708060121663, 0.5518002161907668),
                Point(13, 0.20657309475145644),
                Point(16.25509449940201, -2.3826303160433713),
                Point(13.320663967167869, -1),
                Point(13.389709391455732, -2.6242893010508883),
                Point(12.250459890706008, -1.139812678861854),
                Point(11.69809649640311, -2.5207211646190952),
                Point(11, -1.208858103149716),
                Point(9.626733767767249, -2.6933347253387505),
                Point(9.177938509896146, -0.8291082695664747),
                Point(7.1065757812602826, -2.865948286058406),
                Point(8.314870706297869, 0.7934592011982841),
                Point(6.519689674813455, 1.65652700479656),
                Point(8.3493934184418, 4.418343976311043),
                Point(6.554212386957387, 5.557593477060767),
                Point(8, 7.387297220689112),
                Point(6.347076114093801, 7.7670470542723535),
            ], closed=False),
        ])

    return floor
