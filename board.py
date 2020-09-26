import field
import csv
import player
import pygame
import shop

class Board:
    def __init__(self, scale, level_number, window):
        self.size_of_one_field = int(100 * scale)
        self.board = []
        self.window = window
        self.scale = scale
        self.top_offset = player.Bar.get_height_of_bar(scale)
        file = csv.reader(open('./levels/level_' + str(level_number) + '.csv'), delimiter=';')

        row_number = 0
        for row in file:
            if row_number == 0:
                self.start_side = row[2]
                start_x = int(row[0])
                start_y = int(row[1])
                end_x = int(row[3])
                end_y = int(row[4])
            else:
                self.board.append([])
                for cell in row:
                    if cell == "ey":
                        self.board[row_number - 1].append(field.EmptyField(self.size_of_one_field))
                    elif cell == "sh":
                        self.board[row_number - 1].append(field.StraightPathFieldHorizontal(self.size_of_one_field))
                    elif cell == "sv":
                        self.board[row_number - 1].append(field.StraightPathFieldVertical(self.size_of_one_field))
                    elif cell == "elu":
                        self.board[row_number - 1].append(field.EdgePathFieldLeftUp(self.size_of_one_field))
                    elif cell == "eld":
                        self.board[row_number - 1].append(field.EdgePathFieldLeftDown(self.size_of_one_field))
                    elif cell == "eru":
                        self.board[row_number - 1].append(field.EdgePathFieldRightUp(self.size_of_one_field))
                    elif cell == "erd":
                        self.board[row_number - 1].append(field.EdgePathFieldRightDown(self.size_of_one_field))
            row_number += 1

        if self.start_side == "l":
            self.start_pos_x = -self.size_of_one_field // 2
            self.start_pos_y = self.size_of_one_field * start_y - self.size_of_one_field // 2 + self.top_offset
        elif self.start_side == "u":
            self.start_pos_x = self.size_of_one_field * start_x - self.size_of_one_field // 2
            self.start_pos_y = -self.size_of_one_field // 2 + self.top_offset
        elif self.start_side == "r":
            self.start_pos_x = self.size_of_one_field * len(self.board[0]) + self.size_of_one_field // 2
            self.start_pos_y = self.start_pos_y = self.size_of_one_field * start_y - self.size_of_one_field // 2 + self.top_offset
        elif self.start_side == "d":
            self.start_pos_x = self.size_of_one_field * start_x - self.size_of_one_field // 2
            self.start_pos_y = self.size_of_one_field * len(self.board) + self.size_of_one_field // 2 + self.top_offset

        self.board[end_x - 1][end_y - 1].set_as_end_block()

    def get_field_at(self, row, column):
        return self.board[row][column]

    def get_field_at_x_y(self, x, y):
        if 0 <= x <= pygame.display.get_window_size()[0] and player.Bar.get_height_of_bar(self.scale) < y < pygame.display.get_window_size()[1] - shop.Shop.height:
            return self.board[int((y - self.top_offset) // self.size_of_one_field)][int(x // self.size_of_one_field)]
        else:
            return None

    def get_board_width(self):
        return len(self.board[0])

    def get_board_height(self):
        return len(self.board)

    def render(self):
        for row in range(self.get_board_height()):
            for column in range(self.get_board_width()):
                self.window.blit(self.get_field_at(row, column).get_image(),
                                 (self.size_of_one_field * column, self.size_of_one_field * row + self.top_offset))
                if (self.get_field_at(row, column).get_tower()):
                    self.get_field_at(row, column).get_tower().render(self.window,
                                                                      self.size_of_one_field * column + self.size_of_one_field // 2,
                                                                      self.size_of_one_field * row + self.size_of_one_field // 2 + self.top_offset)

    def get_size_of_one_field(self):
        return self.size_of_one_field

    def get_supposed_start_direction(self):
        if self.start_side == "l":
            return "r"
        elif self.start_side == "u":
            return "d"
        elif self.start_side == "r":
            return "l"
        elif self.start_side == "d":
            return "u"

    def add_tower_to_field(self, tower, row, column):
        self.board[row][column].place_tower(tower)

    def remove_tower_from_field(self, row_column):
        return self.board[row_column[0]][row_column[1]].remove_tower()

    def get_start_pos(self):
        return (self.start_pos_x, self.start_pos_y)

    def get_middle_of_field(self, row, column):
        return (column * self.size_of_one_field + self.size_of_one_field // 2,
                row * self.size_of_one_field + self.size_of_one_field // 2 + self.top_offset)

    def get_middle_of_one_field_from_x_y(self, pos):
        return (
        int(pos[0] // self.size_of_one_field * self.size_of_one_field + self.size_of_one_field / 2),
        int((pos[1] - self.top_offset) // self.size_of_one_field * self.size_of_one_field + self.size_of_one_field / 2) + self.top_offset)

    def get_row_and_column_from_x_y(self, x, y):
        return int((y - self.top_offset) // self.size_of_one_field), int(x // self.size_of_one_field)

    def check_if_placable(self, x, y):

        check_field = self.get_field_at_x_y(x, y)

        if check_field and not check_field.tower and not isinstance(check_field, field.PathField):
            return True
        else:
            return False
