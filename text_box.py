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

    def __init__(self, text: str, font: Font,  pos: tuple, window_size: tuple, window: Surface, center: bool = False,
                 bottom: bool = False, heading_font=None):
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
        self.heading_font = heading_font
        self.font = font
        if isinstance(text, str):
            self.text = text
        elif isinstance(text, list):
            self.text = []
            for line in text:
                self.text.append(line)

        self.window = window
        self.window_size = window_size
        self.pos = pos
        self.center = center
        self.bottom = bottom

    def render(self):
        """Renders the text box.

        Author:
            Kim Matt
        """
        if isinstance(self.text, list):
            pos = self.pos
            for line in self.text:
                if not line:
                    pos = list(pos)
                    pos[1] += self.font.get_height()
                    pos = tuple(pos)
                elif line[0] == '#':
                    self.window.blit(self.heading_font.render(line[1:], True, (255, 255, 255)), pos)
                    pos = list(pos)
                    pos[1] += self.heading_font.get_height()
                    pos = tuple(pos)
                else:
                    self.window.blit(self.font.render(line, True, (255, 255, 255)), pos)
                    pos = list(pos)
                    pos[1] += self.font.get_height()
                    pos = tuple(pos)
        else:
            text_box: Surface = self.font.render(self.text, True, (255, 255, 255))
            if self.center:
                pos_list = list(self.pos)
                pos_list[0] = int(self.window_size[0] // 2 - text_box.get_rect().width // 2)
                pos_list[1] = int(pos_list[1])
                self.pos = tuple(pos_list)
            elif self.bottom:
                pos_list = list(self.pos)
                pos_list[0] = int(pos_list[0])
                pos_list[1] = int(self.window_size[1] - text_box.get_rect().height)
                self.pos = tuple(pos_list)
            self.window.blit(text_box, self.pos)
