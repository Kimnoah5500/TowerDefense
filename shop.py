import pygame 

class Shop:
    height = 100
    def __init__(self, x, y, width, scale):
        self.scale = scale
        self.x = x
        self.y = y
        self.width = width
        self.height = 100 * scale
        self.background_image = pygame.image.load('./ressources/interface/shop_background.png')
        self.background_image = pygame.transform.scale(self.background_image, (int(self.width), int(self.height)))
        self.background_image_2 = pygame.image.load('./ressources/interface/shop_background_2.png')
        self.background_image_2 = pygame.transform.scale(self.background_image_2, (int((self.width - 200 * scale) // 10), int(self.height - 20 * scale)))
        self.items = self.getItems()
        self.item_names = self.get_names()
        self.item_prices = self.get_prices()
        self.item_damages = self.get_damages()

    def render(self, window):
        font =  pygame.font.Font("./ressources/Alata-Regular.ttf",15)
        window.blit(self.background_image, (self.x, self.y))
        for i in range(0,10,2):
            window.blit(self.background_image_2, (self.x + self.width//10 * i  ,self.y + 10 * self.scale))
        for item in self.items:
            index = self.items.index(item)
            item = pygame.transform.scale(item, (int(self.scale * 60), int(self.scale * 80)))
            window.blit(item, (self.x + self.width//5 * index + (self.background_image_2.get_width() - item.get_width())//2, self.y + 10))
            self.items[index] = item

            Name = font.render(self.item_names[index], True, (48, 34, 18))
            NameRec = Name.get_rect(x = self.x + self.width//10 * (index*2 +1), y = self.y + 10)
            window.blit(Name, NameRec)

            Price = font.render("Price: " +str(self.item_prices[self.get_item_code(index)]), True, (48, 34, 18))
            PriceRec = Price.get_rect(x = self.x + self.width//10 * (index*2 +1), y = self.y + 25)
            window.blit(Price, PriceRec)

            Damage = font.render("Damage: "+str(self.item_damages[self.get_item_code(index)]), True, (48, 34, 18))
            DamageRec = Damage.get_rect(x = self.x + self.width//10 * (index*2 +1), y = self.y + 40)
            window.blit(Damage, DamageRec)
            

    def getItems(self):
        basic_tower = pygame.image.load('./ressources/towers/Basic_tower.png')
        test = pygame.image.load('./ressources/Test.png')
        test2 = pygame.image.load('./ressources/Test.png')
        return [basic_tower, test, test2]

    def get_prices(self):
        return {"bato":200, "test":500, "test2":0}

    def get_names(self):
        return ["Basic Tower", "Test Tower", "Test Tower"]

    def get_damages(self):
        return {"bato":20, "test":0, "test2":0}

    def get_item_code(self, index):
        codes = ["bato", "test", "test2"]
        return codes[index]

    def check_if_affordable(self, index, player):
        code = self.get_item_code(index)
        if player.get_current_money() >= self.item_prices[code]:
            return True
        else:
            return False

    def buy_item(self, index, player):
        code = self.get_item_code(index)
        if player.get_current_money() >= self.item_prices[code]:
            player.reduce_money(self.item_prices[code])
            return True
        else:
            return False

    def checkShopClick(self, x, y, player):
        for item in self.items:
            index = self.items.index(item)
            self.rect = item.get_rect(x = self.x + self.width//5 * index + (self.background_image_2.get_width() - item.get_width())//2, y = self.y + 10)
            if self.rect.collidepoint(x,y) and self.check_if_affordable(index, player):
                return True, index
        return False, None

    def dragItem(self, index, pos, window, tower_manager):
        tower_range = tower_manager.get_range_from_tower_code(self.get_item_code(index))
        range_rect = pygame.Rect(0,0, tower_range*2, tower_range*2)
        range_rect.center = pos
        overlay = pygame.Surface((tower_range * 2, tower_range*2))
        overlay.set_alpha(180)
        overlay.fill((61, 61, 60))
        window.blit(overlay, range_rect.topleft)

        self.rect.center = pos
        window.blit(self.items[index], self.rect)
        

