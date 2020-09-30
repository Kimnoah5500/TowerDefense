import pygame
import math
import random

from damage_types import DamageTypes
from pygame.surface import Surface


class ProjectileManager:
    """Used to manage all projectiles that exist on the board and to create new ones.

    Attributes:
        scale (float): Designed to adjust the size of the game but never really used because pygame don't like resizing.
        enemy_manager (EnemyManager): Object which manages the enemies that currently exist.
        window (Surface): The surface all the projectiles should be drawn on.
        projectiles (list): List of all projectiles currently traveling across the board.

    Author:
        Kim Matt
        Moritz Nueske
    """

    def __init__(self, enemy_manager, scale: float, window: Surface, easter_egg_mode: bool = False):
        """Used to manage all projectiles that exist on the board and to create new ones.

        Args:
            enemy_manager (EnemyManager): Object which manages the enemies that currently exist.
            scale (float): The scale in which the game is rendered.
            window (Surface): The surface all the projectiles should be drawn on.

        Author:
            Kim Matt
        """
        self.scale = scale
        self.enemy_manager = enemy_manager
        self.window = window
        self.easter_egg_mode = easter_egg_mode
        self.projectiles = []

    def new_projectile(self, code: str, target_pos: tuple, start_pos: tuple, target_enemy):
        """Adds a new projectile to the list of projectiles by given projectile code.
        
        Args:
            code (str): The projectile code for the projectile which should be added.
            target_pos (tuple): The position the projectile should travel towards.
            start_pos (tuple): The position the projectile starts from.
            target_enemy (Enemy): The enemy the projectile is targeting.

        Author:
            Kim Matt
            Moritz Nueske
        """
        if self.easter_egg_mode:
            self.projectiles.append(EasterEggProjectile(target_pos, start_pos, self.scale, target_enemy))
        else:
            if code == "caba":
                self.projectiles.append(CanonBall(target_pos, start_pos, self.scale, target_enemy))
            if code == "bcba":
                self.projectiles.append(BigCanonBall(target_pos, start_pos, self.scale, target_enemy))
            if code == "fipo":
                self.projectiles.append(FireProjectile(target_pos, start_pos, self.scale, target_enemy))
            if code == "icpo":
                self.projectiles.append(IceProjectile(target_pos, start_pos, self.scale, target_enemy))
            if code == "ulcb":
                self.projectiles.append(UltimateCanonBall(target_pos, start_pos, self.scale, target_enemy))
        # TODO Add Projectile Codes here if there are any new

    def manage(self):
        """Manages the projectiles which are currently traversing the board.
        
        Author:
            Kim Matt
        """
        for projectile in self.projectiles:
            projectile.update_pos()
            if projectile.is_at_target_pos():
                self.enemy_manager.hit_enemy(projectile.target_enemy, projectile.damage, projectile.damage_type)
                self.projectiles.remove(projectile)
            else:
                projectile.render(self.window)


