import pygame

class Enemy_manager:
    def __init__(self, board, size, window):
        self.board = board
        self.size = size
        self.enemys = []
        self.window = window
        self.start_pos = board.get_start_pos()

    def new_ememy(self):
        self.enemys.append(Ballon(self.size, self.board, self.start_pos))

    def manage(self):
        for enemy in self.enemys[:]:
            enemy.update_pos()
            enemy.correct_to_middle()
            enemy.render(self.window)
            if enemy.is_at_end():
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
            if enemy.pos_x > start_point[0] and enemy.pos_x < end_point[0] and enemy.pos_y > start_point[1] and enemy.pos_y < end_point[1]:
                enemys_in_range.append(enemy)
        return enemys_in_range

class Enemy:
    def __init__(self, board, size, start_pos):
        self.board = board
        self.size = size
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]
        self.vel = 5
        self.last_movement = self.board.get_supposed_start_direction()


    def update_pos(self):
        field_code = self.board.get_field_at_x_y(self.pos_x, self.pos_y).get_field_code()
        if self.last_movement == "r":
            if field_code == "sh":
                self.pos_x += self.vel
                self.last_movement = "r"
            elif field_code == "elu":
                if (self.is_over_middle_in_x_direction()):
                    self.pos_y -= self.vel
                    self.last_movement = "u"
                else:
                    self.pos_x += self.vel
                    self.last_movement = "r"
            elif field_code == "eld":
                if (self.is_over_middle_in_x_direction()):
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
            else:
                self.pos_x += self.vel
                self.last_movement = "r"
        elif self.last_movement == "u":
            if field_code == "eld":
                if (self.is_over_middle_in_y_direction()):
                    self.pos_x -= self.vel
                    self.last_movement = "l"
                else:
                    self.pos_y -= self.vel
                    self.last_movement = "u"
            elif field_code == "sv":
                self.pos_y -= self.vel
                self.last_movement = "u"
            elif field_code == "erd":
                if (self.is_over_middle_in_y_direction()):
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
                if (self.is_over_middle_in_x_direction()):
                    self.pos_y -= self.vel
                    self.last_movement = "u"
                else:
                    self.pos_x -= self.vel
                    self.last_movement = "l"
            if field_code == "sh":
                self.pos_x -= self.vel
                self.last_movement = "l"
            if field_code == "erd":
                if (self.is_over_middle_in_x_direction()):
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
                if (self.is_over_middle_in_y_direction()):
                    self.pos_x += self.vel
                    self.last_movement = "r"
                else:
                    self.pos_y += self.vel
                    self.last_movement = "d"
            elif field_code == "sv":
                self.pos_y += self.vel
                self.last_movement = "d"
            elif field_code == "elu":
                if (self.is_over_middle_in_y_direction()):
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

    def correct_to_middle(self):
        if self.last_movement == "d" or self.last_movement == "u":
            middle = self.get_middle_of_current_field()[0]
            if self.pos_x < middle:
                self.pos_x += 1
            elif self.pos_x > middle:
                self.pos_x -= 1
        if self.last_movement == "r" or self.last_movement == "l":
            middle = self.get_middle_of_current_field()[1]
            if self.pos_y < middle:
                self.pos_y += 1
            elif self.pos_y > middle:
                self.pos_y -= 1

    def is_over_middle_in_x_direction(self):
        middle = self.get_middle_of_current_field()[0]
        if self.last_movement == "r":
            return self.pos_x > middle
        elif self.last_movement == "l":
            return self.pos_x < middle
        else:
            return False

    def is_over_middle_in_y_direction(self):
        middle = self.get_middle_of_current_field()[1]
        if self.last_movement == "d":
            return self.pos_y > middle
        elif self.last_movement == "u":
            return self.pos_y < middle
        else:
            return False

    def get_middle_of_current_field(self):
        size_of_fields = self.board.get_size_of_one_field()
        return self.pos_x // size_of_fields * size_of_fields + size_of_fields // 2, self.pos_y // size_of_fields * size_of_fields + size_of_fields // 2

    def is_at_end(self):
        current_field = self.board.get_field_at_x_y(self.pos_x, self.pos_y)
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
                last_quarter = self.pos_y // size_of_fields * size_of_fields + size_of_fields // 4 * 3
                if self.pos_y > last_quarter:
                    return True
            if self.last_movement == "l":
                last_quarter = self.pos_y // size_of_fields * size_of_fields + size_of_fields // 4 * 1
                if self.pos_y < last_quarter:
                    return True
        return False

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def render(self, window):
        window.blit(self.image, (self.pos_x - self.size // 2, self.pos_y - self.size // 2))


class Ballon(Enemy):
    def __init__(self, size, board, start_pos):
        Enemy.__init__(self, board, size, start_pos)
        self.image = pygame.image.load('./ressources/Enemy_ballon.png')
        self.image = pygame.transform.scale(self.image, (size, size))
