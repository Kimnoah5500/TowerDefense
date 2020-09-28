import pygame

from projectile import ProjectileManager
from pygame.surface import Surface

class Tower:
    """Base for towers.
    
    Attributes:
        size (int): Edge length of the square tower.
        pos (tuple): Position of the tower on the game board.
        resell_price (int): Price at which the tower is sold.
        shotting_range (int): Range of shots of the tower.
        enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.
        projectile_code (str): The code for the projectiles which the tower fires.
        cooldown (int): The time the tower waits till he is able to shot again.
        time_since_last_shot (int): The time that has elapsed since the last shot.

    Author:
        Kim Matt
    """

    def __init__(self, scale: float, pos: tuple, shotting_range: float, enemy_manager, projectile_code: str,
                 cooldown: int, resell_price: int):
        """

        Args:
            scale (float): The scale in which the game is rendered.
            pos (tuple): Position of the tower on the game board.
            shotting_range (int): Range of shots of the tower.
            enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.
            projectile_code (str): The code for the projectiles which the tower fires.
            cooldown (int): The time the tower waits till he is able to shot again.
            resell_price (int): Price at which the tower is sold.

        Author:
            Kim Matt
        """
        self.size = int(scale * 80)
        self.pos = pos
        self.resell_price = resell_price
        self.range = int(shotting_range)
        self.enemy_manager = enemy_manager
        self.projectile_code = projectile_code
        self.cooldown = cooldown
        self.time_since_last_shot = 0

    def get_pos(self) -> tuple:
        """Get the position in which the tower is placed.

        Returns:
            tuple: Position of the tower.

        Author:
            Kim Matt
        """
        return self.pos

    def render(self, window: Surface):
        """Renders the tower at its position.

        Args:
            window (Surface):

        Author:
            Kim Matt
        """
        window.blit(self.image, (self.pos[0] - self.size * 0.8 // 2, self.pos[1] - self.size // 2))

    def search_for_enemy_in_range(self) -> list:
        """Tower searches for all enemies that are in his quadratically shooting range.

        Returns:
            list: List of all enemies that are in shooting range.

        Author:
            Kim Matt
        """
        return self.enemy_manager.get_enemys_in_range((self.pos[0] - self.range, self.pos[1] - self.range),
                                                      (self.pos[0] + self.range, self.pos[1] + self.range))

    def get_projectile_type(self) -> str:
        """Returns the code for the projectiles of this tower.

        Returns:
            str: Code of the projectiles of this specific tower.

        Author:
            Kim Matt
        """
        return self.projectile_code

    def add_time(self, time_to_add):
        """Adds the time differnce since the last tick to the towers internal clock.

        Args:
            time_to_add (int): Time elapsed since the last click tick.

        Author:
            Kim Matt
        """
        self.time_since_last_shot += time_to_add

    def shot_approved(self):
        """Returns whether the tower is able to shot again.

        Returns:
            bool: True if tower has cooled down and is able to shot again, False if not.

        Author:
            Kim Matt
        """
        return self.time_since_last_shot > self.cooldown

    def shot_fired(self):
        """Resets the time when shot has been fired for cooldown.

        Author:
            Kim Matt
        """
        self.time_since_last_shot = 0


class BasicTower(Tower):
    """A tower with no special abilities.

    Attributes:
        size (int): Edge length of the square tower.
        pos (tuple): Position of the tower on the game board.
        resell_price (int): Price at which the tower is sold.
        shotting_range (int): Range of shots of the tower.
        enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.
        projectile_code (str): The code for the projectiles which the tower fires.
        cooldown (int): The time the tower waits till he is able to shot again.
        time_since_last_shot (int): The time that has elapsed since the last shot.
        image (Surface): Image of the tower.

    Author:
        Kim Matt
    """
    range = 160

    def __init__(self, scale, pos, enemy_manager):
        """A tower with no special abilities.

        Args:
            scale (float): The scale in which the game is rendered.
            pos (tuple): Position of the tower on the game board.
            enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.

        Author:
            Kim Matt
        """
        cooldown = 200
        projectile_code = "caba"
        resell_price = 100
        Tower.__init__(self, scale, pos, self.range * scale, enemy_manager, projectile_code, cooldown, resell_price)
        self.image = pygame.image.load('./ressources/towers/Basic_tower.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 80)))


class SniperTower(Tower):
    """A tower which can aim at targets far away.

    Attributes:
        size (int): Edge length of the square tower.
        pos (tuple): Position of the tower on the game board.
        resell_price (int): Price at which the tower is sold.
        shotting_range (int): Range of shots of the tower.
        enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.
        projectile_code (str): The code for the projectiles which the tower fires.
        cooldown (int): The time the tower waits till he is able to shot again.
        time_since_last_shot (int): The time that has elapsed since the last shot.
        image (Surface): Image of the tower.

    Author:
        Moritz Nueske
    """
    range = 240

    def __init__(self, scale, pos, enemy_manager):
        """A tower which can aim at targets far away.

        Args:
            scale (float): The scale in which the game is rendered.
            pos (tuple): Position of the tower on the game board.
            enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.

        Author:
            Moritz Nueske
        """
        cooldown = 500
        projectile_code = "bcba"
        resell_price = 300
        Tower.__init__(self, scale, pos, self.range * scale, enemy_manager, projectile_code, cooldown, resell_price)
        self.image = pygame.image.load('./ressources/towers/Sniper_tower.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 80)))


class FlameTower(Tower):
    """A tower that shots fire projectiles.

    Attributes:
        size (int): Edge length of the square tower.
        pos (tuple): Position of the tower on the game board.
        resell_price (int): Price at which the tower is sold.
        shotting_range (int): Range of shots of the tower.
        enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.
        projectile_code (str): The code for the projectiles which the tower fires.
        cooldown (int): The time the tower waits till he is able to shot again.
        time_since_last_shot (int): The time that has elapsed since the last shot.
        image (Surface): Image of the tower.

    Author:
        Moritz Nueske
    """
    range = 105

    def __init__(self, scale, pos, enemy_manager):
        """A tower that shots fire projectiles.

        Args:
            scale (float): The scale in which the game is rendered.
            pos (tuple): Position of the tower on the game board.
            enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.

        Author:
            Moritz Nueske
        """
        cooldown = 50
        projectile_code = "fipo"
        resell_price = 450
        Tower.__init__(self, scale, pos, self.range * scale, enemy_manager, projectile_code, cooldown, resell_price)
        self.image = pygame.image.load('./ressources/towers/Flame_tower.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 80)))


class IceTower(Tower):
    """A tower that shots ice projectiles.

    Attributes:
        size (int): Edge length of the square tower.
        pos (tuple): Position of the tower on the game board.
        resell_price (int): Price at which the tower is sold.
        shotting_range (int): Range of shots of the tower.
        enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.
        projectile_code (str): The code for the projectiles which the tower fires.
        cooldown (int): The time the tower waits till he is able to shot again.
        time_since_last_shot (int): The time that has elapsed since the last shot.
        image (Surface): Image of the tower.

    Author:
        Moritz Nueske
    """
    range = 200

    def __init__(self, scale, pos, enemy_manager):
        """A tower that shots ice projectiles.

        Args:
            scale (float): The scale in which the game is rendered.
            pos (tuple): Position of the tower on the game board.
            enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.

        Author:
            Moritz Nueske
        """
        cooldown = 250
        projectile_code = "icpo"
        resell_price = 750
        Tower.__init__(self, scale, pos, self.range * scale, enemy_manager, projectile_code, cooldown, resell_price)
        self.image = pygame.image.load('./ressources/towers/Ice_tower.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 80)))


class UltimateTower(Tower):
    """A tower with special strength.

    Attributes:
        size (int): Edge length of the square tower.
        pos (tuple): Position of the tower on the game board.
        resell_price (int): Price at which the tower is sold.
        shotting_range (int): Range of shots of the tower.
        enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.
        projectile_code (str): The code for the projectiles which the tower fires.
        cooldown (int): The time the tower waits till he is able to shot again.
        time_since_last_shot (int): The time that has elapsed since the last shot.
        image (Surface): Image of the tower.

    Author:
        Moritz Nueske
    """
    range = 320

    def __init__(self, scale, pos, enemy_manager):
        """A tower with special strength.

        Args:
            scale (float): The scale in which the game is rendered.
            pos (tuple): Position of the tower on the game board.
            enemy_manager (EnemyManager): The manger of all the enemies that are currently traversing the board.

        Author:
            Moritz Nueske
        """
        cooldown = 100
        projectile_code = "ulcb"
        resell_price = 3000
        Tower.__init__(self, scale, pos, self.range * scale, enemy_manager, projectile_code, cooldown, resell_price)
        self.image = pygame.image.load('./ressources/towers/Ultimate_tower.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 80)))


class TowerManager:
    """Manages the towers that are currently placed on the board.

    Attributes:
        scale (float): The scale in which the game is rendered.
        enemy_manager (EnemyManager): The manager for all the enemies that are currently on the board.
        projectile_manager (ProjectileManager): The manager for all projectiles flying over the board.
        towers (list): List of all placed towers.

    Author:
        Kim Matt
    """

    def __init__(self, scale: float, enemy_manager, projectile_manager: ProjectileManager):
        """Manages the towers that are currently placed on the board.

        Args:
            scale (float): The scale in which the game is rendered.
            enemy_manager (EnemyManager): The manager for all the enemies that are currently on the board.
            projectile_manager (ProjectileManager): The manager for all projectiles flying over the board.

        Author:
            Kim Matt
        """
        self.scale = scale
        self.enemy_manager = enemy_manager
        self.projectile_manager = projectile_manager
        self.towers = []

    def add_tower(self, code: str, row_column: tuple, size_of_one_field: int, top_offset: int) -> Tower:
        """Adds a new tower to the managed towers.

        Args:
            code (str): The code of the tower which should be placed.
            row_column (tuple): The row and column the tower should be placed on.
            size_of_one_field (int): The length of the sides of the fields on the board.
            top_offset (int): The offset produced by the bar on top of the screen.

        Returns:
            Tower: The tower which has been added to the manager.

        Author:
            Kim Matt
        """
        pos = (row_column[1] * size_of_one_field + size_of_one_field // 2,
               row_column[0] * size_of_one_field + size_of_one_field // 2 + top_offset)
        if code == "bato":
            new_tower = BasicTower(self.scale, pos, self.enemy_manager)
        if code == "snto":
            new_tower = SniperTower(self.scale, pos, self.enemy_manager)
        if code == "flto":
            new_tower = FlameTower(self.scale, pos, self.enemy_manager)
        if code == "icto":
            new_tower = IceTower(self.scale, pos, self.enemy_manager)
        if code == "ulto":
            new_tower = UltimateTower(self.scale, pos, self.enemy_manager)
        # TODO Add other Tower Codes here if there are any new
        self.towers.append(new_tower)
        return new_tower

    def remove_tower(self, tower: Tower) -> int:
        """Removes the tower from the list of managed towers and returns its resell price.

        Args:
            tower (Tower): The tower which should be removed.

        Returns:
            int: The resell price of the tower.

        Author:
            Kim Matt
        """
        self.towers.remove(tower)
        return tower.resell_price

    def manage(self, time: int):
        """Manages the towers based on the time that has elapsed since the function last function call.

        Args:
            time (int): Time elapsed since the function last function call.

        Author:
            Kim Matt
        """
        for tower in self.towers:
            tower.add_time(time)
            if tower.shot_approved():
                enemys_in_range = tower.search_for_enemy_in_range()
                if enemys_in_range:
                    self.projectile_manager.new_projectile(tower.projectile_code, enemys_in_range[0].get_pos(),
                                                           tower.get_pos(), enemys_in_range[0])
                    tower.shot_fired()

    def get_range_from_tower_code(self, code) -> int:
        """Gets the range of the tower by given code.

        Args:
            code (str): Code of the tower which the range is searched for.

        Returns:
            int: Range of the tower.

        Author:
            Moritz Nueske
        """
        if code == "bato":
            return int(BasicTower.range * self.scale)
        if code == "snto":
            return int(SniperTower.range * self.scale)
        if code == "flto":
            return int(FlameTower.range * self.scale)
        if code == "icto":
            return int(IceTower.range * self.scale)
        if code == "ulto":
            return int(UltimateTower.range * self.scale)
