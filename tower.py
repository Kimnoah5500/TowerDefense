import pygame

class TowerManager:
    def __init__(self, scale, enemy_manager, projectile_manager):
        self.scale = scale
        self.enemy_manager = enemy_manager
        self.projectile_manager = projectile_manager
        self.towers = []

    def add_tower(self, code, row_column, size_of_one_field, top_offset):
        pos = (row_column[1] * size_of_one_field + size_of_one_field // 2, row_column[0] * size_of_one_field + size_of_one_field // 2 + top_offset)
        if code == "bato":
            new_tower = Basic_tower(self.scale, pos, self.enemy_manager)
        #TODO Add other Tower Codes here if there are any new
        self.towers.append(new_tower)
        return new_tower

    def manage(self, time):
        for tower in self.towers:
            tower.add_time(time)
            if tower.shot_approved():
                enemys_in_range = tower.search_for_enemy_in_range()
                if enemys_in_range:
                    self.projectile_manager.new_projectile(tower.projectile_code, enemys_in_range[0].get_pos(), tower.get_pos(), enemys_in_range[0])
                    tower.shot_fired()

    def get_range_from_tower_code(self, code):
        if code == "bato":
            return Basic_tower.range * self.scale
        if code == "test" or code == "test2":
            return 0

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
    range = 160

    def __init__(self, scale, pos, enemy_manager):
        cooldown = 200
        projectile_code = "caba"
        Tower.__init__(self, scale, pos, self.range * scale, enemy_manager, projectile_code, cooldown)
        self.image = pygame.image.load('./ressources/Basic_tower.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 80)))
        