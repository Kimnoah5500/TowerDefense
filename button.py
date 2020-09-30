import pygame

from pygame.font import Font
from pygame.surface import Surface


class Button:
    """Utility class for creating and rendering a button in pygame.

    Attributes:
        hovered (bool): Specifies if the mouse pointer currently hovers over the button.
        font (Font): Font in which the text inside the button is rendered.
        text (str): The text that appears in the button.
        window (Surface): The surface on which the button should be rendered.
        text_box (Surface): The box which holds the text of the button.
        box (Surface): The box which sits around the button for hovering effect.
        hover_color (tuple): The color in which the button should be rendered when the mouse hovers over it.
        pos (tuple): The X and Y coordinates in which the button should be rendered.

    Author:
        Kim Matt
    """
    hovered = False

    def __init__(self, text: str, font: Font, pos: tuple, hover_color: tuple, window_size: tuple, window: Surface,
                 horizontal_center: bool = False, vertical_center: bool = False, bottom: bool = False, left: bool = False, right: bool = False, rotation: int = 0):
        """Creates a button with hover effect.

        Args:
            text (str): The text that appears in the button.
            font (Font): Font in which the text inside the button is rendered.
            pos (tuple): The X and Y coordinates in which the button should be rendered.
            hover_color (tuple): The color in which the button should be rendered when the mouse hovers over it.
            window_size (tuple): The size of the window for placing the button int he center or at the bottom.
            window (Surface): The surface on which the button should be rendered.
            horizontal_center (bool): Centers the button horizontally, default: False.
            bottom (bool): Places the button at the bottom of the window, default: False.

        Author:
            Kim Matt
        """
        self.font = font
        self.text = text
        self.window = window
        self.text_box = font.render(self.text, True, (255, 255, 255))
        self.hover_color = hover_color

        self.pos = pos

        if rotation != 0:
            self.text_box = pygame.transform.rotate(self.text_box, rotation)

        if horizontal_center:
            pos_list = list(self.pos)
            pos_list[0] = window_size[0] // 2 - self.text_box.get_rect().width // 2
            self.pos = tuple(pos_list)
        elif right:
            pos_list = list(self.pos)
            pos_list[0] = window_size[0] - self.text_box.get_rect().width - self.font.get_height() // 2
            self.pos = tuple(pos_list)
        elif left:
            pos_list = list(self.pos)
            pos_list[0] = 0 + self.font.get_height() // 2
            self.pos = tuple(pos_list)
        if bottom:
            pos_list = list(self.pos)
            pos_list[1] = window_size[1] - self.text_box.get_rect().height
            self.pos = tuple(pos_list)
        elif vertical_center:
            pos_list = list(self.pos)
            pos_list[1] = window_size[1] // 2 - self.text_box.get_rect().height // 2
            self.pos = tuple(pos_list)

        self.box = self.text_box.get_rect()
        self.box.topleft = self.pos

    def set_pos(self, pos: tuple):
        """Sets the position of the button.

        Args:
            pos (tuple): X and Y coordinates in which the button should appear.

        Author:
            Kim Matt
        """
        self.pos = pos
        self.box.topleft = pos

    def get_box(self):
        """Returns the box around the button.

        Returns:
            Surface: The box around the button.

        Author:
            Kim Matt
        """
        return self.box

    def get_text(self):
        """Returns the text which is in the button.

        Returns:
            str: The text from the button.

        Author:
            Kim Matt
        """
        return self.text

    def render(self):
        """Renders the button. When mouse hovers over the button, it is rendered in the hover color.

        Author:
            Kim Matt
        """
        if self.hovered:
            pygame.draw.rect(self.window, self.hover_color, self.box)
        self.window.blit(self.text_box, self.pos)
