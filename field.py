import pygame
import random
from tower import Tower


class Field:
    """Class with basic attributes from fields which holds the tower on the specific field.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field.
        size (int): Size of one field in pixel.

    Author:
        Kim Matt
    """
    end_block: bool = False
    tower: Tower = False

    def __init__(self, size: int):
        """Basic field to extend other types from.

        Args:
            size (int): Size of field in pixel.
        """
        self.size = size

    def get_image(self) -> pygame.SurfaceType:
        """Returns the image of the field as an pygame surface.

        Returns:
            SurfaceType: Image of field.

        Author:
            Kim Matt
        """
        return self.image

    def get_field_code(self):
        """Returns the field code of the field. (sv: Straight vertical, sh: Straight horizontal, elu: Edge left up,
        eld: Edge left down, eru: Edge right up, erd: Edge right down).

        Returns:
            str: Field code of field.

        Author:
            Kim Matt
        """
        return self.field_code

    def set_as_end_block(self):
        """Sets this field as end of the path for the enemies.

        Author:
            Kim Matt
        """
        self.end_block = True

    def is_end_block(self):
        """Returns whether this field is the end of the path.

        Returns:
            bool: True if this field is the end, else false.

        Author:
            Kim Matt
        """
        return self.end_block

    def place_tower(self, tower: Tower):
        """Places a tower onto this field.

        Args:
            tower (Tower): Tower which should be placed.

        Author:
            Kim Matt
        """
        self.tower = tower

    def remove_tower(self) -> Tower:
        """Removes the tower from this field.

        Returns:
            Tower: Tower which has been removed from this field.

        Author:
            Kim Matt
        """
        tower = self.tower
        self.tower = False
        return tower

    def get_tower(self) -> Tower:
        """Returns the tower on this field.

        Returns:
            Tower: Tower which has been placed on this field.

        Author:
            Kim Matt
        """
        return self.tower


class PathField(Field):
    """Class that contains data for a path field.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field although no tower can be placed on a path field.
        size (int): Size of one field in pixel.

    Author:
            Kim Matt
    """

    def __init__(self, size):
        """Field with path on it.

        Args:
            size (int): Size of field in pixel.

        Author:
            Kim Matt
        """
        Field.__init__(self, size)


