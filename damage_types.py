from enum import Enum

class DamageTypes(Enum):
    """Defines the different types of damage

    Author:
        Moritz Nüske
    """
    normal = 1
    fire = 2
    ice = 3
    ultimate = 4