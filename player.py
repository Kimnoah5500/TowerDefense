import pygame

class Player:
    health_points = 100
    money = 200

    def add_money(self, amount):
        self.money += amount

    def get_current_money(self):
        return self.money
    
    def reduce_money(self, amount):
        self.money -= amount

    def reduce_health_points(self, amount):
        self.health_points -= amount

    def is_dead(self):
        return self.health_points <= 0

class Bar:
    bar_height = 43

    @staticmethod
    def get_height_of_bar():
        return Bar.bar_height

    def __init__(self, player, window, scale):
        self.scale = scale
        self.bar_height = 43 * scale
        self.window = window
        self.player = player
        pygame.font.init()
        self.default_font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(30 * scale))
        self.hearth_image = pygame.image.load('./ressources/interface/hearth.png')
        self.hearth_image = pygame.transform.scale(self.hearth_image, (int(scale * 30), int(scale * 30)))
        self.coin_image = pygame.image.load('./ressources/interface/coin.png')
        self.coin_image = pygame.transform.scale(self.coin_image, (int(scale * 30), int(scale * 30)))
        self.buttons = []

    def get_buttons(self):
        return self.buttons

    def set_buttons(self, buttons):
        self.buttons = buttons

    def render(self):
        pygame.draw.rect(self.window, (84, 59, 31), pygame.Rect((0, 0), (pygame.display.get_window_size()[0], self.bar_height * self.scale)))
        health_points_text = self.default_font.render(str(self.player.health_points), False, (255, 255, 255))
        money_text = self.default_font.render(str(self.player.money), False, (255, 255, 255))
        self.window.blit(self.hearth_image, (5 * self.scale, 5 * self.scale))
        self.window.blit(health_points_text, (self.hearth_image.get_rect().width + 10 * self.scale, 0))
        self.window.blit(self.coin_image, (pygame.display.get_window_size()[0] - 5 * self.scale - self.coin_image.get_rect().width, 5 * self.scale))
        self.window.blit(money_text, (pygame.display.get_window_size()[0] - money_text.get_rect().width - 10 * self.scale - self.coin_image.get_rect().width, 0))
        for a_button in self.buttons:
            a_button.render()