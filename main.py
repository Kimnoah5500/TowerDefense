import pygame

from board import Board
from enemy import EnemyManager
from enemy import WaveManager
from player import Player
from player import Bar
from projectile import ProjectileManager
from shop import Shop
from tower import TowerManager
from button import Button
from text_box import Text_box
from pygame.surface import Surface
from pygame.time import Clock
from pygame.font import Font

class Game:
    """Class which provides functions for running and controlling the game.

    Attributes:
        current_player (Player): Player object which holds all the players data.
        play_board (Board): The currently loaded board with the fields and path on it.
        enemy_manager (EnemyManager): Used to manage all enemies which are currently on the board.
        projectile_manager (ProjectileManager): Used to manage all the projectiles that exist at the moment.
        tower_manager (TowerManager): Used to manage all the placed towers.
        wave_manager (WaveManager): Controls all actions related to the waves in which enemies are spawned.
        shop (Shop): Controls the shop which is shown on the bottom when the board is shown.
        bar (Bar): Controls actions in the top bar when the board is shown.
        selected_level (int): the number of the currently selected level used for restarting the current level.
        scale (float): Designed to adjust the size of the game.
        state (str): Current status of the game, normal flow is:
            "Menu": The menu screen where the player can start or end the game. -> Player clocks start game ->
            "Level_picker": Screen where the player can decide which level he wants to play. -> Player selects number.
                ->
            "Start_game": All managers and utilities will be set up for the selected level. -> Goes on implicitly. ->
            "Game": The selected level is running and gets rendered. -> Player clicks pause in top bar. ->
            "Game_pause": The enemies, towers and projectiles stop and player can decide if he continues, goes back to
                the main menu or ends the whole game. -> Player continues. -> Player loses all health points. ->
            "Game_over": Player is able to restart the level, go back to the main menu or end the game. OR -> Player
                defeats all enemy waves. ->
            "Game_win": Player is able to start endless mode, go back to the main menu or end the game.
        default_font (Font): Font object with preloaded font for rendering text.
        window (Surface): The surface where everything is rendered on.
        window_size (tuple): The window size in (x, y) pixels.
        clock (Clock): The clock which ticks in the background for time based actions.

    Author:
        Kim Matt
        Moritz Nueske
    """
    current_player: Player = None
    play_board: Board = None
    enemy_manager: EnemyManager = None
    projectile_manager: ProjectileManager = None
    tower_manager: TowerManager = None
    wave_manager: WaveManager = None
    shop: Shop = None
    bar: Bar = None
    selected_level: int = None

    def __init__(self):
        """Object that holds all relevant data for the game and is used for running the game.

        Author:
            Kim Matt
        """
        self.scale: float = 0.8
        self.state: str = "Menu"

        pygame.init()
        pygame.display.set_caption("Tower Defense")
        pygame.font.init()
        self.default_font: Font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(30 * self.scale))
        self.help_font: Font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(20 * self.scale))

        self.window: Surface = pygame.display.set_mode(
            (int(100 * self.scale * 15),
             int(100 * self.scale * 7 + Bar.get_height_of_bar(self.scale) + 100 * self.scale)))
        self.window_size: tuple = pygame.display.get_window_size()

        self.clock: Clock = pygame.time.Clock()

    def run(self):
        """Runs the game in a continuous loop till the player ends the game. Cycles through the different game states.

        Author:
            Kim Matt
            Moritz Nueske
        """
        drag: bool = False
        right_click_menu = None
        run: bool = True
        help_text_position = (0, 0)
        help_text: list = []
        help_image = None
        help_image_position = (0, 0)
        help_page_index: int = 0
        last_help_page_index: int = -1
        easter_egg_mode = False

        while run:
            if self.state == "Menu":
                self.window.fill((84, 59, 31))
                buttons = [Button("Spiel starten", self.default_font, (0, 250 * self.scale), (48, 34, 18), self.window_size,
                                  self.window, horizontal_center=True),
                           Button("Hilfe", self.default_font, (0, 320 * self.scale), (48, 34, 18), self.window_size,
                                  self.window, horizontal_center=True),
                           Button("Beenden", self.default_font, (0, 390 * self.scale), (48, 34, 18), self.window_size,
                                  self.window, horizontal_center=True)]

                for a_button in buttons:
                    if a_button.get_box().collidepoint(pygame.mouse.get_pos()):
                        a_button.hovered = True
                    else:
                        a_button.hovered = False
                    a_button.render()

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for a_button in buttons:
                            if a_button.get_box().collidepoint(pos):
                                if a_button.get_text() == "Spiel starten":
                                    self.state = "Level_picker"
                                elif a_button.get_text() == "Hilfe":
                                    self.state = "Help"
                                elif a_button.get_text() == "Beenden":
                                    run = False
            elif self.state == "Help":
                self.window.fill((84, 59, 31))

                if last_help_page_index != help_page_index:
                    help_text_file = open("./misc/help_texts/page_" + str(help_page_index))
                    help_text = []
                    help_image_position = help_text_file.readline().strip().split(",")
                    help_image_position = (int(help_image_position[0]), int(help_image_position[1]))
                    help_image_line = help_text_file.readline().split(",")
                    help_image = pygame.image.load('./misc/help_pictures/' + help_image_line[0] + '.png')
                    help_image = pygame.transform.scale(help_image, (int(int(help_image_line[1].strip()) * self.scale), int(int(help_image_line[2].strip()) * self.scale)))
                    help_text_position = help_text_file.readline().strip().split(",")
                    help_text_position = (int(help_text_position[0]), int(help_text_position[1]))
                    for line in help_text_file:
                        help_text.append(line.strip())
                    last_help_page_index = help_page_index
                self.window.blit(help_image, help_image_position)
                help_text_box = Text_box(help_text, self.help_font, help_text_position, self.window_size, self.window, heading_font=self.default_font)
                buttons = [
                    Button("Nächste Seite", self.default_font, (10 * self.scale, 0), (48, 34, 18), self.window_size,
                           self.window, right=True, vertical_center=True, rotation=-90),
                    Button("Vorherige Seite", self.default_font, (10 * self.scale, 0), (48, 34, 18), self.window_size,
                           self.window, left=True, vertical_center=True, rotation=90),
                    Button("Zurück", self.default_font, (10 * self.scale, 0), (48, 34, 18), self.window_size,
                           self.window, bottom=True)]

                help_text_box.render()
                for a_button in buttons:
                    if a_button.get_box().collidepoint(pygame.mouse.get_pos()):
                        a_button.hovered = True
                    else:
                        a_button.hovered = False
                    a_button.render()

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            for a_button in buttons:
                                if a_button.get_box().collidepoint(pos):
                                    if a_button.get_text() == "Zurück":
                                        self.state = "Menu"
                                    elif a_button.get_text() == "Nächste Seite":
                                        help_page_index += 1
                                        if help_page_index > 10:
                                            help_page_index = 0
                                    elif a_button.get_text() == "Vorherige Seite":
                                        help_page_index -= 1
                                        if help_page_index < 0:
                                            help_page_index = 10
                        elif event.button == 4:
                            help_page_index -= 1
                            if help_page_index < 0:
                                help_page_index = 11
                            if help_page_index == 11:
                                easter_egg_mode = not easter_egg_mode
                        elif event.button == 5:
                            help_page_index += 1
                            if help_page_index == 11:
                                easter_egg_mode = not easter_egg_mode
                            if help_page_index > 11:
                                help_page_index = 0

            elif self.state == "Level_picker":
                self.window.fill((84, 59, 31))
                text_levels = Text_box("Bitte Level wählen", self.default_font, (0, 140 * self.scale), self.window_size,
                                       self.window, center=True)
                buttons = [
                    Button("1", self.default_font, (400 * self.scale, 200 * self.scale), (48, 34, 18), self.window_size, self.window),
                    Button("2", self.default_font, (620 * self.scale, 200 * self.scale), (48, 34, 18), self.window_size, self.window),
                    Button("3", self.default_font, (840 * self.scale, 200 * self.scale), (48, 34, 18), self.window_size, self.window),
                    Button("4", self.default_font, (1080 * self.scale, 200 * self.scale), (48, 34, 18), self.window_size, self.window),
                    Button("Zurück", self.default_font, (10 * self.scale, 0), (48, 34, 18), self.window_size,
                           self.window, bottom=True)]

                text_levels.render()
                for a_button in buttons:
                    if a_button.get_box().collidepoint(pygame.mouse.get_pos()):
                        a_button.hovered = True
                    else:
                        a_button.hovered = False
                    a_button.render()

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for a_button in buttons:
                            if a_button.get_box().collidepoint(pos):
                                if a_button.get_text() == "Zurück":
                                    self.state = "Menu"
                                else:
                                    self.selected_level = a_button.get_text()
                                    self.state = "Start_game"
            elif self.state == "Start_game":
                self.start_level(self.selected_level, easter_egg_mode=easter_egg_mode)
                self.clock.tick()
                self.state = "Game"
            elif self.state == "Game":
                self.bar.set_buttons([Button("II", self.default_font, (0, 0), (48, 34, 18),
                                             pygame.display.get_window_size(), self.window, horizontal_center=True)])

                time_difference = self.clock.tick()

                if not self.current_player.is_dead():
                    self.play_board.render()
                    self.projectile_manager.manage()
                    self.enemy_manager.manage()
                    self.wave_manager.manage(time_difference)
                    self.tower_manager.manage(time_difference)
                    self.bar.render()
                    self.shop.render(self.window)
                    if drag:
                        self.shop.dragItem(index, pygame.mouse.get_pos(), self.window, self.tower_manager)
                    if self.wave_manager.get_all_waves_completed():
                        self.state = "Game_win"
                else:
                    self.state = "Game_over"

                for a_button in self.bar.get_buttons():
                    if a_button.get_box().collidepoint(pygame.mouse.get_pos()):
                        a_button.hovered = True
                    else:
                        a_button.hovered = False
                    a_button.render()

                if right_click_menu:
                    pygame.draw.rect(self.window, (255, 0,0 ), right_click_menu.get_box())
                    self.shop.draw_range(range_pos, self.window, range)
                    if right_click_menu.get_box().collidepoint(pygame.mouse.get_pos()):
                        right_click_menu.hovered = True
                    else:
                        right_click_menu.hovered = False
                    right_click_menu.render()

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = event.pos
                            drag, index = self.shop.checkShopClick(pos[0], pos[1], self.current_player)
                            for a_button in self.bar.get_buttons():
                                if a_button.get_box().collidepoint(pos):
                                    if a_button.get_text() == "II":
                                        self.state = "Game_pause"
                            if right_click_menu:
                                if right_click_menu.get_box().collidepoint(pos):
                                    self.current_player.add_money(self.tower_manager.remove_tower(
                                        self.play_board.remove_tower_from_field(
                                            self.play_board.get_row_and_column_from_x_y(right_click_menu.get_box().left,
                                                                                        right_click_menu.get_box().top))))
                                    right_click_menu = None
                                else:
                                    right_click_menu = None
                        elif event.button == 3:
                            clicked_field = self.play_board.get_field_at_x_y(pygame.mouse.get_pos())
                            if clicked_field and clicked_field.get_tower():
                                right_click_menu = Button("Verkaufen",
                                                          pygame.font.Font('./ressources/Alata-Regular.ttf',
                                                                           int(22 * self.scale)), (0, 0),
                                                          (158, 0, 0), self.window_size, self.window)
                                right_click_menu.set_pos((
                                    self.play_board.get_middle_of_field_from_x_y(pygame.mouse.get_pos())[
                                        0] - right_click_menu.get_box().width // 2,
                                    self.play_board.get_middle_of_field_from_x_y(pygame.mouse.get_pos())[
                                        1] + self.play_board.get_size_of_one_field() // 2 - right_click_menu.get_box().height))
                                range_pos = self.play_board.get_middle_of_field_from_x_y((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                                range = clicked_field.get_tower().range

                    elif drag and event.type == pygame.MOUSEBUTTONUP:
                        drag = False
                        if self.play_board.check_if_placeable(event.pos[0], event.pos[1]) and self.shop.buy_item(index,
                                                                                                                 self.current_player):
                            row, column = self.play_board.get_row_and_column_from_x_y(event.pos[0], event.pos[1])
                            self.play_board.add_tower_to_field(
                                self.tower_manager.add_tower(self.shop.get_item_code(index), (row, column),
                                                             self.play_board.get_size_of_one_field(),
                                                             Bar.get_height_of_bar(self.scale)), row, column)

            elif self.state == "Game_win":
                right_click_menu = None
                self.window.fill((83, 186, 69))
                big_font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(50 * self.scale))
                game_over_text = Text_box("Gewonnen", big_font,
                                          (0, self.window_size[1] // 2 - 120 * self.scale), self.window_size,
                                          self.window, center=True)
                buttons = [
                    Button("Endlosmodus", self.default_font, (0, self.window_size[1] // 2 - 40 * self.scale),
                           (60, 133, 50), self.window_size, self.window, horizontal_center=True),
                    Button("Hauptmenü", self.default_font,
                           (0, self.window_size[1] // 2 + 10 * self.scale), (60, 133, 50), self.window_size,
                           self.window, horizontal_center=True),
                    Button("Beenden", self.default_font, (0, self.window_size[1] // 2 + 60 * self.scale),
                           (60, 133, 50), self.window_size, self.window, horizontal_center=True)]

                game_over_text.render()
                for a_button in buttons:
                    if a_button.get_box().collidepoint(pygame.mouse.get_pos()):
                        a_button.hovered = True
                    else:
                        a_button.hovered = False
                    a_button.render()

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            run = False

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for a_button in buttons:
                            if a_button.get_box().collidepoint(pos):
                                if a_button.get_text() == "Endlosmodus":
                                    self.state = "Game"
                                    self.wave_manager.set_endless_mode()
                                elif a_button.get_text() == "Hauptmenü":
                                    self.state = "Menu"
                                elif a_button.get_text() == "Beenden":
                                    run = False

            elif self.state == "Game_pause":
                self.clock.tick()
                self.bar.set_buttons([Button("Fortsetzen", self.default_font,
                                             (self.window_size[0] // 4 - 20 * self.scale, 0), (48, 34, 18),
                                             self.window_size, self.window),
                                      Button("Hauptmenü", self.default_font, (0, 0), (48, 34, 18),
                                             self.window_size, self.window, horizontal_center=True),
                                      Button("Beenden", self.default_font,
                                             (self.window_size[0] // 4 * 3 - 100 * self.scale, 0),
                                             (48, 34, 18),
                                             self.window_size, self.window)])

                for a_button in self.bar.get_buttons():
                    if a_button.get_box().collidepoint(pygame.mouse.get_pos()):
                        a_button.hovered = True
                    else:
                        a_button.hovered = False
                    a_button.render()

                self.bar.render()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            run = False

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = event.pos
                        for a_button in self.bar.get_buttons():
                            if a_button.get_box().collidepoint(pos):
                                if a_button.get_text() == "Fortsetzen":
                                    self.state = "Game"
                                elif a_button.get_text() == "Hauptmenü":
                                    self.state = "Menu"
                                elif a_button.get_text() == "Beenden":
                                    run = False

            elif self.state == "Game_over":
                right_click_menu = None
                self.window.fill((255, 0, 0))
                big_font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(50 * self.scale))
                game_over_text = Text_box("Game over", big_font,
                                          (0, self.window_size[1] // 2 - 120 * self.scale), self.window_size,
                                          self.window, center=True)
                buttons = [Button("Neustart", self.default_font, (0, self.window_size[1] // 2 - 40 * self.scale),
                                  (158, 0, 0), self.window_size, self.window, horizontal_center=True),
                           Button("Hauptmenü", self.default_font,
                                  (0, self.window_size[1] // 2 + 10 * self.scale), (158, 0, 0), self.window_size,
                                  self.window, horizontal_center=True),
                           Button("Beenden", self.default_font, (0, self.window_size[1] // 2 + 60 * self.scale),
                                  (158, 0, 0), self.window_size, self.window, horizontal_center=True)]

                game_over_text.render()
                for a_button in buttons:
                    if a_button.get_box().collidepoint(pygame.mouse.get_pos()):
                        a_button.hovered = True
                    else:
                        a_button.hovered = False
                    a_button.render()

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    elif event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            run = False

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for a_button in buttons:
                            if a_button.get_box().collidepoint(pos):
                                if a_button.get_text() == "Neustart":
                                    self.state = "Start_game"
                                elif a_button.get_text() == "Hauptmenü":
                                    self.state = "Menu"
                                elif a_button.get_text() == "Beenden":
                                    run = False

    def start_level(self, level_number: str, easter_egg_mode: bool = False):
        """Sets up all the managers and utilities for running a specific level.

        Args:
            level_number (int): The number of the level which should be loaded.

        Author:
            Kim Matt
        """
        self.window.fill((0, 0, 0))
        self.current_player = Player()
        self.play_board = Board(self.scale, level_number, self.window)
        self.enemy_manager = EnemyManager(self.play_board, self.current_player, self.scale, self.window)
        self.wave_manager = WaveManager(self.enemy_manager)
        self.projectile_manager = ProjectileManager(self.enemy_manager, self.scale, self.window, easter_egg_mode)
        self.tower_manager = TowerManager(self.scale, self.enemy_manager, self.projectile_manager)
        self.bar = Bar(self.current_player, self.window, self.scale)
        self.shop = Shop((self.play_board.get_board_size()[0] * 100 * self.scale / 2) - 500 * self.scale, self.play_board.get_board_size()[1] * 100 * self.scale + Bar.get_height_of_bar(self.scale),
            self.scale, self.play_board.get_board_size()[0] * 100 * self.scale )

        self.time = 0


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
