import pygame

class TowerManager:
    towers = []

    def __init__(self, scale, enemy_manager, projectile_manager):
        self.scale = scale
        self.enemy_manager = enemy_manager
        self.projectile_manager = projectile_manager

    def add_tower(self, code, pos):
        new_tower = Basic_tower(self.scale, pos, self.enemy_manager)
        self.towers.append(new_tower)
        return new_tower

    def manage(self, time):
        for tower in self.towers:
            tower.add_time(time)
            if tower.shot_approved():
                enemys_in_range = tower.search_for_enemy_in_range()
                if enemys_in_range:
                    self.projectile_manager.new_projectile("Test", enemys_in_range[0].get_pos(), tower.get_pos(), enemys_in_range[0])
                    tower.shot_fired()

class Tower:
    def __init__(self, scale, pos, range, enemy_manager, projectile_code, cooldown):
        self.size = int(scale * 80)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.range = range
        self.enemy_manager = enemy_manager
        self.projectile_code = projectile_code
        self.cooldown = cooldown
        self.time_since_last_shot = 0

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def render(self, window, pos_x, pos_y):
        window.blit(self.image, (pos_x - self.size * 0.8 // 2, pos_y - self.size // 2))

    def search_for_enemy_in_range(self):
        return self.enemy_manager.get_enemys_in_range((self.pos_x - self.range, self.pos_y - self.range), (self.pos_x + self.range, self.pos_y + self.range))

    def get_projectile_type(self):
        return self.projectile_code

    def add_time(self, time_to_add):
        self.time_since_last_shot += time_to_add

    def shot_approved(self):
        return self.time_since_last_shot > self.cooldown

    def shot_fired(self):
        self.time_since_last_shot = 0

class Basic_tower(Tower):
    def __init__(self, scale, pos, enemy_manager):
        range = 160 * scale
        cooldown = 200
        Tower.__init__(self, scale, pos, range, enemy_manager, "Test", cooldown)
        self.image = pygame.image.load('./ressources/Basic_tower.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 80)))