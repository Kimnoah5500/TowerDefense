import pygame


class Button:
    hovered = False

    def __init__(self, text, font, pos, hover_color, window_size, window, center=False, bottom=False):
        self.font = font
        self.text = text
        self.window = window
        self.window_size = window_size
        self.text_box = font.render(self.text, True, (255, 255, 255))
        self.hover_color = hover_color
        self.center = center
        self.bottom = bottom

        self.pos = pos
        if center:
            pos_list = list(self.pos)
            pos_list[0] = window_size[0] // 2 - self.text_box.get_rect().width // 2
            self.pos = tuple(pos_list)
        elif bottom:
            pos_list = list(self.pos)
            pos_list[1] = window_size[1] - self.text_box.get_rect().height
            self.pos = tuple(pos_list)

        self.box = self.text_box.get_rect()
        self.box.topleft = self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_box(self):
        return self.box

    def get_text(self):
        return self.text

    def render(self):
        self.text_box = self.font.render(self.text, True, (255, 255, 255))
        if self.hovered:
            pygame.draw.rect(self.window, self.hover_color, self.box)
        self.window.blit(self.text_box, self.pos)
