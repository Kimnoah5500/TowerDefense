import pygame 

class Shop:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = 100
        self.image = pygame.image.load('./ressources/shop.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.items = self.getItems()

    def render(self, window):
        window.blit(self.image ,(self.x, self.y))
        for item in self.items:
            index = self.items.index(item)
            item = pygame.transform.scale(item, (self.height - 20, self.height - 20))
            window.blit(item, (self.x + index * (item.get_width() + 10), self.y + 10))
            self.items[index] = item

    def getItems(self):
        basic_tower = pygame.image.load('./ressources/Basic_tower.png')
        test = pygame.image.load('./ressources/Test.png')
        return [basic_tower, test]

    def checkShopClick(self, x,y):
        for item in self.items:
            index = self.items.index(item)
            self.rect = item.get_rect(x = self.x + index * (item.get_width() + 10), y = self.y + 10)
            if self.rect.collidepoint(x,y):
                return True, index
        return False, None

    def dragItem(self, index, pos, window):
        self.rect.center = pos
        window.blit(self.items[index], self.rect)
        

