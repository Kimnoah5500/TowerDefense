import csv

from pygame.surface import Surface

from field import *
from field import PathField
from player import Bar
from shop import Shop


class Board:
    """Class which holds the currently selected board and its fields.

    Attributes:
        size_of_one_field (int): Size of a field depending on the selected scaling.
        board (list): list which contains the rows of the board, which in turn consists of a list which contains all
            fields of the rows.
        window (Surface): Surface on which the board is to be rendered.
        top_offset (int): The offset resulting from the bar rendered at the upper portion of the screen.
        start_side (str): The side from which the opponents should run into the field of vision of the player.
        start_pos (tuple): Pixel coordinates on which the enemies should start.

    Author:
        Kim Matt
        Moritz Nueske
    """

    def __init__(self, scale: float, level_number: int, window: Surface):
        """Initializes the board with the selected level number.

        Args:
            scale (float): The value in which the game is scaled.
            level_number (int): The level which should be loaded.
            window (Surface): The surface on which the board should be rendered.

        Author:
            Kim Matt
        """
        self.size_of_one_field = int(100 * scale)
        self.board = []
        self.window = window
        self.top_offset = int(Bar.get_height_of_bar(scale))
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
                        self.board[row_number - 1].append(EmptyField(self.size_of_one_field))
                    elif cell == "sh":
                        self.board[row_number - 1].append(StraightPathFieldHorizontal(self.size_of_one_field))
                    elif cell == "sv":
                        self.board[row_number - 1].append(StraightPathFieldVertical(self.size_of_one_field))
                    elif cell == "elu":
                        self.board[row_number - 1].append(EdgePathFieldLeftUp(self.size_of_one_field))
                    elif cell == "eld":
                        self.board[row_number - 1].append(EdgePathFieldLeftDown(self.size_of_one_field))
                    elif cell == "eru":
                        self.board[row_number - 1].append(EdgePathFieldRightUp(self.size_of_one_field))
                    elif cell == "erd":
                        self.board[row_number - 1].append(EdgePathFieldRightDown(self.size_of_one_field))
            row_number += 1

        if self.start_side == "l":
            self.start_pos = (-self.size_of_one_field // 2,
                              self.size_of_one_field * start_y - self.size_of_one_field // 2 + self.top_offset)
        elif self.start_side == "u":
            self.start_pos = (self.size_of_one_field * start_x - self.size_of_one_field // 2,
                              -self.size_of_one_field // 2 + self.top_offset)
        elif self.start_side == "r":
            self.start_pos = (self.size_of_one_field * len(self.board[0]) + self.size_of_one_field // 2,
                              self.size_of_one_field * start_y - self.size_of_one_field // 2 + self.top_offset)
        elif self.start_side == "d":
            self.start_pos = (self.size_of_one_field * start_x - self.size_of_one_field // 2,
                              self.size_of_one_field * len(self.board) + self.size_of_one_field // 2 + self.top_offset)

        self.board[end_x - 1][end_y - 1].set_as_end_block()

    def get_field_at(self, row: int, column: int) -> Field:
        """Returns the field in the given row and column.

        Args:
            row (int): Row of the field.
            column (int): Column of the field.

        Returns:
            Field: Field in searched position.

        Author:
            Kim Matt
        """
        return self.board[row][column]

    def get_field_at_x_y(self, coordinates: tuple) -> Field:
        """Returns the field which is located at the selected coordinates or None when there is no field.

        Args:
            coordinates (tuple): Coordinates at which the field is searched.

        Returns:
            Field: The searched field.
            None: No field found at this position.

        Author:
            Kim Matt
        """
        if 0 <= coordinates[0] <= pygame.display.get_window_size()[0] and self.top_offset < coordinates[1] < \
                pygame.display.get_window_size()[
                    1] - Shop.height:
            return self.board[int((coordinates[1] - self.top_offset) // self.size_of_one_field)][
                int(coordinates[0] // self.size_of_one_field)]
        else:
            return None

    def get_board_size(self) -> tuple:
        """Returns the board width.

        Returns:
            tuple: Board width and height.

        Author:
            Kim Matt
        """
        return len(self.board[0]), len(self.board)

    def render(self):
        """Renders the board with all its fields.

        Author:
            Kim Matt
        """
        for row in range(self.get_board_size()[1]):
            for column in range(self.get_board_size()[0]):
                self.window.blit(self.get_field_at(row, column).get_image(),
                                 (self.size_of_one_field * column, self.size_of_one_field * row + self.top_offset))
                if self.get_field_at(row, column).get_tower():
                    self.get_field_at(row, column).get_tower().render(self.window)

    def get_size_of_one_field(self) -> int:
        """Returns the side length of one of the square fields.

        Returns:
            int: Side length of one of the square fields.

        Author:
            Kim Matt
        """
        return self.size_of_one_field

    def get_supposed_start_direction(self) -> str:
        """Returns the direction in which the enemies should run at the beginning.

        Returns:
            str: The Direction in which the enemy should run (r: right, d: down, l: left, u: up).

        Author:
            Kim Matt
        """
        if self.start_side == "l":
            return "r"
        elif self.start_side == "u":
            return "d"
        elif self.start_side == "r":
            return "l"
        elif self.start_side == "d":
            return "u"

    def add_tower_to_field(self, tower: Tower, row: int, column: int):
        """Place the given tower on the field with the given row and column.

        Args:
            tower (Tower): The tower to be placed.
            row (int): The row in which the tower should be placed.
            column (int): The column in which the tower should be placed.

        Author:
            Kim Matt
        """
        self.board[row][column].place_tower(tower)

    def remove_tower_from_field(self, row_column: tuple) -> Tower:
        """Remove the tower from the field with given row and column.

        Args:
            row_column (tuple): Row and column in which the tower should be removed.

        Returns:
            Tower: The tower which had been removed to remove the specific tower in the tower manager.

        Author:
            Kim Matt
        """
        return self.board[row_column[0]][row_column[1]].remove_tower()

    def get_start_pos(self) -> tuple:
        """Returns the pixel position in which the enemies should start their way.

        Returns:
            tuple: X and Y coordinates where the enemies should start.

        Author:
            Kim Matt
        """
        return self.start_pos

    def get_middle_of_field_from_x_y(self, pos: tuple) -> tuple:
        """Returns the pixel co-ordinates of the centre of the field to the selected X and Y coordinates.

        Args:
            pos: X and Y coordinates of the field from which the middle is searched.

        Returns:
            tuple: The X and Y coordinates of the middle.

        Author:
            Kim Matt
        """
        return (
            int(pos[0] // self.size_of_one_field * self.size_of_one_field + self.size_of_one_field / 2),
            int((pos[
                     1] - self.top_offset) // self.size_of_one_field * self.size_of_one_field + self.size_of_one_field
                / 2) + self.top_offset)

    def get_row_and_column_from_x_y(self, x: int, y: int) -> tuple:
        """Returns the row and column from the given X and Y coordinates.

        Args:
            x: X coordinate for searching the row.
            y: Y coordinate for searching the column.

        Returns:
            tuple: Row and column number.

        Author:
            Moritz Nueske
        """
        return int((y - self.top_offset) // self.size_of_one_field), int(x // self.size_of_one_field)

    def check_if_placeable(self, x: int, y: int) -> bool:
        """Check whether a tower can be placed at the x, y position.

        Args:
            x: X position for the test.
            y: Y position for the test.

        Returns:
            bool: True when a tower is placeable at the given position, False if not.

        Author:
            Moritz Nueske
        """
        check_field = self.get_field_at_x_y((x, y))

        if check_field and not check_field.tower and not isinstance(check_field, PathField):
            return True
        else:
            return False
