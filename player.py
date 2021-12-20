import math
from settings import *
from geometric_classes import Column, Line_segment, Point


class Player(Column):
    def __init__(self, x=0, y=-1, angle_w=90, h=1.8, h_down=0, angle_h=0, speed=5):
        super().__init__(x=x, y=y, h=h, h_down=h_down)
        self.angle_w = angle_w % 360
        self.fov_w = FOW_W
        self.left_angle = (angle_w + FOW_W / 2) % 360
        self.right_angle = (angle_w - FOW_W / 2) % 360

        self.angle_h = angle_h
        self.fov_h = FOW_H
        self.bott_angle = angle_h - FOW_H / 2
        self.top_angle = angle_h + FOW_H / 2

        self.speed = speed

    def turn(self, diff_w, diff_h):
        self.angle_w = (self.angle_w + diff_w) % 360
        self.left_angle = (self.angle_w + self.fov_w / 2) % 360
        self.right_angle = (self.angle_w - self.fov_w / 2) % 360

        self.angle_h = (self.angle_h + diff_h) % 360
        self.top_angle = (self.angle_h + self.fov_h / 2) % 360
        self.bott_angle = (self.angle_h - self.fov_h / 2) % 360

    def run(self, direction, fps, floor):
        if fps != 0:
            time = 1 / fps
            dist = self.speed * time
            angle = None
            if direction == FORWARD:
                angle = self.angle_w
            if direction == LEFT:
                angle = (self.angle_w + 90) % 360
            if direction == RIGHT:
                angle = (self.angle_w - 90) % 360
            if direction == BACK:
                angle = (self.angle_w + 180) % 360

            delta_x = math.cos(math.radians(angle)) * dist
            delta_y = math.sin(math.radians(angle)) * dist

            move_vector = Line_segment(self, Point(self.x + delta_x, self.y + delta_y))

            if COLLISION:
                is_intersection = False
                for build in floor.build_list:
                    for wall in build.wall_list:
                        intersection = move_vector.find_intersection(wall)
                        if intersection:
                            is_intersection = True
                            break
                    if is_intersection:
                        break
                if is_intersection:
                    return 0, 0

            self.x += delta_x
            self.y += delta_y
            self.pos = (self.x, self.y)

            return delta_x, delta_y
        return 0, 0

    def fly(self, direction, fps):
        if fps != 0:
            time = 1 / fps
            dist = self.speed * time
            if direction == UP:
                self.h_down += dist
            if direction == DOWN:
                self.h_down -= dist
