import pygame
import math

class Projectile_manager:
    projectiles = []
    def __init__(self, window):
        self.window = window

    def new_projectile(self, code, target_pos, start_pos):
        self.projectiles.append(Canon_ball(target_pos, start_pos))

    def manage(self):
        for projectile in self.projectiles:
            projectile.update_pos()
            projectile.render(self.window)

class Projectile:
    def __init__(self, movement_x, movement_y, start_pos, size):
        self.size = size
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]

    def update_pos(self):
        self.pos_x += self.movement_x
        self.pos_y += self.movement_y

    def render(self, window):
        window.blit(self.image, (self.pos_x - self.size // 2, self.pos_y - self.size // 2))

class Canon_ball(Projectile):
    def __init__(self, target_pos, start_pos):
        self.vel = 20
        length_x = target_pos[0] - start_pos[0]
        length_y = target_pos[1] - start_pos[1]
        tangential_length = math.sqrt(length_x ** 2 + length_y ** 2)
        factor = self.vel / tangential_length
        movement_x = length_x * factor
        movement_y = length_y * factor
        Projectile.__init__(self, movement_x, movement_y, start_pos, 10)
        self.image = pygame.image.load('./ressources/Cannon_Ball.png')
        self.image = pygame.transform.scale(self.image, (10, 10))