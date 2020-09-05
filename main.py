import pygame
import board
import enemy
import tower
import projectile
import shop

pygame.init()
size_of_one_field = 100
size_of_enemys = 60
#pygame.display.Info().current_w
#pygame.display.Info().current_h
#pygame.FULLSCREEN
window = pygame.display.set_mode((size_of_one_field * 10, size_of_one_field * 5 + 100), )

pygame.display.set_caption("Test")

x = 50
y = 50
width = 80
height = 80
vel = 5
clock = pygame.time.Clock()

imageTest = pygame.image.load('./ressources/Test.png')
imageTest = pygame.transform.scale(imageTest, (width, height))

play_board = board.Board(size_of_one_field)
enemy_manager = enemy.Enemy_manager(play_board, size_of_enemys, window)
projectile_manager = projectile.Projectile_manager(window)
tower_manager = tower.TowerManager(1, enemy_manager, projectile_manager)

test_pos = play_board.get_middle_of_field(2, 5)
test_pos_2 = play_board.get_middle_of_field(2, 2)
test_pos_3 = play_board.get_middle_of_field(2, 0)
test_tower = play_board.add_tower_to_field(tower_manager.add_tower("lol", test_pos), 2, 5)
test_tower_2 = play_board.add_tower_to_field(tower_manager.add_tower("lol", test_pos_2), 2, 2)
test_tower_3 = play_board.add_tower_to_field(tower_manager.add_tower("lol", test_pos_3), 2, 0)

shop = shop.Shop(0, play_board.get_board_height() * size_of_one_field, play_board.get_board_width() * size_of_one_field)
shop.render(window)

time_since_last_action = 0

drag = False
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            drag, index = shop.checkShopClick(x,y)

        if drag and event.type == pygame.MOUSEBUTTONUP:
            drag = False
            x,y = play_board.get_middle_of_on_field_from_x_y(event.pos)
            row, colum = play_board.get_row_and_column_from_x_y(x,y)
            play_board.add_tower_to_field(tower_manager.add_tower("lol", (x,y)),row, colum )


    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()
    mousePressed = pygame.mouse.get_pressed()
    mousePosRel = pygame.mouse.get_rel()
    if mousePressed[0] and x < mousePos[0] < x+width and y < mousePos[1] < y+height or mousePressed[0] and x < mousePos[0]-mousePosRel[0] < x+width and y < mousePos[1]-mousePosRel[1] < y+height:
        x = mousePos[0]-width//2
        y = mousePos[1]-height//2

    dt = clock.tick()

    time_since_last_action += dt

    if time_since_last_action > 2000:
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
    play_board.render(window)

    enemy_manager.manage()
    tower_manager.manage(dt)
    projectile_manager.manage()
    shop.render(window)

    if drag:
        shop.dragItem(index, mousePos, window)

    pygame.display.update()

pygame.quit()