from pygame.font import Font
from pygame.surface import Surface


class Text_box:
    """Utility class for creating and rendering a text box in pygame.

    Attributes:
        text_size (int): Height of the line.
        text_box (Surface/list): The box with the text in it or a list with text boxes.
        window (Surface): The surface the textbox should be rendered on.
        pos: the position in which the text box should be rendered.

    Author:
        Kim Matt
    """

    def __init__(self, text: str, font: Font, pos: tuple, window_size: tuple, window: Surface, center: bool = False,
                 bottom: bool = False):
        """Creates a text box at given position with given text.

        Args:
            text (str): The text that appears in the button.
            font (Font): Font in which the text inside the button is rendered.
            pos (tuple): The X and Y coordinates in which the button should be rendered.
            window_size (tuple): The size of the window for placing the button int he center or at the bottom.
            window (Surface): The surface on which the button should be rendered.
            center (bool): Centers the button horizontally, default: False.
            bottom (bool): Places the button at the bottom of the window, default: False.

        Author:
            Kim Matt
        """
        self.text_size = font.get_height()
        if isinstance(text, str):
            self.text_box = font.render(text, True, (255, 255, 255))
        elif isinstance(text, list):
            self.text_box = []
            for line in text:
                self.text_box.append(font.render(line, True, (255, 255, 255)))

        self.window = window
        self.pos = pos
        if center:
            pos_list = list(self.pos)
            pos_list[0] = window_size[0] // 2 - self.text_box.get_rect().width // 2
            self.pos = tuple(pos_list)
        elif bottom:
            pos_list = list(self.pos)
            pos_list[1] = window_size[1] - self.text_box.get_rect().height
            self.pos = tuple(pos_list)

    def render(self):
        """Renders the text box.

        Author:
            Kim Matt
        """
        if isinstance(self.text_box, list):
            line_index = 0
            for line in self.text_box:
                self.window.blit(line, (self.pos[0], self.pos[1] + line_index * self.text_size))
                line_index += 1
        else:
            self.window.blit(self.text_box, self.pos)
