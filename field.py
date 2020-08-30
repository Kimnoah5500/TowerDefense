import pygame

class Field:
    end_block = False
    tower = False
    def __init__(self, size):
        self.size = size

    def get_image(self):
        return self.image

    def get_field_code(self):
        return self.field_code

    def set_as_end_block(self):
        self.end_block = True

    def is_end_block(self):
        return self.end_block

    def place_tower(self, tower):
        self.tower = tower

    def get_tower(self):
        return self.tower

class Way_field(Field):
    def __init__(self, size):
        Field.__init__(self, size)

class Straight_way_field_hotizontal(Way_field):
    def __init__(self, size):
        Way_field.__init__(self, size)
        self.image = pygame.image.load('./ressources/Path_straight.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.field_code = "sh"

class Straight_way_field_vertikal(Way_field):
    def __init__(self, size):
        Way_field.__init__(self, size)
        self.image = pygame.image.load('./ressources/Path_straight.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, 90)
        self.field_code = "sv"

class Edge_way_field_left_up(Way_field):
    def __init__(self, size):
        Way_field.__init__(self, size)
        self.image = pygame.image.load('./ressources/Path_edge.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.field_code = "elu"

class Edge_way_field_right_up(Way_field):
    def __init__(self, size):
        Way_field.__init__(self, size)
        self.image = pygame.image.load('./ressources/Path_edge.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, 270)
        self.field_code = "eru"

class Edge_way_field_left_down(Way_field):
    def __init__(self, size):
        Way_field.__init__(self, size)
        self.image = pygame.image.load('./ressources/Path_edge.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, 90)
        self.field_code = "eld"

class Edge_way_field_right_down(Way_field):
    def __init__(self, size):
        Way_field.__init__(self, size)
        self.image = pygame.image.load('./ressources/Path_edge.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, 180)
        self.field_code = "erd"

class Empty_Field(Field):
    def __init__(self, size):
        Field.__init__(self, size)
        self.image = pygame.image.load('./ressources/Field_empty.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.field_code = "ey"