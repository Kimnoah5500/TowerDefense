import pygame
import player
from collections import deque


class WaveManager:
    def __init__(self, enemy_manager):
        self.setup_waves()
        self.endless_mode = False
        self.enemy_manager = enemy_manager
        self.time = 0
        self.time_since_last_spawn = 0
        self.all_waves_completed = False

    def setup_waves(self):
        self.first_wave = deque(["ba", "ba", "ba", "ba", "ba", "ba", "ba"])
        self.second_wave = deque(["ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba"])
        self.third_wave = deque(
            ["ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba",
             "ba", "ba", "ba", "ba"])
        self.endless_mode_wave = deque(
            ["ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba",
             "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba",
             "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba"])

    def manage(self, time_difference):
        self.time_since_last_spawn += time_difference
        if not self.endless_mode:
            self.time += time_difference
            if 20000 > self.time > 10000:
                if self.first_wave:
                    if self.time_since_last_spawn > 1000:
                        self.enemy_manager.new_enemy(self.first_wave.popleft())
                        self.time_since_last_spawn = 0
            elif 30000 > self.time > 20000:
                if self.second_wave:
                    if self.time_since_last_spawn > 800:
                        self.enemy_manager.new_enemy(self.second_wave.popleft())
                        self.time_since_last_spawn = 0
            elif self.time > 30000:
                if self.third_wave:
                    if self.time_since_last_spawn > 400:
                        self.enemy_manager.new_enemy(self.third_wave.popleft())
                        self.time_since_last_spawn = 0
                elif not self.enemy_manager.enemys:
                    self.all_waves_completed = True
        else:
            if self.endless_mode_wave:
                if self.time_since_last_spawn > 100:
                    self.enemy_manager.new_enemy(self.endless_mode_wave.popleft())
                    self.time_since_last_spawn = 0
            else:
                self.time_since_last_spawn = -9900
                self.endless_mode_wave = deque(
                    ["ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba",
                     "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba",
                     "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba"])

    def set_endless_mode(self):
        self.endless_mode = True

    def get_all_waves_completed(self):
        if not self.endless_mode:
            return self.all_waves_completed
        else:
            return False


class EnemyManager:
    def __init__(self, board, player, scale, window):
        self.board = board
        self.player = player
        self.scale = scale
        self.enemys = []
        self.window = window
        self.start_pos = board.get_start_pos()

    def new_enemy(self, enemy_code):
        if enemy_code == "ba":
            self.enemys.append(Ballon(self.scale, self.board, self.start_pos))

    def hit_enemy(self, enemy, damage):
        if self.enemys.__contains__(enemy):
            if self.enemys[self.enemys.index(enemy)].hit(damage):
                self.player.add_money(enemy.get_money_value())
                self.enemys.remove(enemy)

    def manage(self):
        for enemy in self.enemys[:]:
            enemy.update_pos()
            enemy.correct_to_middle()
            enemy.render(self.window)
            if enemy.is_at_end():
                self.player.reduce_health_points(enemy.get_damage())
                self.enemys.remove(enemy)

    def get_enemys_in_range(self, start_point, end_point):
        """Searches for enemys in given quadratic range

        :param start_point: Tupel with x, y coordinates from left upper edge of search area
        :param end_point: Tupel with x, y coordinates from right lower edge of search area
        :type start_point: (int, int)
        :type end_point: (int, int)
        :return: List with all enemys found in search area
        """
        enemys_in_range = []
        for enemy in self.enemys:
            if enemy.pos_x > start_point[0] and enemy.pos_x < end_point[0] and enemy.pos_y > start_point[
                1] and enemy.pos_y < end_point[1]:
                enemys_in_range.append(enemy)
        return enemys_in_range


