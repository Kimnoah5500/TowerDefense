import pygame


class Player:
    """Class which holds player data such as health_point and money.

    Attributes:
        health_points (int): Number of the player's life points.
        money (int): money of the player with which items can be bought.

    Author:
        Kim Matt
    """
    health_points: int = 100
    money: int = 200

    def add_money(self, amount: int):
        """Adds money to players account balance.


        Args:
            amount (int): Amount of money to add.

        Author:
            Kim Matt
        """
        self.money += amount

    def reduce_money(self, amount: int):
        """Reduces the players account balance by given amount.

        Args:
            amount (int): Amount of money to reduce.

        Author:
            Kim Matt
        """
        self.money -= amount

    def get_current_money(self) -> int:
        """Returns the current account balance of the player.

        Returns:
            int: Current account balance of player

        Author:
            Kim Matt
        """
        return self.money

    def reduce_health_points(self, amount: int):
        """Reduces the player's health points by the stated value.

        Args:
            amount (int): Quantity of health points to be deducted.

        Author:
            Kim Matt
        """
        self.health_points -= amount

    def is_dead(self) -> bool:
        """Returns whether the players health points are below zero, so that the player is considered dead.

        Returns:
            bool: True when player is dead, false otherwise

        Author:
            Kim Matt
        """
        return self.health_points <= 0


class Bar:
    """Class with data and functions for the top bar in the play state of the game."""
    bar_height = 43

    @staticmethod
    def get_height_of_bar(scale) -> int:
        """Returns the height of the bar with the scale factor set in the main class.

        Returns:
            int: Height of bar with specified scale factor.

        Author:
            Kim Matt
        """
        return Bar.bar_height * scale

    def __init__(self, player: Player, window: pygame.SurfaceType, scale: float):
        """Top bar which shows player statistics.

        Args:
            player (Player): Player object with current stats and data from player.
            window (Surface): Surface on which the bar should be drawn.
            scale (float): Factor with which the game should be rendered.

        Author:
            Kim Matt
        """
        self.scale = scale
        self.window = window
        self.player = player
        pygame.font.init()
        self.default_font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(30 * scale))
        self.hearth_image = pygame.image.load('./ressources/interface/hearth.png')
        self.hearth_image = pygame.transform.scale(self.hearth_image, (int(scale * 30), int(scale * 30)))
        self.coin_image = pygame.image.load('./ressources/interface/coin.png')
        self.coin_image = pygame.transform.scale(self.coin_image, (int(scale * 30), int(scale * 30)))
        self.buttons = []

    def get_buttons(self) -> list:
        """Returns all buttons which the top bar currently holds.

        Returns:
            list: All buttons from the top bar
        """
        return self.buttons

    def set_buttons(self, buttons: list):
        """Sets a list of buttons as those buttons which should currently be shown in top bar.

        Args:
            buttons (list): List of buttons which should be shown.

        Author:
            Kim Matt
        """
        self.buttons = buttons

    def render(self):
        """Renders the top bar with current health point and coin count, as well as the buttons which have been set in
        bar object.

        Author:
            Kim Matt
        """
        pygame.draw.rect(self.window, (84, 59, 31),
                         pygame.Rect((0, 0), (pygame.display.get_window_size()[0], self.bar_height * self.scale)))
        health_points_text = self.default_font.render(str(self.player.health_points), False, (255, 255, 255))
        money_text = self.default_font.render(str(self.player.money), False, (255, 255, 255))
        self.window.blit(self.hearth_image, (5 * self.scale, 5 * self.scale))
        self.window.blit(health_points_text, (self.hearth_image.get_rect().width + 10 * self.scale, 0))
        self.window.blit(self.coin_image, (
        pygame.display.get_window_size()[0] - 5 * self.scale - self.coin_image.get_rect().width, 5 * self.scale))
        self.window.blit(money_text, (pygame.display.get_window_size()[
                                          0] - money_text.get_rect().width - 10 * self.scale - self.coin_image.get_rect().width,
                                      0))
        for a_button in self.buttons:
            a_button.render()