class Projectile:
    """Base projectile.
    
    Attributes:
        vel (int): Speed with which the projectile flies over the board.
        size (int): Size of the projectile.
        target_enemy (Enemy): The enemy to be hit by the projectile.
        damage (int): The damage that the projectile causes to the enemy.
        damage_type (DamageTypes): The type of damage caused to the opponent.
        move_direction (tuple): The direction in which the projectile is flying per tick.
        pos (tuple): The current position of the projectile.
        target_pos (tuple): The target to which the projectile is flying.

    Author:
        Kim Matt
    """
    def __init__(self, target_pos: tuple, start_pos: tuple, vel: int, target_enemy, damage: int,
                 damage_type: DamageTypes, size: int, scale: float):
        """Base projectile.

        Args:
            target_pos (tuple): The target to which the projectile is flying.
            start_pos (tuple): The position the projectile starts from.
            vel (int): Speed with which the projectile flies over the board.
            target_enemy (Enemy): The enemy to be hit by the projectile.
            damage (int): The damage that the projectile causes to the enemy.
            damage_type (DamageTypes): The type of damage caused to the opponent.
            size (int): Size of the projectile.
            scale (float): The scale in which the game gets rendered.

        Author:
            Kim Matt
        """
        self.vel = int(vel * scale)
        self.size = int(size * scale)
        self.target_enemy = target_enemy
        self.damage = damage
        self.damage_type = damage_type
        length_x = target_pos[0] - start_pos[0]
        length_y = target_pos[1] - start_pos[1]
        tangential_length = math.sqrt(length_x ** 2 + length_y ** 2)
        factor = self.vel / tangential_length
        self.move_direction = [length_x * factor, length_y * factor]
        self.pos = list(start_pos)
        self.target_pos = target_pos

    def update_pos(self):
        """Moves the enemy by its speed into the target direction.

        Author:
            Kim Matt
        """
        self.pos = [self.pos[0] + self.move_direction[0], self.pos[1] + self.move_direction[1]]

    def is_at_target_pos(self) -> bool:
        """Checks whether the projectile is at its target position.

        Returns:
            bool: True when the projectile is in range of its target position, False if not.

        Author:
            Kim Matt
        """
        return self.target_pos[0] - self.vel < self.pos[0] < self.target_pos[0] + self.vel and self.target_pos[
            1] - self.vel < self.pos[1] < self.target_pos[1] + self.vel

    def render(self, window):
        """Renders the projectile onto the given surface.

        Author:
            Kim Matt
        """
        window.blit(self.image, (self.pos[0] - self.size // 2, self.pos[1] - self.size // 2))


class CanonBall(Projectile):
    """Basic canon ball.

    Attributes:
        vel (int): Speed with which the projectile flies over the board.
        size (int): Size of the projectile.
        target_enemy (Enemy): The enemy to be hit by the projectile.
        damage (int): The damage that the projectile causes to the enemy.
        damage_type (DamageTypes): The type of damage caused to the opponent.
        move_direction (tuple): The direction in which the projectile is flying per tick.
        pos (tuple): The current position of the projectile.
        target_pos (tuple): The target to which the projectile is flying.
        image (Surface): Image of the projectile.

    Author:
        Kim Matt
    """
    def __init__(self, target_pos: tuple, start_pos: tuple, scale: float, target_enemy):
        """Basic canon ball.

        Args:
            target_pos (tuple): The target to which the projectile is flying.
            start_pos (tuple): The position the projectile starts from.
            scale (float): The scale in which the game gets rendered.
            target_enemy (Enemy): The enemy to be hit by the projectile.

        Author:
            Kim Matt
        """
        vel = 20
        damage = 20
        Projectile.__init__(self, target_pos, start_pos, vel, target_enemy, damage, DamageTypes.normal, 10,
                            scale)
        self.image = pygame.image.load('./ressources/projectiles/Cannon_Ball.png')
        self.image = pygame.transform.scale(self.image, (int(10 * scale), int(10 * scale)))


class BigCanonBall(Projectile):
    """Bigger canon ball.

    Attributes:
        vel (int): Speed with which the projectile flies over the board.
        size (int): Size of the projectile.
        target_enemy (Enemy): The enemy to be hit by the projectile.
        damage (int): The damage that the projectile causes to the enemy.
        damage_type (DamageTypes): The type of damage caused to the opponent.
        move_direction (tuple): The direction in which the projectile is flying per tick.
        pos (tuple): The current position of the projectile.
        target_pos (tuple): The target to which the projectile is flying.
        image (Surface): Image of the projectile.

    Author:
        Moritz Nueske
    """
    def __init__(self, target_pos, start_pos, scale, target_enemy):
        """Bigger canon ball.

        Args:
            target_pos (tuple): The target to which the projectile is flying.
            start_pos (tuple): The position the projectile starts from.
            scale (float): The scale in which the game gets rendered.
            target_enemy (Enemy): The enemy to be hit by the projectile.

        Author:
            Moritz Nueske
        """
        vel = 20
        damage = 200
        Projectile.__init__(self, target_pos, start_pos, vel, target_enemy, damage, DamageTypes.normal, 10,
                            scale)
        self.image = pygame.image.load('./ressources/projectiles/Cannon_Ball.png')
        self.image = pygame.transform.scale(self.image, (int(10 * scale), int(10 * scale)))


class FireProjectile(Projectile):
    """Projectile made from fire.

    Attributes:
        vel (int): Speed with which the projectile flies over the board.
        size (int): Size of the projectile.
        target_enemy (Enemy): The enemy to be hit by the projectile.
        damage (int): The damage that the projectile causes to the enemy.
        damage_type (DamageTypes): The type of damage caused to the opponent.
        move_direction (tuple): The direction in which the projectile is flying per tick.
        pos (tuple): The current position of the projectile.
        target_pos (tuple): The target to which the projectile is flying.
        image (Surface): Image of the projectile.

    Author:
        Moritz Nueske
    """
    def __init__(self, target_pos: tuple, start_pos: tuple, scale: float, target_enemy):
        """Projectile made from fire.

        Args:
            target_pos (tuple): The target to which the projectile is flying.
            start_pos (tuple): The position the projectile starts from.
            scale (float): The scale in which the game gets rendered.
            target_enemy (Enemy): The enemy to be hit by the projectile.

        Author:
            Moritz Nueske
        """
        vel = 20
        damage = 25
        Projectile.__init__(self, target_pos, start_pos, vel, target_enemy, damage, DamageTypes.fire, 10,
                            scale)
        self.image = pygame.image.load('./ressources/projectiles/Cannon_Ball.png')
        self.image = pygame.transform.scale(self.image, (int(10 * scale), int(10 * scale)))


class IceProjectile(Projectile):
    """Projectile made from ice.

    Attributes:
        vel (int): Speed with which the projectile flies over the board.
        size (int): Size of the projectile.
        target_enemy (Enemy): The enemy to be hit by the projectile.
        damage (int): The damage that the projectile causes to the enemy.
        damage_type (DamageTypes): The type of damage caused to the opponent.
        move_direction (tuple): The direction in which the projectile is flying per tick.
        pos (tuple): The current position of the projectile.
        target_pos (tuple): The target to which the projectile is flying.
        image (Surface): Image of the projectile.

    Author:
        Moritz Nueske
    """
    def __init__(self, target_pos: tuple, start_pos: tuple, scale: float, target_enemy):
        """Projectile made from ice.

        Args:
            target_pos (tuple): The target to which the projectile is flying.
            start_pos (tuple): The position the projectile starts from.
            scale (float): The scale in which the game gets rendered.
            target_enemy (Enemy): The enemy to be hit by the projectile.

        Author:
            Moritz Nueske
        """
        vel = 20
        damage = 200
        Projectile.__init__(self, target_pos, start_pos, vel, target_enemy, damage, DamageTypes.ice, 10,
                            scale)
        self.image = pygame.image.load('./ressources/projectiles/Cannon_Ball.png')
        self.image = pygame.transform.scale(self.image, (int(10 * scale), int(10 * scale)))


class UltimateCanonBall(Projectile):
    """Ultimate canon ball.

    Attributes:
        vel (int): Speed with which the projectile flies over the board.
        size (int): Size of the projectile.
        target_enemy (Enemy): The enemy to be hit by the projectile.
        damage (int): The damage that the projectile causes to the enemy.
        damage_type (DamageTypes): The type of damage caused to the opponent.
        move_direction (tuple): The direction in which the projectile is flying per tick.
        pos (tuple): The current position of the projectile.
        target_pos (tuple): The target to which the projectile is flying.
        image (Surface): Image of the projectile.

    Author:
        Moritz Nueske
    """
    def __init__(self, target_pos: tuple, start_pos: tuple, scale: float, target_enemy):
        """Ultimate canon ball.

        Args:
            target_pos (tuple): The target to which the projectile is flying.
            start_pos (tuple): The position the projectile starts from.
            scale (float): The scale in which the game gets rendered.
            target_enemy (Enemy): The enemy to be hit by the projectile.

        Author:
            Moritz Nueske
        """
        vel = 20
        damage = 150
        Projectile.__init__(self, target_pos, start_pos, vel, target_enemy, damage, DamageTypes.ultimate,
                            15, scale)
        self.image = pygame.image.load('./ressources/projectiles/Cannon_Ball.png')
        self.image = pygame.transform.scale(self.image, (int(15 * scale), int(15 * scale)))

class EasterEggProjectile(Projectile):
    """Easter Egg Canon Ball, just for fun.

        Attributes:
            vel (int): Speed with which the projectile flies over the board.
            size (int): Size of the projectile.
            target_enemy (Enemy): The enemy to be hit by the projectile.
            damage (int): The damage that the projectile causes to the enemy.
            damage_type (DamageTypes): The type of damage caused to the opponent.
            move_direction (tuple): The direction in which the projectile is flying per tick.
            pos (tuple): The current position of the projectile.
            target_pos (tuple): The target to which the projectile is flying.
            image (Surface): Image of the projectile.

        Author:
            Kim Matt
        """

    def __init__(self, target_pos: tuple, start_pos: tuple, scale: float, target_enemy):
        """Easter Egg Canon Ball, just for fun.

        Args:
            target_pos (tuple): The target to which the projectile is flying.
            start_pos (tuple): The position the projectile starts from.
            scale (float): The scale in which the game gets rendered.
            target_enemy (Enemy): The enemy to be hit by the projectile.

        Author:
            Moritz Nueske
        """
        vel = 10
        damage = 20
        Projectile.__init__(self, target_pos, start_pos, vel, target_enemy, damage, DamageTypes.ultimate,
                            15, scale)
        self.image = pygame.image.load('./misc/help_pictures/Help_easter_egg.png')
        self.image = pygame.transform.scale(self.image, (int(30 * scale), int(30 * scale)))
        self.image = pygame.transform.rotate(self.image, random.randint(-180, 180))