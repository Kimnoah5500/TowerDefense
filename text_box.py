class Text_box:
    def __init__(self, text, font, pos, window_size, window, center = False, bottom = False):
        self.text = text
        self.window = window
        self.text_box = font.render(self.text, True, (255, 255, 255))

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
        self.window.blit(self.text_box, self.pos)