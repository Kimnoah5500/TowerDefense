import pygame 

class Shop:
    """Class fo rendering and managing the shop and all buyable items.
    
    Attributes:
        scale (float): The scaling factor used to manage the size of the game.
        x (int): The top left x coordinate of the shop.
        y (int): The top left y coordinate of the shop. 
        width (int): The width of the shop.
        height (int): The height of the shop.
        background_image (pygame.Surface): The background of the shop.
        background_image_2 (pygame.Surface): The background for each item slot.
        items (List): List with all buyable items as images.
        item_names (List): List with the names of the items.
        item_prices (Dict): Dict with the prices for each item, key = itemcode.
        item_damages (Dict): Dict with the damages of each item, key = itemcode.
        item_damage_types (Dict): Dict with the damage type of each item, key = itemcode.

    Author:
        Moritz Nüske
    """

    height = 100
    def __init__(self, x, y, scale, window_with):
        """The shop for buying new towers.

        Args:
            x (int): The top left x coordinate of the shop.
            y (int): The top left y coordinate of the shop.
            scale (float): The scaling factor used to manage the size of the game.
            window_with (int): The width of the game window.

        Author:
            Moritz Nüske
        """
        self.scale = scale
        self.x = x
        self.y = y
        self.width = 1000 * scale
        self.height = 100 * scale
        self.background_image = pygame.image.load('./ressources/interface/shop_background.png')
        self.background_image = pygame.transform.scale(self.background_image, (int(window_with), int(self.height)))
        self.background_image_2 = pygame.image.load('./ressources/interface/shop_background_2.png')
        self.background_image_2 = pygame.transform.scale(self.background_image_2, (int((self.width - 200 * scale) // 10), int(self.height - 20 * scale)))
        self.items = self.getItems()
        self.item_names = self.get_names()
        self.item_prices = self.get_prices()
        self.item_damages = self.get_damages()
        self.item_damage_types = self.get_damage_types()

    def render(self, window):
        """Renders the shop with all items and descritptions

        Args:
            window (Surface): Surface on which the bar should be drawn.

        Author:
            Moritz Nüske
        """
        font = pygame.font.Font("./ressources/Alata-Regular.ttf", int(15 * self.scale))
        window.blit(self.background_image, (0, self.y))
        for i in range(0, 10, 2):
            window.blit(self.background_image_2, (self.x + self.width // 10 * i, self.y + 10 * self.scale))
        for item in self.items:
            index = self.items.index(item)
            item = pygame.transform.scale(item, (int(self.scale * 60), int(self.scale * 80)))
            window.blit(item, (
            self.x + self.width // 5 * index + (self.background_image_2.get_width() - item.get_width()) // 2,
            self.y + 10))
            self.items[index] = item

            Name = font.render(self.item_names[index], True, (48, 34, 18))
            NameRec = Name.get_rect(x=self.x + self.width // 10 * (index * 2 + 1), y=self.y + 10)
            window.blit(Name, NameRec)

            Price = font.render("Price: " + str(self.item_prices[self.get_item_code(index)]), True, (48, 34, 18))
            PriceRec = Price.get_rect(x=self.x + self.width // 10 * (index * 2 + 1), y=self.y + 25)
            window.blit(Price, PriceRec)

            Damage = font.render("Dps: " + str(self.item_damages[self.get_item_code(index)]), True, (48, 34, 18))
            DamageRec = Damage.get_rect(x=self.x + self.width // 10 * (index * 2 + 1), y=self.y + 40)
            window.blit(Damage, DamageRec)

            Type = font.render("Type: " + str(self.item_damage_types[self.get_item_code(index)]), True, (48, 34, 18))
            TypeRec = Type.get_rect(x=self.x + self.width // 10 * (index * 2 + 1), y=self.y + 55)
            window.blit(Type, TypeRec)

    def getItems(self):
        """Get all buyable items in the shop

        Returns:
            list: All buyable items as images.

        Author:
            Moritz Nüske
        """
        basic_tower = pygame.image.load('./ressources/towers/Basic_tower.png')
        sniper_tower = pygame.image.load('./ressources/towers/Sniper_tower.png')
        flame_tower = pygame.image.load('./ressources/towers/Flame_tower.png')
        ice_tower = pygame.image.load('./ressources/towers/Ice_tower.png')
        ultimate_tower = pygame.image.load('./ressources/towers/Ultimate_tower.png')
        return [basic_tower, sniper_tower, flame_tower, ice_tower, ultimate_tower]

    def get_prices(self):
        """Get prices of all items

        Returns:
            dict: Prices for each item as int. Key = itemcode.

        Author:
            Moritz Nüske
        """
        return {"bato": 200, "snto": 600, "flto": 900, "icto": 1500, "ulto": 6000}

    def get_names(self):
        """Get names of each item

        Returns:
            list: All names as strings.

        Author:
            Moritz Nüske
        """
        return ["Basic Tower", "Sniper Tower", "Flame Tower", "Ice Tower", "Ultiamte Tower"]

    def get_damages(self):
        """Get damage of each item

        Returns:
            dict: Damage of each item as int. Key = itemcode.

        Author:
            Moritz Nüske
        """
        return {"bato": 100, "snto": 400, "flto": 500, "icto": 800, "ulto": 1500}

    def get_damage_types(self):
        """Get damage type of each item

        Returns:
            dict: Damage type of each item as string. Key = itemcode.

        Author:
            Moritz Nüske
        """
        return {"bato": "normal", "snto": "normal", "flto": "fire", "icto": "ice", "ulto": "ultimate"}

    def get_item_code(self, index):
        """Get the code of a item from its index

        Args:
            index (int): Index of the item.

        Returns:
            str: Code of the item

        Author:
            Moritz Nüske
        """
        codes = ["bato", "snto", "flto", "icto", "ulto"]
        return codes[index]

    def check_if_affordable(self, index, player):
        """Checks if a item is affordable

        Args:
            index (int): Index of the item.
            player (Player): The current player.

        Returns:
            bool: True if item is affordable, else false

        Author:
            Moritz Nüske
        """
        code = self.get_item_code(index)
        if player.get_current_money() >= self.item_prices[code]:
            return True
        else:
            return False

    def buy_item(self, index, player):
        """Buys an item from the shop

        Args:
            index (int): Index of the item.
            player (Player): The current player.

        Returns:
            bool: True if item has been buyed, else false

        Author:
            Moritz Nüske
        """
        code = self.get_item_code(index)
        if player.get_current_money() >= self.item_prices[code]:
            player.reduce_money(self.item_prices[code])
            return True
        else:
            return False

    def checkShopClick(self, x, y, player):
        """Checks if the player clicked on an shop item

        Args:
            x (int): X position of the click.
            y (int): Y position of the click.
            player (Player): The current player.

        Returns:
            bool: True if the player clicked on an item and it it affordable, else false
            int:  The index of the clicked item if ture, else none

        Author:
            Moritz Nüske
        """
        for item in self.items:
            index = self.items.index(item)
            self.rect = item.get_rect(
                x=self.x + self.width // 5 * index + (self.background_image_2.get_width() - item.get_width()) // 2,
                y=self.y + 10)
            if self.rect.collidepoint(x, y) and self.check_if_affordable(index, player):
                return True, index
        return False, None

    def dragItem(self, index, pos, window, tower_manager):
        """Renders the dragging of an item

        Args:
            index (int): Index of the item.
            pos (int,int):Position of the mouse
            window (Surface): Surface on which the bar should be drawn.
            tower_manager (TowerManager): The active Tower Manager.

        Author:
            Moritz Nüske
        """
        tower_range = tower_manager.get_range_from_tower_code(self.get_item_code(index))
        self.draw_range(pos, window, tower_range)
        window.blit(self.items[index], self.rect)

    def draw_range(self, pos, window, range):
        """Renders a rectangle arround an item representing the range

        Args:
            pos (int,int):Position of the mouse
            window (Surface): Surface on which the bar should be drawn.
            range (int): The range of the item.

        Author:
            Moritz Nüske
        """
        range_rect = pygame.Rect(0, 0, range * 2, range * 2)
        range_rect.center = pos
        overlay = pygame.Surface((range * 2, range * 2))
        overlay.set_alpha(180)
        overlay.fill((61, 61, 60))
        window.blit(overlay, range_rect.topleft)

        self.rect.center = pos