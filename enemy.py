import pygame

from collections import deque
from pygame.surface import Surface
from player import Bar
from player import Player
from board import Board
from damage_types import DamageTypes


class Enemy:
    """The base class of an enemy.

    Attributes:
        money_value (int): The value credited to the player should he defeat the opponent.
        board (Board): The board on which the enemy moves.
        size (int): The diagonal size of the enemy.
        pos (tuple): The current position of the enemy.
        damage (int): The damage which the opponent inflicts on the players health points should the opponent traverse
            the path unhindered.
        weaknesses (list): The weaknesses of the enemy for certain elements.
        resistances (list): The opponent's resistance to certain elements.
        vel (int): The speed at which the opponent runs across the board.
        last_movement (str): The movement direction of the enemy in the last clock tick.
        health_points (int): The health points which decide whether an opponent has been defeated.
        top_offset (int): The offset created by the bar at the top of the screen.

    Author:
        Kim Matt
        Moritz Nueske
    """

    def __init__(self, board: Board, scale: float, start_pos: tuple, health_points: int, money_value: int, damage: int,
                 weaknesses: list, resistances: list, vel: float):
        """Creates an base enemy.

        Args:
            board (Board): The board on which the enemy moves.
            scale (float): The scale in which the game is rendered.
            start_pos (tuple): The coordinates at which the enemy begins his path
            health_points (int): The health points of the enemy.
            money_value (int): The value credited to the player should he defeat the opponent.
            damage (int): The damage which the opponent inflicts on the players health points should the opponent
                traverse the path unhindered.
            weaknesses (list): The weaknesses of the enemy for certain elements.
            resistances (list): The opponent's resistance to certain elements.:
            vel (float): The speed at which the opponent runs across the board.

        Author:
            Kim Matt
            Moritz Nueske
        """
        self.money_value = money_value
        self.board = board
        self.size = int(scale * 60)
        self.pos = list(start_pos)
        self.damage = damage
        self.weaknesses = weaknesses
        self.resistances = resistances
        self.vel = int(vel)
        self.last_movement = self.board.get_supposed_start_direction()
        self.health_points = health_points
        self.top_offset = Bar.get_height_of_bar(scale)

    def update_pos(self):
        """Moves the enemy along the path by deciding the next movement based on the last and current field under the
        enemy.

        Author:
            Kim Matt
        """
        field_code = self.board.get_field_at_x_y(tuple(self.pos))
        if field_code:
            field_code = field_code.get_field_code()
            if self.last_movement == "r":
                if field_code == "sh":
                    self.pos[0] += self.vel
                    self.last_movement = "r"
                elif field_code == "elu":
                    if self.is_over_middle_in_x_direction():
                        self.pos[1] -= self.vel
                        self.last_movement = "u"
                    else:
                        self.pos[0] += self.vel
                        self.last_movement = "r"
                elif field_code == "eld":
                    if self.is_over_middle_in_x_direction():
                        self.pos[1] += self.vel
                        self.last_movement = "d"
                    else:
                        self.pos[0] += self.vel
                        self.last_movement = "r"
                elif field_code == "erd":
                    self.pos[0] += self.vel
                    self.last_movement = "r"
                elif field_code == "eru":
                    self.pos[0] += self.vel
                    self.last_movement = "r"
            elif self.last_movement == "u":
                if field_code == "eld":
                    if self.is_over_middle_in_y_direction():
                        self.pos[0] -= self.vel
                        self.last_movement = "l"
                    else:
                        self.pos[1] -= self.vel
                        self.last_movement = "u"
                elif field_code == "sv":
                    self.pos[1] -= self.vel
                    self.last_movement = "u"
                elif field_code == "erd":
                    if self.is_over_middle_in_y_direction():
                        self.pos[0] += self.vel
                        self.last_movement = "r"
                    else:
                        self.pos[1] -= self.vel
                        self.last_movement = "u"
                elif field_code == "elu":
                    self.pos[1] -= self.vel
                    self.last_movement = "u"
                elif field_code == "eru":
                    self.pos[1] -= self.vel
                    self.last_movement = "u"
            elif self.last_movement == "l":
                if field_code == "eru":
                    if self.is_over_middle_in_x_direction():
                        self.pos[1] -= self.vel
                        self.last_movement = "u"
                    else:
                        self.pos[0] -= self.vel
                        self.last_movement = "l"
                if field_code == "sh":
                    self.pos[0] -= self.vel
                    self.last_movement = "l"
                if field_code == "erd":
                    if self.is_over_middle_in_x_direction():
                        self.pos[1] += self.vel
                        self.last_movement = "d"
                    else:
                        self.pos[0] -= self.vel
                        self.last_movement = "l"
                if field_code == "elu":
                    self.pos[0] -= self.vel
                    self.last_movement = "l"
                if field_code == "eld":
                    self.pos[0] -= self.vel
                    self.last_movement = "l"
            elif self.last_movement == "d":
                if field_code == "eru":
                    if self.is_over_middle_in_y_direction():
                        self.pos[0] += self.vel
                        self.last_movement = "r"
                    else:
                        self.pos[1] += self.vel
                        self.last_movement = "d"
                elif field_code == "sv":
                    self.pos[1] += self.vel
                    self.last_movement = "d"
                elif field_code == "elu":
                    if self.is_over_middle_in_y_direction():
                        self.pos[0] -= self.vel
                        self.last_movement = "l"
                    else:
                        self.pos[1] += self.vel
                        self.last_movement = "d"
                elif field_code == "erd":
                    self.pos[1] += self.vel
                    self.last_movement = "d"
                elif field_code == "eld":
                    self.pos[1] += self.vel
                    self.last_movement = "d"
        else:
            if self.last_movement == "r":
                self.pos[0] += self.vel
            elif self.last_movement == "u":
                self.pos[1] -= self.vel
            elif self.last_movement == "l":
                self.pos[0] -= self.vel
            else:
                self.pos[1] += self.vel

    def correct_to_middle(self):
        """Corrects the enemy to the middle of the path when moved a bit to far at edge fields.

        Author:
            Kim Matt
        """
        middle = self.get_middle_of_current_field()
        if self.last_movement == "d" or self.last_movement == "u":
            if not self.pos[0] == middle[0]:
                self.pos[0] = middle[0]
        if self.last_movement == "r" or self.last_movement == "l":
            if not self.pos[1] == middle[1]:
                self.pos[1] = middle[1]

    def is_over_middle_in_x_direction(self) -> bool:
        """Checks whether the enemy is over the middle of the field in horizontal directions.

        Returns:
            bool: True when enemy is over the middle of the field, False if not.

        Author:
            Kim Matt
        """
        middle = self.get_middle_of_current_field()
        if self.last_movement == "r":
            return self.pos[0] > middle[0]
        elif self.last_movement == "l":
            return self.pos[0] < middle[0]
        else:
            return False

    def is_over_middle_in_y_direction(self) -> bool:
        """Checks whether the enemy is over the middle of the field in vertical directions.

        Returns:
            bool: True when enemy is over the middle of the field, False if not.

        Author:
            Kim Matt
        """
        middle = self.get_middle_of_current_field()
        if self.last_movement == "d":
            return self.pos[1] > middle[1]
        elif self.last_movement == "u":
            return self.pos[1] < middle[1]
        else:
            return False

    def get_middle_of_current_field(self) -> tuple:
        """Returns the middle point of the field under the enemy.

        Returns:
            tuple: The coordinates of the middle point.

        Author:
            Kim Matt
        """
        return self.board.get_middle_of_field_from_x_y(tuple(self.pos))

    def is_at_end(self) -> bool:
        """Checks whether the enemy is at the end of the course.

        Returns:
            bool: True when enemy is at the end, False if not.

        Author:
            Kim Matt
        """
        current_field = self.board.get_field_at_x_y((self.pos[0], self.pos[1]))
        if current_field:
            if current_field.is_end_block():
                size_of_fields = self.board.get_size_of_one_field()
                if self.last_movement == "r":
                    last_quarter = self.pos[0] // size_of_fields * size_of_fields + size_of_fields // 4 * 3
                    if self.pos[0] > last_quarter:
                        return True
                if self.last_movement == "l":
                    last_quarter = self.pos[0] // size_of_fields * size_of_fields + size_of_fields // 4 * 1
                    if self.pos[0] < last_quarter:
                        return True
                if self.last_movement == "d":
                    last_quarter = ( self.pos[1] + self.top_offset) // size_of_fields * size_of_fields + \
                                   size_of_fields // 4 * 3
                    if self.pos[1] > last_quarter:
                        return True
                if self.last_movement == "l":
                    last_quarter = (self.pos[1] + self.top_offset) // size_of_fields * size_of_fields + \
                                   size_of_fields // 4 * 1
                    if self.pos[1] < last_quarter:
                        return True
            return False

    def hit(self, damage: int):
        """Reduces the enemy's health points by the given value.

        Args:
            damage (int): The value by how much the health points should be reduced.

        Author:
            Kim Matt
        """
        self.health_points -= damage
        return self.health_points <= 0

    def get_damage(self) -> int:
        """Returns the value of how much damage the opponent inflicts on the player's health points.

        Returns:
            int: Value of damage.

        Author:
            Kim Matt
        """
        return self.damage

    def get_money_value(self) -> int:
        """Returns the value of how much money the player gets when defeating the opponent.

        Returns:
            int: The value of how much money the player gets when defeating the opponent.

        Author:
            Kim Matt
        """
        return self.money_value

    def check_damage_type(self, damage: int, damage_type: DamageTypes) -> int:
        """Checks whether the enemy is weak or has resistance to a certain type of damage.

        Args:
            damage (DamageTypes): The amount of normal damage.
            damage_type (DamageTypes): The type of damage to be compared with.

        Returns:
            int: The resulting damage.

        Author:
            Moritz Nueske
        """
        for weakness in self.weaknesses:
            if weakness == damage_type:
                return damage * 2
        for resistance in self.resistances:
            if resistance == damage_type:
                return damage // 2
        return damage

    def get_pos(self):
        """Returns the current position of the enemy.

        Returns:
            tuple: The current position of the enemy.

        Author:
            Kim Matt
        """
        return self.pos[0], self.pos[1]

    def render(self, window: Surface):
        """Renders the enemy onto the given window.

        Args:
            window (Surface): The surface on which the enemy should be rendered.

        Author:
            Kim Matt
        """
        window.blit(self.image, (self.pos[0] - self.size // 2, self.pos[1] - self.size // 2))


class BaseEnemy(Enemy):
    """The weakest enemy, mostly appearing at the begin of a level to get comfortable with the game mechanics.

    Attributes:
        money_value (int): The value credited to the player should he defeat the opponent.
        board (Board): The board on which the enemy moves.
        size (int): The diagonal size of the enemy.
        pos (tuple): The current position of the enemy.
        damage (int): The damage which the opponent inflicts on the players health points should the opponent traverse
            the path unhindered.
        weaknesses (list): The weaknesses of the enemy for certain elements.
        resistances (list): The opponent's resistance to certain elements.
        vel (int): The speed at which the opponent runs across the board.
        last_movement (str): The movement direction of the enemy in the last clock tick.
        health_points (int): The health points which decide whether an opponent has been defeated.
        top_offset (int): The offset created by the bar at the top of the screen.
        image (Surface): The image of the enemy for rendering.

    Author:
        Kim Matt
        Moritz Nueske
    """

    def __init__(self, scale: float, board: Board, start_pos: tuple):
        """The weakest enemy, mostly appearing at the begin of a level to get comfortable with the game mechanics.

        Args:
            scale (float): The scale in which the game is rendered.
            board (Board): The board which the enemy should traverse.
            start_pos (tuple): The position the enemy starts its path.

        Author:
            Kim Matt
            Moritz Nueske
        """
        health_points = 100
        damage = 1
        vel = 4 * scale
        money_value = 40
        resistances = []
        weaknesses = [DamageTypes.ultimate]
        Enemy.__init__(self, board, scale, start_pos, health_points, money_value, damage, weaknesses, resistances, vel)
        self.image = pygame.image.load('./ressources/enemys/Enemy_balloon.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 60)))


class GreenBalloon(Enemy):
    """This enemy has many life points but is slower than other enemies.

    Attributes:
        money_value (int): The value credited to the player should he defeat the opponent.
        board (Board): The board on which the enemy moves.
        size (int): The diagonal size of the enemy.
        pos (tuple): The current position of the enemy.
        damage (int): The damage which the opponent inflicts on the players health points should the opponent traverse
            the path unhindered.
        weaknesses (list): The weaknesses of the enemy for certain elements.
        resistances (list): The opponent's resistance to certain elements.
        vel (int): The speed at which the opponent runs across the board.
        last_movement (str): The movement direction of the enemy in the last clock tick.
        health_points (int): The health points which decide whether an opponent has been defeated.
        top_offset (int): The offset created by the bar at the top of the screen.
        image (Surface): The image of the enemy for rendering.

    Author:
        Moritz Nueske
    """

    def __init__(self, scale: float, board: Board, start_pos: tuple):
        """This enemy has many life points but is slower than other enemies.

        Args:
            scale (float): The scale in which the game is rendered.
            board (Board): The board which the enemy should traverse.
            start_pos (tuple): The position the enemy starts its path.

        Author:
            Moritz Nueske
        """
        health_points = 500
        damage = 5
        vel = 2 * scale
        money_value = 100
        resistances = []
        weaknesses = [DamageTypes.ultimate]
        Enemy.__init__(self, board, scale, start_pos, health_points, money_value, damage, weaknesses, resistances, vel)
        self.image = pygame.image.load('./ressources/enemys/Enemy_balloon_green.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 60)))


class BlueBalloon(Enemy):
    """This enemy is resistant to ice projectiles but is more vulnerable against fire projectiles.

    Attributes:
        money_value (int): The value credited to the player should he defeat the opponent.
        board (Board): The board on which the enemy moves.
        size (int): The diagonal size of the enemy.
        pos (tuple): The current position of the enemy.
        damage (int): The damage which the opponent inflicts on the players health points should the opponent traverse
            the path unhindered.
        weaknesses (list): The weaknesses of the enemy for certain elements.
        resistances (list): The opponent's resistance to certain elements.
        vel (int): The speed at which the opponent runs across the board.
        last_movement (str): The movement direction of the enemy in the last clock tick.
        health_points (int): The health points which decide whether an opponent has been defeated.
        top_offset (int): The offset created by the bar at the top of the screen.
        image (Surface): The image of the enemy for rendering.

    Author:
        Moritz Nueske
    """

    def __init__(self, scale: float, board: Board, start_pos: tuple):
        """This enemy is resistant to ice projectiles but is more vulnerable against fire projectiles.

        Args:
            scale (float): The scale in which the game is rendered.
            board (Board): The board which the enemy should traverse.
            start_pos (tuple): The position the enemy starts its path.

        Author:
            Moritz Nueske
        """
        health_points = 1000
        damage = 10
        vel = 3 * scale
        money_value = 200
        resistances = [DamageTypes.ice]
        weaknesses = [DamageTypes.fire]
        Enemy.__init__(self, board, scale, start_pos, health_points, money_value, damage, weaknesses, resistances, vel)
        self.image = pygame.image.load('./ressources/enemys/Enemy_balloon_blue.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 60)))


class YellowBalloon(Enemy):
    """This enemy is resistant to fire projectiles but is more vulnerable against ice projectiles.

    Attributes:
        money_value (int): The value credited to the player should he defeat the opponent.
        board (Board): The board on which the enemy moves.
        size (int): The diagonal size of the enemy.
        pos (tuple): The current position of the enemy.
        damage (int): The damage which the opponent inflicts on the players health points should the opponent traverse
            the path unhindered.
        weaknesses (list): The weaknesses of the enemy for certain elements.
        resistances (list): The opponent's resistance to certain elements.
        vel (int): The speed at which the opponent runs across the board.
        last_movement (str): The movement direction of the enemy in the last clock tick.
        health_points (int): The health points which decide whether an opponent has been defeated.
        top_offset (int): The offset created by the bar at the top of the screen.
        image (Surface): The image of the enemy for rendering.

    Author:
        Moritz Nueske
    """

    def __init__(self, scale: float, board: Board, start_pos: tuple):
        """This enemy is resistant to fire projectiles but is more vulnerable against ice projectiles.

        Args:
            scale (float): The scale in which the game is rendered.
            board (Board): The board which the enemy should traverse.
            start_pos (tuple): The position the enemy starts its path.

        Author:
            Moritz Nueske
        """
        health_points = 1500
        damage = 20
        vel = 4 * scale
        money_value = 400
        resistances = [DamageTypes.fire]
        weaknesses = [DamageTypes.ice]
        Enemy.__init__(self, board, scale, start_pos, health_points, money_value, damage, weaknesses, resistances, vel)
        self.image = pygame.image.load('./ressources/enemys/Enemy_balloon_yellow.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 60)))


class BossBalloon(Enemy):
    """The strongest enemy of all.

    Attributes:
        money_value (int): The value credited to the player should he defeat the opponent.
        board (Board): The board on which the enemy moves.
        size (int): The diagonal size of the enemy.
        pos (tuple): The current position of the enemy.
        damage (int): The damage which the opponent inflicts on the players health points should the opponent traverse
            the path unhindered.
        weaknesses (list): The weaknesses of the enemy for certain elements.
        resistances (list): The opponent's resistance to certain elements.
        vel (int): The speed at which the opponent runs across the board.
        last_movement (str): The movement direction of the enemy in the last clock tick.
        health_points (int): The health points which decide whether an opponent has been defeated.
        top_offset (int): The offset created by the bar at the top of the screen.
        image (Surface): The image of the enemy for rendering.

    Author:
        Moritz Nueske
    """

    def __init__(self, scale: float, board: Board, start_pos: tuple):
        """The strongest enemy of all.

        Args:
            scale (float): The scale in which the game is rendered.
            board (Board): The board which the enemy should traverse.
            start_pos (tuple): The position the enemy starts its path.

        Author:
            Moritz Nueske
        """
        health_points = 10000
        damage = 100
        vel = 3 * scale
        money_value = 10000
        resistances = [DamageTypes.normal]
        weaknesses = [DamageTypes.ultimate]
        Enemy.__init__(self, board, scale, start_pos, health_points, money_value, damage, weaknesses, resistances, vel)
        self.image = pygame.image.load('./ressources/enemys/Enemy_balloon_purple.png')
        self.image = pygame.transform.scale(self.image, (int(scale * 60), int(scale * 60)))


class EnemyManager:
    """Manages the enemies while they are traversing the board.

    board (Board): The board which the enemies should traverse.
    player (Player): The current player with his/her stats.
    scale (float): The scale in which the game should be rendered.
    enemies (list): List of all enemies which are currently traversing the board.
    window (Surface): The Surface on which the enemies should be drawn on.
    start_pos (tuple): The position in which the enemies should start.

    Author:
        Kim Matt
    """

    def __init__(self, board: Board, player: Player, scale: float, window: Surface):
        """Creates a manager for managing the enemies while they are traversing the board.

        Args:
            board (Board): The board which the enemies should traverse.
            player (Player): The current player with his/her stats.
            scale (float): The scale in which the game should be rendered.
            window (Surface): The Surface on which the enemies should be drawn on.

        Author:
            Kim Matt
        """
        self.board = board
        self.player = player
        self.scale = scale
        self.enemies = []
        self.window = window
        self.start_pos = board.get_start_pos()

    def new_enemy(self, enemy_code: str):
        """Adds a new enemy to the manager.

        Args:
            enemy_code (str): The code of the enemy which should be added.

        Author:
            Kim Matt
            Moritz Nueske
        """
        print(enemy_code)
        if enemy_code == "ba":
            self.enemies.append(BaseEnemy(self.scale, self.board, self.start_pos))
        if enemy_code == "blb":
            self.enemies.append(BlueBalloon(self.scale, self.board, self.start_pos))
        if enemy_code == "grb":
            self.enemies.append(GreenBalloon(self.scale, self.board, self.start_pos))
        if enemy_code == "yeb":
            self.enemies.append(YellowBalloon(self.scale, self.board, self.start_pos))
        if enemy_code == "bob":
            self.enemies.append(BossBalloon(self.scale, self.board, self.start_pos))

    def hit_enemy(self, enemy: Enemy, damage: int, damage_type: DamageTypes):
        """Inflicts damage to the given enemy.

        Args:
            enemy (Enemy): The enemy to whom damage is to be inflicted.
            damage (int): The value of the damage to be done .
            damage_type (DamageTypes): The type of damage that should be done.

        Author:
            Kim Matt
            Moritz Nueske
        """
        if self.enemies.__contains__(enemy):
            enemy = self.enemies[self.enemies.index(enemy)]
            damage = enemy.check_damage_type(damage, damage_type)
            if enemy.hit(damage):
                self.player.add_money(enemy.get_money_value())
                self.enemies.remove(enemy)

    def manage(self):
        """Manages the enemies that traversing the board.

        Author:
            Kim Matt
        """
        for enemy in self.enemies:
            enemy.update_pos()
            enemy.correct_to_middle()
            enemy.render(self.window)
            if enemy.is_at_end():
                self.player.reduce_health_points(enemy.get_damage())
                self.enemies.remove(enemy)

    def get_enemys_in_range(self, start_point: tuple, end_point: tuple) -> list:
        """Searches for enemies in given quadratic range.
        
        Args:
            start_point (tuple): Tuple with x, y coordinates from left upper edge of search area.
            end_point (tuple): Tuple with x, y coordinates from right lower edge of search area.

        Returns:
            list: List with all enemies found in search area.

        Author:
            Kim Matt
        """
        enemys_in_range = []
        for enemy in self.enemies:
            if enemy.pos[0] > start_point[0] and enemy.pos[0] < end_point[0] and enemy.pos[1] > start_point[
                1] and enemy.pos[1] < end_point[1]:
                enemys_in_range.append(enemy)
        return enemys_in_range


class WaveManager:
    """Manages the different waves in which enemies were sent out.

    endless_wave_count (int): Gets multiplied by two every time a endless mode wave has ended to spawn mire enemies in
        the next wave.
    waves (list): List with Double-ended queues for each wave in it.
    endless_mode (bool): Indicates whether the level is in endless mode.
    enemy_manager (EnemyManager): Manager to add new enemies and controlling them.
    time (int): The game internal time since the start of the level.
    time_since_last_spawn (int): The time since an enemy was last spawned.
    all_waves_completed (bool): Indicates whether the player has survived all waves.

    Author:
        Kim Matt
    """

    def __init__(self, enemy_manager: EnemyManager):
        """Manages the different waves in which enemies were sent out.

        Args:
            enemy_manager (EnemyManager): Manager to add new enemies and controlling them.

        Author:
            Kim Matt
        """
        self.endless_wave_count = 5
        self.setup_waves()
        self.endless_mode = False
        self.enemy_manager = enemy_manager
        self.time = 0
        self.time_since_last_spawn = 0
        self.all_waves_completed = False

    def setup_waves(self):
        """Reads rhe wave file in which the different enemies per waves are defined and loads them into the game.

        Author:
            Kim Matt
        """
        self.waves = []
        wave_number = 0
        with open("./misc/waves") as wave_file:
            for line in wave_file:
                self.waves.append(deque())
                for enemy in line.split(","):
                    self.waves[wave_number].append(enemy.strip())
                wave_number += 1
        wave_file.close()

    def manage(self, time_difference: int):
        """Manages the spawning of new enemies.

        Args:
            time_difference (int): The time difference between the last time the function was called up.

        Author:
            Kim Matt
        """
        self.time_since_last_spawn += time_difference
        if not self.endless_mode:
            self.time += time_difference
            if 30000 > self.time > 10000:
                if self.waves[0]:
                    if self.time_since_last_spawn > 1000:
                        self.enemy_manager.new_enemy(self.waves[0].popleft())
                        self.time_since_last_spawn = 0
            elif 60000 > self.time > 30000:
                if self.waves[1]:
                    if self.time_since_last_spawn > 800:
                        self.enemy_manager.new_enemy(self.waves[1].popleft())
                        self.time_since_last_spawn = 0
            elif 90000 > self.time > 60000:
                if self.waves[2]:
                    if self.time_since_last_spawn > 800:
                        self.enemy_manager.new_enemy(self.waves[2].popleft())
                        self.time_since_last_spawn = 0
            elif 120000 > self.time > 90000:
                if self.waves[3]:
                    if self.time_since_last_spawn > 800:
                        self.enemy_manager.new_enemy(self.waves[3].popleft())
                        self.time_since_last_spawn = 0
            elif 150000 > self.time > 120000:
                if self.waves[4]:
                    if self.time_since_last_spawn > 800:
                        self.enemy_manager.new_enemy(self.waves[4].popleft())
                        self.time_since_last_spawn = 0
            elif 180000 > self.time > 150000:
                if self.waves[5]:
                    if self.time_since_last_spawn > 800:
                        self.enemy_manager.new_enemy(self.waves[5].popleft())
                        self.time_since_last_spawn = 0
            elif self.time > 180000:
                if self.waves[6]:
                    if self.time_since_last_spawn > 400:
                        self.enemy_manager.new_enemy(self.waves[6].popleft())
                        self.time_since_last_spawn = 0
                elif not self.enemy_manager.enemies:
                    self.all_waves_completed = True
        else:
            if self.waves[7]:
                if self.time_since_last_spawn > 100:
                    self.enemy_manager.new_enemy(self.waves[7].popleft())
                    self.time_since_last_spawn = 0
            else:
                self.endless_wave_count *= 2
                self.time_since_last_spawn = -9900
                self.waves[7] = deque(
                    ["ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba",
                     "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba",
                     "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba", "ba"])
                for i in range(self.endless_wave_count):
                    self.waves[7].append("ba")
                for i in range(self.endless_wave_count // 2):
                    self.waves[7].append("grb")
                for i in range(self.endless_wave_count // 3):
                    self.waves[7].append("blb")
                for i in range(self.endless_wave_count // 4):
                    self.waves[7].append("yeb")
                for i in range(self.endless_wave_count // 10):
                    self.waves[7].append("bob")

    def set_endless_mode(self):
        """Sets the wave manager to endless mode when player decides to after he has beaten all waves.

        Author:
            Kim Matt
        """
        self.endless_mode = True

    def get_all_waves_completed(self) -> bool:
        """Checks whether the player has defeated all waves besides the endless mode wave.

        Returns:
            bool: True if player has defeated all waves, False if not.

        Author:
            Kim Matt
        """
        if not self.endless_mode:
            return self.all_waves_completed
        else:
            return False
