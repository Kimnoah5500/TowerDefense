class Text_box:
    def __init__(self, text, font, pos, window_size, window, center = False, bottom = False):
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
        if isinstance(self.text_box, list):
            line_index = 0
            for line in self.text_box:
                self.window.blit(line, (self.pos[0], self.pos[1] + line_index * self.text_size))
                line_index += 1
        else:
            self.window.blit(self.text_box, self.pos)