import pygame
import board
import enemy
import tower
import projectile
import player as Player

scale = 1
state = "Game"

pygame.init()
pygame.font.init()
default_font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(30 * scale))

#pygame.display.Info().current_w
#pygame.display.Info().current_h
#pygame.FULLSCREEN
window = pygame.display.set_mode((int(100 * scale * 10), int(100 * scale * 5) + Player.Bar.get_height_of_bar()), )
window_size = pygame.display.get_window_size()

pygame.display.set_caption("Tower Defense")

x = 50
y = 50
width = 80
height = 80
vel = 5
clock = pygame.time.Clock()

imageTest = pygame.image.load('./ressources/Test.png')
imageTest = pygame.transform.scale(imageTest, (width, height))

player = Player.Player()
play_board = board.Board(scale, window)
enemy_manager = enemy.Enemy_manager(play_board, player, scale, window)
projectile_manager = projectile.Projectile_manager(enemy_manager, scale, window)
tower_manager = tower.TowerManager(scale, enemy_manager, projectile_manager)
bar = Player.Bar(player, window, scale)
game_over_screen_shown = False

test_pos = play_board.get_middle_of_field(2, 5)
test_pos_2 = play_board.get_middle_of_field(2, 2)
test_pos_3 = play_board.get_middle_of_field(2, 0)
test_tower = play_board.add_tower_to_field(tower_manager.add_tower("lol", test_pos), 2, 5)
test_tower_2 = play_board.add_tower_to_field(tower_manager.add_tower("lol", test_pos_2), 2, 2)
test_tower_3 = play_board.add_tower_to_field(tower_manager.add_tower("lol", test_pos_3), 2, 0)

time_since_last_action = 0

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # if event.type == pygame.JOYAXISMOTION:
        #
        #     if (0.1 < joystickTest.get_axis(0)):
        #         x += vel * joystickTest.get_axis(0)
        #     elif (joystickTest.get_axis(0) < -0.1):
        #         x += vel * joystickTest.get_axis(0)
        #     if (0.1 < joystickTest.get_axis(1)):
        #         y += vel * joystickTest.get_axis(1)
        #     elif (joystickTest.get_axis(1) < -0.1):
        #         y += vel * joystickTest.get_axis(1)
        #     if (joystickTest.get_axis(5) > 0):
        #         vel = 10
        #     else:
        #         vel = 5

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run = False
    if state == "Game":
        keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        mousePosRel = pygame.mouse.get_rel()
        if mousePressed[0] and x < mousePos[0] < x+width and y < mousePos[1] < y+height or mousePressed[0] and x < mousePos[0]-mousePosRel[0] < x+width and y < mousePos[1]-mousePosRel[1] < y+height:
            x = mousePos[0]-width//2
            y = mousePos[1]-height//2

        dt = clock.tick()

        time_since_last_action += dt

        if time_since_last_action > 200:
            enemy_manager.new_ememy()
            time_since_last_action = 0

        # if keys[pygame.K_LEFT]:
        #     width -= vel
        # if keys[pygame.K_RIGHT]:
        #     width += vel
        # if keys[pygame.K_UP]:
        #     height -= vel
        # if keys[pygame.K_DOWN]:
        #     height += vel

        if not player.is_dead():
            play_board.render()
            enemy_manager.manage()
            tower_manager.manage(dt)
            projectile_manager.manage()
            bar.render()
        else:
            state = "Game_Over"

        pygame.display.update()
    elif state == "Game_Over":
        game_over_background = pygame.Surface((window_size[0], window_size[1]), pygame.SRCALPHA)
        game_over_background.fill((255, 0, 0, 128))
        window.blit(game_over_background, (0, 0))
        game_over_text = default_font.render('Game Over', False, (255, 255, 255))
        window.blit(game_over_text, (window_size[0] // 2 - game_over_text.get_rect().width // 2, window_size[1] // 2 - game_over_text.get_rect().height // 2))
        if not game_over_screen_shown:
            pygame.display.update()
            game_over_screen_shown = True

pygame.quit()