class StraightPathFieldHorizontal(PathField):
    """Class that contains data for a field with a straight horizontal path.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field although no tower can be placed on a path field.
        size (int): Size of one field in pixel.
        image (SurfaceType): Image with a straight horizontal path as pygame surface.
        field_code (str): Code which indicates the type of field.

    Author:
            Kim Matt
    """
    def __init__(self, size):
        """Field with a straight horizontal path on it.

        Args:
            size (int): Size of field in pixel.

        Author:
            Kim Matt
        """
        PathField.__init__(self, size)
        field_selector = random.randint(1, 3)
        if field_selector == 1:
            self.image = pygame.image.load('./ressources/fields/Path_straight_1.png')
        elif field_selector == 2:
            self.image = pygame.image.load('./ressources/fields/Path_straight_2.png')
        else:
            self.image = pygame.image.load('./ressources/fields/Path_straight_3.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.field_code = "sh"


class StraightPathFieldVertical(PathField):
    """Class that contains data for a field with a straight vertical path.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field although no tower can be placed on a path field.
        size (int): Size of one field in pixel.
        image (SurfaceType): Image with a straight vertical path as pygame surface.
        field_code (str): Code which indicates the type of field.

    Author:
        Kim Matt
    """
    def __init__(self, size):
        """Field with a straight vertical path on it.

        Args:
            size (int): Size of field in pixel.

        Author:
            Kim Matt
        """
        PathField.__init__(self, size)
        field_selector = random.randint(1, 3)
        if field_selector == 1:
            self.image = pygame.image.load('./ressources/fields/Path_straight_1.png')
        elif field_selector == 2:
            self.image = pygame.image.load('./ressources/fields/Path_straight_2.png')
        else:
            self.image = pygame.image.load('./ressources/fields/Path_straight_3.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, 90)
        self.field_code = "sv"


class EdgePathFieldLeftUp(PathField):
    """Class that contains data for a field with a edge path that has connections on the left and upper side.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field although no tower can be placed on a path field.
        size (int): Size of one field in pixel.
        image (SurfaceType): Image with a edge path that has connections on the left and upper side as pygame surface.
        field_code (str): Code which indicates the type of field.

    Author:
        Kim Matt
    """
    def __init__(self, size):
        """Field with a edge path that has connections on the left and upper side on it.

        Args:
            size (int): Size of field in pixel.

        Author:
            Kim Matt
        """
        PathField.__init__(self, size)
        field_selector = random.randint(1, 3)
        if field_selector == 1:
            self.image = pygame.image.load('./ressources/fields/Path_edge_1.png')
        elif field_selector == 2:
            self.image = pygame.image.load('./ressources/fields/Path_edge_2.png')
        else:
            self.image = pygame.image.load('./ressources/fields/Path_edge_3.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.field_code = "elu"


class EdgePathFieldRightUp(PathField):
    """Class that contains data for a field with a edge path that has connections on the right and upper side.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field although no tower can be placed on a path field.
        size (int): Size of one field in pixel.
        image (SurfaceType): Image with a edge path that has connections on the right and upper side as pygame surface.
        field_code (str): Code which indicates the type of field.

    Author:
        Kim Matt
    """
    def __init__(self, size):
        """Field with a edge path that has connections on the right and upper side on it.

        Args:
            size (int): Size of field in pixel.

        Author:
            Kim Matt
        """
        PathField.__init__(self, size)
        field_selector = random.randint(1, 3)
        if field_selector == 1:
            self.image = pygame.image.load('./ressources/fields/Path_edge_1.png')
        elif field_selector == 2:
            self.image = pygame.image.load('./ressources/fields/Path_edge_2.png')
        else:
            self.image = pygame.image.load('./ressources/fields/Path_edge_3.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, 270)
        self.field_code = "eru"


class EdgePathFieldLeftDown(PathField):
    """Class that contains data for a field with a edge path that has connections on the left and lower side.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field although no tower can be placed on a path field.
        size (int): Size of one field in pixel.
        image (SurfaceType): Image with a edge path that has connections on the left and lower side as pygame surface.
        field_code (str): Code which indicates the type of field.

    Author:
        Kim Matt
    """
    def __init__(self, size):
        """Field with a edge path that has connections on the left and lower side on it.

        Args:
            size (int): Size of field in pixel.

        Author:
            Kim Matt
        """
        PathField.__init__(self, size)
        field_selector = random.randint(1, 3)
        if field_selector == 1:
            self.image = pygame.image.load('./ressources/fields/Path_edge_1.png')
        elif field_selector == 2:
            self.image = pygame.image.load('./ressources/fields/Path_edge_2.png')
        else:
            self.image = pygame.image.load('./ressources/fields/Path_edge_3.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, 90)
        self.field_code = "eld"


class EdgePathFieldRightDown(PathField):
    """Class that contains data for a field with a edge path that has connections on the right and lower side.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field although no tower can be placed on a path field.
        size (int): Size of one field in pixel.
        image (SurfaceType): Image with a edge path that has connections on the right and lower side as pygame surface.
        field_code (str): Code which indicates the type of field.

    Author:
        Kim Matt
    """
    def __init__(self, size):
        """Field with a edge path that has connections on the right and lower side on it.

        Args:
            size (int): Size of field in pixel.

        Author:
            Kim Matt
        """
        PathField.__init__(self, size)
        field_selector = random.randint(1, 3)
        if field_selector == 1:
            self.image = pygame.image.load('./ressources/fields/Path_edge_1.png')
        elif field_selector == 2:
            self.image = pygame.image.load('./ressources/fields/Path_edge_2.png')
        else:
            self.image = pygame.image.load('./ressources/fields/Path_edge_3.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, 180)
        self.field_code = "erd"


class EmptyField(Field):
    """Class that contains data for a empty field.

    Attributes:
        end_block (bool): Indicates if this field is the end of the path.
        tower (Tower): Tower on this field.
        size (int): Size of one field in pixel.
        image (SurfaceType): Image with a edge path that has connections on the right and lower side as pygame surface.
        field_code (str): Code which indicates the type of field.

    Author:
        Kim Matt
    """
    def __init__(self, size):
        """Field with no path on it.

        Args:
            size (int): Size of field in pixel.

        Author:
            Kim Matt
        """
        Field.__init__(self, size)
        self.image = pygame.image.load('./ressources/fields/Field_empty.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.field_code = "ey"
