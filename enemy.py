import pygame
from geometry import Column
from resourses import *
from geometry import find_angle_point, find_dist
from geometry import Line_segment, Point

objects_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()


class Object(Column, pygame.sprite.Sprite):
    def __init__(self, x, y, h, h_down, name=BASE_OBJECT):
        Column.__init__(self, x, y, h, h_down)
        self.name = name
        if name in objects_sprites[ENEMIES].keys():
            image = objects_sprites[ENEMIES][name][ROTATION][FRAMES][0]
        else:
            image = objects_sprites[BASE_OBJECT]
        self.w = image.get_width() * h / image.get_height()
        pygame.sprite.Sprite.__init__(self, objects_group)
        self.image = image
        self.radius = self.w / 2 * COLLIDE_SCALE
        self.true_radius = self.w / 2
        self.rect = pygame.Rect(x * COLLIDE_SCALE, y * COLLIDE_SCALE, ALMOST_ZERO * COLLIDE_SCALE,
                                ALMOST_ZERO * COLLIDE_SCALE)


class Enemy(Object):
    def __init__(self, x, y, h, h_down, angle, fow, hp, damage, name):
        super().__init__(x=x, y=y, h=h, h_down=h_down, name=name)
        enemies_group.add(self)
        self.angle = angle
        self.fow = fow
        self.hp = hp
        self.damage = damage

        self.sees_the_player = False
        self.run_to_player = False
        self.in_progress_of_hit = False
        self.hit_start_time = None

    def set_angle(self, angle):
        self.angle = angle

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            objects_group.remove(self)
            self.h_down = 0

    def run(self, fps, player, floor):
        if fps != 0:
            time = 1 / fps
            speed = player.add_speed + 5
            # speed = 2
            dist = speed * time

            delta_x = math.cos(math.radians(self.angle)) * dist
            delta_y = math.sin(math.radians(self.angle)) * dist

            move_vector = Line_segment(self, Point(self.x + delta_x, self.y + delta_y))

            is_intersection = False
            if not is_intersection:
                for build in floor.build_list:
                    for wall in build.wall_list:
                        intersection = move_vector.find_intersection(wall)
                        if intersection:
                            if self.h_down <= intersection.column.h_down + intersection.column.h and self.h_down + self.h >= intersection.column.h_down:
                                is_intersection = True
                                break
                    if is_intersection:
                        break
            if is_intersection:
                return

            self.x += delta_x
            self.y += delta_y
            self.pos = (self.x, self.y)
            self.rect.x += delta_x * COLLIDE_SCALE
            self.rect.y += delta_y * COLLIDE_SCALE

    def hit(self, victim):
        self.in_progress_of_hit = True
        self.hit_start_time = pygame.time.get_ticks()
        victim.take_damage(self.damage)

    def does_he_see_player(self, player, floor):
        # враг увидит игрока, если:
        #   игрок в его поле зрения
        angle_to_player = find_angle_point(self, player)
        delta_angle = min(
            max(angle_to_player, self.angle) - min(angle_to_player, self.angle),
            360 - (max(angle_to_player, self.angle) - min(angle_to_player, self.angle)),
        )
        in_sight = delta_angle <= self.fow / 2
        if not in_sight:
            return False

        # между ним и игроком нет стен:
        view_vector = Line_segment(self, player)
        behind_the_wall = False
        for build in floor.build_list:
            for wall in build.wall_list:
                intersection = view_vector.find_intersection(wall)
                if intersection:
                    behind_the_wall = True
                    break
            if behind_the_wall:
                break
        if behind_the_wall:
            return False
        return True

    def update(self, player, floor, fps):
        # ии:
        if not (self.hp > 0 and ENABLE_AI_ENEMIES):
            return
        self.sees_the_player = self.does_he_see_player(player, floor)
        if self.sees_the_player:
            self.angle = find_angle_point(self, player)
            dist = find_dist(self, player)
            if dist > self.true_radius + player.true_radius + 1:
                self.run(fps, player, floor)
            if dist < ATTACK_DIST:
                if not self.in_progress_of_hit:
                    self.hit(player)


class Toflund(Enemy):
    def __init__(self, x, y, angle):
        h = 3
        h_down = 0
        hp = 1
        damage = 10
        fow = 90
        name = TOFLUND
        super().__init__(x=x, y=y, h=h, h_down=h_down, angle=angle, fow=fow, hp=hp, damage=damage, name=name)


class Baggebo(Enemy):
    def __init__(self, x, y, angle):
        h = 1.5
        h_down = 0
        hp = 1
        damage = 10
        fow = 90
        name = BAGGEBO
        super().__init__(x=x, y=y, h=h, h_down=h_down, angle=angle, fow=fow, hp=hp, damage=damage, name=name)
