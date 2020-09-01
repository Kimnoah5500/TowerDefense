import field
import csv

class Board:

    def __init__(self, size):
        self.size_of_one_field = size
        self.board = []
        file = csv.reader(open('./levels/level_1.csv'), delimiter=';')

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
                        self.board[row_number - 1].append(field.Empty_Field(size))
                    elif cell == "sh":
                        self.board[row_number - 1].append(field.Straight_way_field_hotizontal(size))
                    elif cell == "sv":
                        self.board[row_number - 1].append(field.Straight_way_field_vertikal(size))
                    elif cell == "elu":
                        self.board[row_number - 1].append(field.Edge_way_field_left_up(size))
                    elif cell == "eld":
                        self.board[row_number - 1].append(field.Edge_way_field_left_down(size))
                    elif cell == "eru":
                        self.board[row_number - 1].append(field.Edge_way_field_right_up(size))
                    elif cell == "erd":
                        self.board[row_number - 1].append(field.Edge_way_field_right_down(size))
            row_number += 1

        if self.start_side == "l":
            self.start_pos_x = -size//2
            self.start_pos_y = size * start_y - size // 2
        elif self.start_side == "u":
            self.start_pos_x = size * start_x - size // 2
            self.start_pos_y = -size//2
        elif self.start_side == "r":
            self.start_pos_x = size * len(self.board[0]) + size // 2
            self.start_pos_y = self.start_pos_y = size * start_y - size // 2
        elif self.start_side == "d":
            self.start_pos_x = size * start_x - size // 2
            self.start_pos_y = size * len(self.board) + size // 2

        self.board[end_x - 1][end_y - 1].set_as_end_block()

    def get_field_at(self, row, column):
        return self.board[row][column]

    def get_field_at_x_y(self, x, y):
        return self.board[int(y//self.size_of_one_field)][int(x//self.size_of_one_field)]

    def get_board_width(self):
        return len(self.board[0])

    def get_board_height(self):
        return len(self.board)

    def render(self, window):
        for row in range(self.get_board_height()):
            for column in range(self.get_board_width()):
                window.blit(self.get_field_at(row, column).get_image(),
                            (self.size_of_one_field * column, self.size_of_one_field * row))
                if (self.get_field_at(row, column).get_tower()):
                    self.get_field_at(row, column).get_tower().render(window, self.size_of_one_field * column + self.size_of_one_field // 2, self.size_of_one_field * row + self.size_of_one_field // 2)


    def get_size_of_one_field(self):
        return self.size_of_one_field

    def get_supposed_start_direction(self):
        if self.start_side == "l":
            return "r"
        elif self.start_side == "u":
            return "d"
        elif self.start_side == "r":
            return  "l"
        elif self.start_side == "d":
            return "u"

    def add_tower_to_field(self, tower, row, column):
        self.board[row][column].place_tower(tower)
        return (self.size_of_one_field * column + self.size_of_one_field // 2, self.size_of_one_field * row + self.size_of_one_field // 2)

    def get_start_pos(self):
        return (self.start_pos_x, self.start_pos_y)

    def get_middle_of_field(self, row, column):
        return (column * self.size_of_one_field + self.size_of_one_field // 2, row * self.size_of_one_field + self.size_of_one_field // 2)

    def get_middle_of_on_field_from_x_y(self, pos):
        return (pos[0]//self.size_of_one_field*self.size_of_one_field+self.size_of_one_field/2, pos[1]//self.size_of_one_field*self.size_of_one_field+self.size_of_one_field/2)