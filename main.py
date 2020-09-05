import pygame

import board
import enemy
import player
import projectile
import shop
import tower
import button
import text_box


class Game(object):
    current_player = None
    play_board = None
    enemy_manager = None
    projectile_manager = None
    tower_manager = None
    wave_manager = None
    shop = None
    bar = None
    selected_level = None

    def __init__(self):
        self.scale = 1
        self.state = "Menu"

        pygame.init()
        pygame.display.set_caption("Tower Defense")
        pygame.font.init()
        self.default_font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(30 * self.scale))

        self.window = pygame.display.set_mode(
            (int(100 * self.scale * 10),
             int(100 * self.scale * 5) + player.Bar.get_height_of_bar(self.scale) + 100 * self.scale))
        self.window_size = pygame.display.get_window_size()

        self.clock = pygame.time.Clock()

    def run(self):
        drag = False
        run = True

        while run:
            if self.state == "Menu":
                self.window.fill((84, 59, 31))
                buttons = [button.Button("Spiel starten", self.default_font, (0, 200), (48, 34, 18), self.window_size,
                                         self.window, center=True),
                           button.Button("Beenden", self.default_font, (0, 260), (48, 34, 18), self.window_size,
                                         self.window, center=True)]

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
                                elif a_button.get_text() == "Beenden":
                                    run = False

            elif self.state == "Level_picker":
                self.window.fill((84, 59, 31))
                text_levels = text_box.Text_box("Bitte Level wählen", self.default_font, (0, 140), self.window_size,
                                                self.window, center=True)
                buttons = [
                    button.Button("1", self.default_font, (400, 180), (48, 34, 18), self.window_size, self.window),
                    button.Button("Zurück", self.default_font, (10, 0), (48, 34, 18), self.window_size,
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
                self.start_level(self.selected_level)
                self.clock.tick()
                self.state = "Game"
            elif self.state == "Game":
                self.bar.set_buttons([button.Button("II", self.default_font, (0, 0), (48, 34, 18),
                                                    pygame.display.get_window_size(), self.window, center=True)])

                time_difference = self.clock.tick()

                if not self.current_player.is_dead():
                    self.play_board.render()
                    self.enemy_manager.manage()
                    self.wave_manager.manage(time_difference)
                    self.tower_manager.manage(time_difference)
                    self.projectile_manager.manage()
                    self.bar.render()
                    self.shop.render(self.window)
                    if drag:
                        self.shop.dragItem(index, pygame.mouse.get_pos(), self.window)
                    if self.wave_manager.get_all_waves_completed():
                        self.state = "Game_win"
                else:
                    self.state = "Game_Over"

                for a_button in self.bar.get_buttons():
                    if a_button.get_box().collidepoint(pygame.mouse.get_pos()):
                        a_button.hovered = True
                    else:
                        a_button.hovered = False
                    a_button.render()

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = event.pos
                        drag, index = self.shop.checkShopClick(pos[0], pos[1])
                        for a_button in self.bar.get_buttons():
                            if a_button.get_box().collidepoint(pos):
                                if a_button.get_text() == "II":
                                    self.state = "Pause_game"

                    elif drag and event.type == pygame.MOUSEBUTTONUP:
                        drag = False
                        row, column = self.play_board.get_row_and_column_from_x_y(event.pos[0], event.pos[1])
                        self.play_board.add_tower_to_field(
                            self.tower_manager.add_tower("bato", (row, column), self.play_board.get_size_of_one_field(),
                                                         player.Bar.get_height_of_bar(self.scale)), row, column)

            elif self.state == "Game_win":
                self.window.fill((83, 186, 69))
                big_font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(50 * self.scale))
                game_over_text = text_box.Text_box("Gewonnen", big_font,
                                                   (0, self.window_size[1] // 2 - 120 * self.scale), self.window_size,
                                                   self.window, center=True)
                buttons = [
                    button.Button("Endlosmodus", self.default_font, (0, self.window_size[1] // 2 - 40 * self.scale),
                                  (60, 133, 50), self.window_size, self.window, center=True),
                    button.Button("Hauptmenü", self.default_font,
                                  (0, self.window_size[1] // 2 + 10 * self.scale), (60, 133, 50), self.window_size,
                                  self.window, center=True),
                    button.Button("Beenden", self.default_font, (0, self.window_size[1] // 2 + 60 * self.scale),
                                  (60, 133, 50), self.window_size, self.window, center=True)]

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

            elif self.state == "Pause_game":
                self.bar.set_buttons([button.Button("Fortsetzen", self.default_font,
                                                    (self.window_size[0] // 4 - 20 * self.scale, 0), (48, 34, 18),
                                                    self.window_size, self.window),
                                      button.Button("Hauptmenü", self.default_font, (0, 0), (48, 34, 18),
                                                    self.window_size, self.window, center=True),
                                      button.Button("Beenden", self.default_font,
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

            elif self.state == "Game_Over":
                self.window.fill((255, 0, 0))
                big_font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(50 * self.scale))
                game_over_text = text_box.Text_box("Game over", big_font,
                                                   (0, self.window_size[1] // 2 - 120 * self.scale), self.window_size,
                                                   self.window, center=True)
                buttons = [button.Button("Neustart", self.default_font, (0, self.window_size[1] // 2 - 40 * self.scale),
                                         (158, 0, 0), self.window_size, self.window, center=True),
                           button.Button("Hauptmenü", self.default_font,
                                         (0, self.window_size[1] // 2 + 10 * self.scale), (158, 0, 0), self.window_size,
                                         self.window, center=True),
                           button.Button("Beenden", self.default_font, (0, self.window_size[1] // 2 + 60 * self.scale),
                                         (158, 0, 0), self.window_size, self.window, center=True)]

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

    def start_level(self, level_number):
        self.window.fill((0, 0, 0))
        self.current_player = player.Player()
        self.play_board = board.Board(self.scale, level_number, self.window)
        self.enemy_manager = enemy.Enemy_manager(self.play_board, self.current_player, self.scale, self.window)
        self.wave_manager = enemy.Wave_manager(self.enemy_manager)
        self.projectile_manager = projectile.Projectile_manager(self.enemy_manager, self.scale, self.window)
        self.tower_manager = tower.TowerManager(self.scale, self.enemy_manager, self.projectile_manager)
        self.bar = player.Bar(self.current_player, self.window, self.scale)
        self.shop = shop.Shop(0, self.play_board.get_board_height() * 100 * self.scale,
                              self.play_board.get_board_width() * self.scale * 100)
        self.time = 0

    pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
