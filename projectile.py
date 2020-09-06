import pygame
import math

class Projectile_manager:
    def __init__(self, enemy_manager, scale, window):
        self.scale = scale
        self.enemy_manager = enemy_manager
        self.window = window
        self.projectiles = []

    def new_projectile(self, code, target_pos, start_pos, target_enemy):
        if code == "caba":
            self.projectiles.append(Canon_ball(target_pos, start_pos, self.scale, target_enemy))
        #TODO Add Projectile Codes here if there are any new

    def manage(self):
        for projectile in self.projectiles:
            projectile.update_pos()
            if projectile.is_at_target_pos():
                self.enemy_manager.hit_enemy(projectile.target_enemy, projectile.damage)
                self.projectiles.remove(projectile)
            else:
                projectile.render(self.window)

class Projectile:
    def __init__(self, target_pos, start_pos, vel, target_enemy, damage, size, scale):
        self.vel = vel
        self.size = size * scale
        self.target_enemy = target_enemy
        self.damage = damage
        length_x = target_pos[0] - start_pos[0]
        length_y = target_pos[1] - start_pos[1]
        tangential_length = math.sqrt(length_x ** 2 + length_y ** 2)
        factor = self.vel / tangential_length
        self.movement_x = length_x * factor
        self.movement_y = length_y * factor
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]
        self.target_pos = target_pos

    def update_pos(self):
        self.pos_x += self.movement_x
        self.pos_y += self.movement_y

    def is_at_target_pos(self):
        return self.target_pos[0] - self.vel < self.pos_x < self.target_pos[0] + self.vel and self.target_pos[1] - self.vel < self.pos_y < self.target_pos[1] + self.vel

    def render(self, window):
        window.blit(self.image, (self.pos_x - self.size // 2, self.pos_y - self.size // 2))

class Canon_ball(Projectile):
    def __init__(self, target_pos, start_pos, scale, target_enemy):
        vel = 20 * scale
        damage = 20
        Projectile.__init__(self, target_pos, start_pos, vel, target_enemy, damage, 10, scale)
        self.image = pygame.image.load('./ressources/Cannon_Ball.png')
        self.image = pygame.transform.scale(self.image, (int(10 * scale), int(10 * scale)))