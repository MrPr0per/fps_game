from geometric_classes import Floor, Build, Column
import math


def load_floor(num_floor):
    floor = None
    # if num_floor == 1:
    #     point_list = [
    #         Point(-1, 0),
    #         Point(1, 0),
    #     ]
    #     build = Build(column_list=point_list, is_closed=False)
    #     floor = Floor(build_list=[build])
    # if num_floor == 2:
    #     floor = Floor(build_list=[
    #         Build(column_list=[
    #             Point(0, 0),
    #             Point(1, 0),
    #             Point(1, 1),
    #             Point(0, 1),
    #         ], is_closed=True),
    #         Build(column_list=[
    #             Point(2, 0),
    #             Point(4, 0),
    #             Point(3, -2),
    #         ], is_closed=True),
    #         Build(column_list=[
    #             Point(5, 1),
    #             Point(5, 0),
    #             Point(10, 0),
    #             Point(10, 5),
    #             Point(5, 5),
    #             Point(5, 4),
    #         ], is_closed=False),
    #     ])
    # if num_floor == 3:
    #     build_list = []
    #     for i in range(-20, 20):
    #         i *= 4
    #         build = Build(column_list=[
    #             Point(i, 0),
    #             Point(i + 2, 0),
    #             Point(i + 2, 2),
    #             Point(i, 2),
    #         ], is_closed=True)
    #         build_list.append(build)
    #     floor = Floor(build_list)
    # if num_floor == 4:
    #     floor = Floor(build_list=[
    #         Build(column_list=[
    #             Point(-1, 0),
    #             Point(-1, -1),
    #             Point(1, -1),
    #             Point(1, 0),
    #             Point(2, 0),
    #             Point(4, 1),
    #             Point(5, 2),
    #             Point(6, 4),
    #             Point(6, 6),
    #             Point(8.8747526, 6),
    #             Point(9, 8),
    #             Point(2, 8),
    #             Point(2, 6),
    #             Point(4.8967929, 6),
    #             Point(5, 4),
    #             Point(4, 2),
    #             Point(2, 1),
    #             Point(1, 1),
    #             Point(1, 2),
    #             Point(-1, 2),
    #             Point(-1, 1),
    #         ], is_closed=False),
    #         Build(column_list=[
    #             Point(-1, 1),
    #             Point(-2, 1),
    #             Point(-2, 3),
    #             Point(-1, 3),
    #             Point(-1, 5),
    #             Point(-3, 5),
    #             Point(-3, 3),
    #             Point(-2.5598684000000023, 3),
    #             Point(-2.543763300000002, 1),
    #             Point(-2.5598684000000023, 0),
    #             Point(-1, 0),
    #         ], is_closed=False),
    #     ])
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
            ], is_closed=False),
            Build(column_list=[
                Column(6.381598826237731, 13.152590148725595),
                Column(4.759031355472972, 13.152590148725595),
                Column(4.275713385457938, 14.809680331634285),
                Column(0.3056014889058689, 18.33099697031525),
                Column(-5.252555166267028, 15.569179998800767),
                Column(-4.803759908395924, 13),
                Column(-7.116781622039304, 13),
            ], is_closed=False),
            Build(column_list=[
                Column(-7, 10),
                Column(-4.631146347676269, 10.149114192203594),
                Column(-4.424010074812683, 7.594433493552698),
                Column(-1, 6),
                Column(-1, 3),
            ], is_closed=False),
            Build(column_list=[
                Column(-7, 10),
                Column(-9.119098926387304, 9.251523676461387),
                Column(-11, 7.352774508545181),
                Column(-11.777347761469994, 5.454025340628974),
                Column(-12.157097595053235, 3.4862307484249047),
                Column(-12.32971115577289, 1.65652700479656),
                Column(-12.536847428636477, 0.10300495831966333),
            ], is_closed=False),
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
            ], is_closed=False),
            Build(column_list=[
                Column(-17, -3.5909252410809573),
                Column(-14.193937611545167, -10.737126654874682),
                Column(-11.777347761469994, -3.3147435439295094),
                Column(-18, -7.595559849776958),
                Column(-10.6726209728642, -8),
            ], is_closed=True),
            Build(column_list=[
                Column(6.312553401949869, 13.187112860869526),
                Column(6.485166962669524, 19),
                Column(4.862599491904765, 19.159542061769596),
            ], is_closed=False),
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
            ], is_closed=False),
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
            ], is_closed=False),
            Build(column_list=[
                Column(8.107734433434283, 24.372471595503182),
                Column(8.832711388456834, 27),
                Column(9.108893085608283, 24.510562444078907),
            ], is_closed=False),
            Build(column_list=[
                Column(10, 26.443834324139043),
                Column(10, 24.786744141230354),
                Column(10.69693784422911, 24.6141305805107),
                Column(11.421914799251663, 25.166493974813594),
                Column(11.249301238532007, 27.34142483988125),
                Column(10.524324283509456, 27.30690212773732),
            ], is_closed=True),
            Build(column_list=[
                Column(12.595687012145317, 24.510562444078907),
                Column(13.389709391455732, 27.410470264169113),
                Column(14, 24.545085156222836),
            ], is_closed=False),
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
            ], is_closed=False),
        ])
    if num_floor == 6:
        floor = Floor(build_list=[
            Build(column_list=[
                Column(-1, 3),
                Column(-1, 5),
                Column(-2, 5),
                Column(-2, 6),
                Column(-4, 6),
                Column(-4, 4),
                Column(-5, 4),
                Column(-5, 3),
                Column(-1, 3),
            ], is_closed=False),
            Build(column_list=[
                Column(-4, 2),
                Column(-5, 2),
                Column(-5, -1),
                Column(-8, -1),
                Column(-8, 0),
                Column(-9, 0),
                Column(-9, -2),
                Column(-4, -2),
                Column(-4, 2),
            ], is_closed=False),
            Build(column_list=[
                Column(-9, 2),
                Column(-8, 2),
                Column(-8, 6),
                Column(-9, 6),
                Column(-9, 2),
            ], is_closed=False),
            Build(column_list=[
                Column(-4, 8),
                Column(-2, 8),
                Column(-2, 9),
                Column(-1, 9),
                Column(-1, 11),
                Column(-4, 11),
            ], is_closed=True),
            Build(column_list=[
                Column(-9, 8),
                Column(-8, 8),
                Column(-8, 11),
                Column(-9, 11),
            ], is_closed=True),
            Build(column_list=[
                Column(-9, 13),
                Column(-8, 13),
                Column(-8, 14),
                Column(-9, 14),
            ], is_closed=True),
            Build(column_list=[
                Column(-9, 16),
                Column(-8, 16),
                Column(-8, 17),
                Column(-9, 17),
                Column(-9, 16),
            ], is_closed=False),
            Build(column_list=[
                Column(-9, 19),
                Column(-8, 19),
                Column(-8, 23),
                Column(-9, 23),
            ], is_closed=True),
            Build(column_list=[
                Column(-9, 25),
                Column(-8, 25),
                Column(-8, 27),
                Column(-5, 27),
                Column(-5, 29),
            ], is_closed=False),
            Build(column_list=[
                Column(-9, 25),
                Column(-9, 27),
                Column(-12, 27),
                Column(-12, 28),
                Column(-9, 28),
                Column(-9, 31),
                Column(-7, 31),
                Column(-5, 29),
            ], is_closed=False),
            Build(column_list=[
                Column(-14, 28),
                Column(-14, 27),
                Column(-17, 27),
                Column(-17, 31),
                Column(-16, 31),
                Column(-16, 28),
            ], is_closed=True),
            Build(column_list=[
                Column(-17, 33),
                Column(-16, 33),
                Column(-16, 34),
                Column(-17, 34),
            ], is_closed=True),
            Build(column_list=[
                Column(-17, 36),
                Column(-16, 36),
                Column(-16, 37),
                Column(-17, 37),
            ], is_closed=True),
            Build(column_list=[
                Column(-17, 39),
                Column(-16, 39),
                Column(-16, 42),
                Column(-14, 42),
                Column(-14, 43),
                Column(-17, 43),
            ], is_closed=True),
            Build(column_list=[
                Column(-12, 43),
                Column(-12, 42),
                Column(-9, 42),
                Column(-9, 39),
                Column(-7, 39),
                Column(-5, 41),
                Column(-5, 43),
                Column(-8, 43),
                Column(-8, 45),
                Column(-9, 45),
                Column(-9, 43),
            ], is_closed=True),
            Build(column_list=[
                Column(-8, 47),
                Column(-8, 50),
                Column(-9, 50),
                Column(-9, 47),
                Column(-8, 47),
            ], is_closed=False),
            Build(column_list=[
                Column(5, 43),
                Column(5, 41),
                Column(7, 39),
                Column(9, 39),
                Column(9, 42),
                Column(12, 42),
                Column(12, 43),
                Column(9, 43),
                Column(9, 45),
                Column(8, 45),
                Column(8, 43),
                Column(5, 43),
            ], is_closed=False),
            Build(column_list=[
                Column(8, 47),
                Column(9, 47),
                Column(9, 50),
                Column(8, 50),
                Column(8, 47),
            ], is_closed=False),
            Build(column_list=[
                Column(-6, 50),
                Column(-6, 49),
                Column(-3, 49),
                Column(-3, 50),
                Column(-6, 50),
            ], is_closed=False),
            Build(column_list=[
                Column(-2, 50),
                Column(-2, 49),
                Column(6, 49),
                Column(6, 50),
                Column(-2, 50),
            ], is_closed=False),
            Build(column_list=[
                Column(-5, 50),
                Column(-4, 53),
                Column(-3, 54),
                Column(0, 55),
                Column(3, 54),
                Column(4, 53),
                Column(5, 50),
            ], is_closed=False),
            Build(column_list=[
                Column(-4, 50),
                Column(-3, 53),
                Column(0, 54),
                Column(3, 53),
                Column(4, 50),
            ], is_closed=False),
            Build(column_list=[
                Column(14, 43),
                Column(17, 43),
                Column(17, 39),
                Column(16, 39),
                Column(16, 42),
                Column(14, 42),
                Column(14, 43),
            ], is_closed=False),
            Build(column_list=[
                Column(16, 37),
                Column(17, 37),
                Column(17, 36),
                Column(16, 36),
            ], is_closed=True),
            Build(column_list=[
                Column(16, 34),
                Column(17, 34),
                Column(17, 33),
                Column(16, 33),
            ], is_closed=True),
            Build(column_list=[
                Column(16, 31),
                Column(17, 31),
                Column(17, 27),
                Column(14, 27),
                Column(14, 28),
                Column(16, 28),
            ], is_closed=True),
            Build(column_list=[
                Column(12, 28),
                Column(9, 28),
                Column(9, 31),
                Column(7, 31),
                Column(5, 29),
                Column(5, 27),
                Column(8, 27),
                Column(8, 25),
                Column(9, 25),
                Column(9, 27),
                Column(12, 27),
                Column(12, 28),
            ], is_closed=False),
            Build(column_list=[
                Column(8, 23),
                Column(9, 23),
                Column(9, 19),
                Column(8, 19),
                Column(8, 23),
            ], is_closed=False),
            Build(column_list=[
                Column(8, 17),
                Column(9, 17),
                Column(9, 16),
                Column(8, 16),
                Column(8, 17),
            ], is_closed=False),
            Build(column_list=[
                Column(8, 14),
                Column(9, 14),
                Column(9, 13),
                Column(8, 13),
                Column(8, 14),
            ], is_closed=False),
            Build(column_list=[
                Column(8, 11),
                Column(9, 11),
                Column(9, 8),
                Column(8, 8),
                Column(8, 11),
            ], is_closed=False),
            Build(column_list=[
                Column(8, 6),
                Column(9, 6),
                Column(9, 2),
                Column(8, 2),
                Column(8, 6),
            ], is_closed=False),
            Build(column_list=[
                Column(8, 0),
                Column(9, 0),
                Column(9, -2),
                Column(4, -2),
                Column(4, 3),
                Column(1, 3),
                Column(1, 5),
                Column(2, 5),
                Column(2, 6),
                Column(4, 6),
                Column(4, 4),
                Column(5, 4),
                Column(5, -1),
                Column(8, -1),
                Column(8, 0),
            ], is_closed=False),
            Build(column_list=[
                Column(2, 8),
                Column(4, 8),
                Column(4, 11),
                Column(1, 11),
                Column(1, 9),
                Column(2, 9),
                Column(2, 8),
            ], is_closed=False),
        ])
    if num_floor == 7:
        floor = Floor(build_list=[
            Build(column_list=[
                Column(i, 0, i, 0),
                Column(i + 1, 0, i, 0),
            ], is_closed=False)
            for i in range(2, 100)
        ])
    if num_floor == 8:
        floor = Floor(build_list=[
            Build(column_list=[
                Column(x=0, y=0, h=2, h_down=0),
                Column(x=1, y=0, h=2, h_down=3),
                Column(x=2, y=0, h=2, h_down=0),
            ], is_closed=False),
            Build(column_list=[
                Column(x=3, y=0, h=5, h_down=0),
                Column(x=4, y=0, h=5, h_down=0),
            ], is_closed=False),
            Build(column_list=[
                Column(x=5, y=0, h=5, h_down=0),
                Column(x=6, y=0, h=5, h_down=0),
            ], is_closed=False),
            Build(column_list=[
                Column(x=4, y=0, h=1, h_down=4),
                Column(x=5, y=0, h=1, h_down=4),
            ], is_closed=False),
            Build(column_list=[
                Column(x=4, y=0, h=1, h_down=0),
                Column(x=5, y=0, h=1, h_down=0),
            ], is_closed=False),
            Build(column_list=[
                Column(x=7, y=0, h=2, h_down=0),
                Column(x=8, y=0, h=2, h_down=3),
                Column(x=9, y=0, h=2, h_down=0),
            ], is_closed=False),
            Build(column_list=[
                Column(x=-1, y=2, h=2, h_down=0),
                Column(x=10, y=2, h=2, h_down=3),
            ], is_closed=False),
            Build(column_list=[
                Column(x=-1, y=5, h=2, h_down=3),
                Column(x=10, y=5, h=2, h_down=0),
            ], is_closed=False),
        ])
    if num_floor == 9:
        floor = Floor(build_list=[])

        for i in range(100):
            for j in range(i - 2, i):
                b = Build(column_list=[
                    Column(1, i * 2, 1, j * 2),
                    Column(2, i * 2, 1, j * 2),
                    # Column(2, i * 2 + 1, 1, j * 2),
                    # Column(1, i * 2 + 1, 1, j * 2),
                ], is_closed=False
                )
                floor.build_list.append(b)

        b = Build(column_list=[
            Column(1, 1, 100, 0),
            Column(2, 1, 100, 0),
        ], is_closed=False)
        floor.build_list.append(b)
        b = Build(column_list=[
            Column(1, 100, 100, 0),
            Column(2, 100, 100, 0),
        ], is_closed=False)
        floor.build_list.append(b)
    if num_floor == 10:
        n = 20
        floor = Floor(build_list=[
            Build(column_list=[
                Column(-3, i * 4 + 0, 2, 5),
                Column(-3, i * 4 + 1, 1, 6),
                Column(-3, i * 4 + 2, 2, 5),
                Column(-3, i * 4 + 2, 7, 0),
                Column(-3, i * 4 + 4, 7, 0),
            ], is_closed=False) for i in range(-n, n)
        ])
        for i in range(-n, n):
            floor.build_list.append(
                Build(column_list=[
                    Column(3, i * 4 + 0, 2, 5),
                    Column(3, i * 4 + 1, 1, 6),
                    Column(3, i * 4 + 2, 2, 5),
                    Column(3, i * 4 + 2, 7, 0),
                    Column(3, i * 4 + 4, 7, 0),
                ], is_closed=False)
            )
        floor.build_list.append(
            Build(column_list=[
                Column(3, -n * 4, 1, 0),
                Column(3, n * 4, 1, 0),
            ], is_closed=False)
        )
        floor.build_list.append(
            Build(column_list=[
                Column(-3, -n * 4, 1, 0),
                Column(-3, n * 4, 1, 0),
            ], is_closed=False)
        )

    if num_floor == 11:
        floor = Floor(build_list=[
            Build(column_list=[
                Column(-1.5, 3.0, 4.5, 0.0),
                Column(-9.0, 3.0, 4.5, 0.0),
                Column(-9.0, -1.5, 4.5, 0.0),
                Column(-6.0, -4.5, 4.5, 0.0),
                Column(4.5, -4.5, 4.5, 0.0),
                Column(4.5, -3.0, 4.5, 0.0),
                Column(6.0, -3.0, 4.5, 0.0),
                Column(7.5, -4.5, 4.5, 0.0),
                Column(7.5, -7.5, 4.5, 0.0),
                Column(-9.0, -7.5, 4.5, 0.0),
                Column(-12.0, -4.5, 4.5, 0.0),
                Column(-12.0, -1.5, 4.5, 0.0),
                Column(-13.5, -1.5, 4.5, 0.0),
            ], is_closed=False),
            Build(column_list=[
                Column(-13.5, -1.5, 1.5, 0.0),
                Column(-18.0, -1.5, 1.5, 0.0),
            ], is_closed=False),
            Build(column_list=[
                Column(-13.5, -1.5, 1.5, 3.0),
                Column(-18.0, -1.5, 1.5, 3.0),
            ], is_closed=False),
            Build(column_list=[
                Column(-18.0, -1.5, 4.5, 0.0),
                Column(-21.0, -1.5, 4.5, 0.0),
                Column(-31.5, 3.302233873798383, 4.5, 0.0),
                Column(-31.5, 12.0, 4.5, 0.0),
                Column(-28.5, 12.0, 4.5, 0.0),
                Column(-28.5, 9.0, 4.5, 0.0),
                Column(-18.0, 9.0, 4.5, 0.0),
            ], is_closed=False),
            Build(column_list=[
                Column(-18.0, 9.0, 1.5, 3.0),
                Column(-13.5, 9.0, 1.5, 3.0),
            ], is_closed=False),
            Build(column_list=[
                Column(-18.0, 9.0, 1.5, 0.0),
                Column(-13.5, 9.0, 1.5, 0.0),
            ], is_closed=False),
            Build(column_list=[
                Column(-13.5, 9.0, 4.5, 0.0),
                Column(-9.0, 9.0, 4.5, 0.0),
                Column(-6.0, 13.5, 4.5, 0.0),
                Column(-1.5, 13.5, 4.5, 0.0),
                Column(-1.5, 3.0, 4.5, 0.0),
            ], is_closed=False),
            Build(column_list=[
                Column(3.0, 3.0, 4.5, 0.0),
                Column(3.0, 16.5, 4.5, 0.0),
                Column(-7.5, 16.5, 4.5, 0.0),
                Column(-10.5, 12.0, 4.5, 0.0),
                Column(-15.0, 21.0, 4.5, 0.0),
                Column(-45.0, 21.0, 4.5, 0.0),
            ], is_closed=False),
            Build(column_list=[
                Column(-39.0, 19.01388927924775, 4.5, 0.0),
                Column(-36.0, 19.065673347463644, 4.5, 0.0),
                Column(-36.0, -6.0, 4.5, 0.0),
                Column(-39.0, -6.0, 4.5, 0.0),
                Column(-43.5, -4.5, 4.5, 0.0),
                Column(-46.5, -3.0, 4.5, 0.0),
                Column(-48.0, -1.5, 4.5, 0.0),
                Column(-49.5, 1.5, 4.5, 0.0),
                Column(-51.0, 6.0, 4.5, 0.0),
                Column(-51.0, 9.0, 4.5, 0.0),
                Column(-46.5, 13.5, 4.5, 0.0),
                Column(-39.0, 13.5, 4.5, 0.0),
                Column(-39.0, 18.964043048252336, 4.5, 0.0),
            ], is_closed=False),
            Build(column_list=[
                Column(-45.0, 21.0, 4.5, 0.0),
                Column(-55.5, 21.0, 4.5, 0.0),
                Column(-55.5, 9.0, 4.5, 0.0),
                Column(-54.0, 9.0, 4.5, 0.0),
                Column(-54.0, 4.5, 4.5, 0.0),
                Column(-52.5, 0.0, 4.5, 0.0),
                Column(-51.0, -3.0, 4.5, 0.0),
                Column(-48.0, -6.0, 4.5, 0.0),
                Column(-45.0, -7.5, 4.5, 0.0),
                Column(-40.5, -9.0, 4.5, 0.0),
                Column(-31.5, -9.0, 4.5, 0.0),
                Column(-31.5, -6.0, 4.5, 0.0),
                Column(-18.0, -6.0, 4.5, 0.0),
                Column(-15.0, -9.0, 4.5, 0.0),
                Column(-12.0, -10.5, 4.5, 0.0),
                Column(9.0, -10.5, 4.5, 0.0),
                Column(10.5, -9.0, 4.5, 0.0),
                Column(10.5, -3.0, 4.5, 0.0),
                Column(7.5, 0.0, 4.5, 0.0),
                Column(4.5, 0.0, 4.5, 0.0),
                Column(4.5, 3.0, 4.5, 0.0),
                Column(3.0, 3.0, 4.5, 0.0),
            ], is_closed=False),
        ])

    return floor