class Enemy:
    def __init__(self, board, scale, start_pos, health_points, money_value, damage, vel):
        self.money_value = money_value
        self.board = board
        self.size = scale * 60
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]
        self.damage = damage
        self.vel = vel
        self.last_movement = self.board.get_supposed_start_direction()
        self.health_points = health_points
        self.top_offset = player.Bar.get_height_of_bar()

    def update_pos(self):
        field_code = self.board.get_field_at_x_y(self.pos_x, self.pos_y)
        if field_code:
            field_code = field_code.get_field_code()
            if self.last_movement == "r":
                if field_code == "sh":
                    self.pos_x += self.vel
                    self.last_movement = "r"
                elif field_code == "elu":
                    if self.is_over_middle_in_x_direction():
                        self.pos_y -= self.vel
                        self.last_movement = "u"
                    else:
                        self.pos_x += self.vel
                        self.last_movement = "r"
                elif field_code == "eld":
                    if self.is_over_middle_in_x_direction():
                        self.pos_y += self.vel
                        self.last_movement = "d"
                    else:
                        self.pos_x += self.vel
                        self.last_movement = "r"
                elif field_code == "erd":
                    self.pos_x += self.vel
                    self.last_movement = "r"
                elif field_code == "eru":
                    self.pos_x += self.vel
                    self.last_movement = "r"
            elif self.last_movement == "u":
                if field_code == "eld":
                    if self.is_over_middle_in_y_direction():
                        self.pos_x -= self.vel
                        self.last_movement = "l"
                    else:
                        self.pos_y -= self.vel
                        self.last_movement = "u"
                elif field_code == "sv":
                    self.pos_y -= self.vel
                    self.last_movement = "u"
                elif field_code == "erd":
                    if self.is_over_middle_in_y_direction():
                        self.pos_x += self.vel
                        self.last_movement = "r"
                    else:
                        self.pos_y -= self.vel
                        self.last_movement = "u"
                elif field_code == "elu":
                    self.pos_y -= self.vel
                    self.last_movement = "u"
                elif field_code == "eru":
                    self.pos_y -= self.vel
                    self.last_movement = "u"
            elif self.last_movement == "l":
                if field_code == "eru":
                    if self.is_over_middle_in_x_direction():
                        self.pos_y -= self.vel
                        self.last_movement = "u"
                    else:
                        self.pos_x -= self.vel
                        self.last_movement = "l"
                if field_code == "sh":
                    self.pos_x -= self.vel
                    self.last_movement = "l"
                if field_code == "erd":
                    if self.is_over_middle_in_x_direction():
                        self.pos_y += self.vel
                        self.last_movement = "d"
                    else:
                        self.pos_x -= self.vel
                        self.last_movement = "l"
                if field_code == "elu":
                    self.pos_x -= self.vel
                    self.last_movement = "l"
                if field_code == "eld":
                    self.pos_x -= self.vel
                    self.last_movement = "l"
            elif self.last_movement == "d":
                if field_code == "eru":
                    if self.is_over_middle_in_y_direction():
                        self.pos_x += self.vel
                        self.last_movement = "r"
                    else:
                        self.pos_y += self.vel
                        self.last_movement = "d"
                elif field_code == "sv":
                    self.pos_y += self.vel
                    self.last_movement = "d"
                elif field_code == "elu":
                    if self.is_over_middle_in_y_direction():
                        self.pos_x -= self.vel
                        self.last_movement = "l"
                    else:
                        self.pos_y += self.vel
                        self.last_movement = "d"
                elif field_code == "erd":
                    self.pos_y += self.vel
                    self.last_movement = "d"
                elif field_code == "eld":
                    self.pos_y += self.vel
                    self.last_movement = "d"
        else:
            if self.last_movement == "r":
                self.pos_x += self.vel
            elif self.last_movement == "u":
                self.pos_y -= self.vel
            elif self.last_movement == "l":
                self.pos_x -= self.vel
            else:
                self.pos_y += self.vel

    def correct_to_middle(self):
        middle = self.get_middle_of_current_field()
        if self.last_movement == "d" or self.last_movement == "u":
            if self.pos_x < middle[0]:
                self.pos_x += 1
            elif self.pos_x > middle[0]:
                self.pos_x -= 1
        if self.last_movement == "r" or self.last_movement == "l":
            if self.pos_y < middle[1]:
                self.pos_y += 1
            elif self.pos_y > middle[1]:
                self.pos_y -= 1

    def is_over_middle_in_x_direction(self):
        middle = self.get_middle_of_current_field()
        if self.last_movement == "r":
            return self.pos_x > middle[0]
        elif self.last_movement == "l":
            return self.pos_x < middle[0]
        else:
            return False

    def is_over_middle_in_y_direction(self):
        middle = self.get_middle_of_current_field()
        if self.last_movement == "d":
            return self.pos_y > middle[1]
        elif self.last_movement == "u":
            return self.pos_y < middle[1]
        else:
            return False

    def get_middle_of_current_field(self):
        size_of_fields = self.board.get_size_of_one_field()
        return (self.pos_x // size_of_fields * size_of_fields + size_of_fields // 2, (
                self.pos_y - self.top_offset) // size_of_fields * size_of_fields + size_of_fields // 2 + self.top_offset)

    def is_at_end(self):
        current_field = self.board.get_field_at_x_y(self.pos_x, self.pos_y)
        if current_field:
            if current_field.is_end_block():
                size_of_fields = self.board.get_size_of_one_field()
                if self.last_movement == "r":
                    last_quarter = self.pos_x // size_of_fields * size_of_fields + size_of_fields // 4 * 3
                    if self.pos_x > last_quarter:
                        return True
                if self.last_movement == "l":
                    last_quarter = self.pos_x // size_of_fields * size_of_fields + size_of_fields // 4 * 1
                    if self.pos_x < last_quarter:
                        return True
                if self.last_movement == "d":
                    last_quarter = (
                                           self.pos_y + self.top_offset) // size_of_fields * size_of_fields + size_of_fields // 4 * 3
                    if self.pos_y > last_quarter:
                        return True
                if self.last_movement == "l":
                    last_quarter = (
                                           self.pos_y + self.top_offset) // size_of_fields * size_of_fields + size_of_fields // 4 * 1
                    if self.pos_y < last_quarter:
                        return True
            return False

    def hit(self, damage):
        self.health_points -= damage
        return self.health_points <= 0

    def get_damage(self):
        return self.damage

    def get_money_value(self):
        return self.money_value

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def render(self, window):
        window.blit(self.image, (self.pos_x - self.size // 2, self.pos_y - self.size // 2))


class Ballon(Enemy):
    def __init__(self, scale, board, start_pos):
        health_points = 100
        damage = 10
        vel = 5 * scale
        money_value = 200
        Enemy.__init__(self, board, scale, start_pos, health_points, money_value, damage, vel)
        self.image = pygame.image.load('./ressources/enemys/Enemy_ballon.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 60)))
