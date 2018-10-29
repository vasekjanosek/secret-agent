import pygame, csv, sys
from Menu.menuPart import MenuPart


class MainMenu(object):
    def __init__(self,  menu_image, menu_file):
        self.menu_image = menu_image
        self.menu_file = menu_file
        self.menu_items = []
        self.load_menu()
        #>= <

    def load_menu(self):
        source_image = pygame.image.load(self.menu_image)
        with open(self.menu_file, 'r') as csv_file:
            file_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in file_reader:
                rect = pygame.Rect((int(row[1]), int(row[2]), 8, 8))
                img = pygame.Surface(rect.size).convert()
                img.blit(source_image, (0, 0), rect)
                if int(row[5]) == 1:
                    pixarray = pygame.PixelArray(img)
                    for y in range(0, 8):
                        pixarray[7][y] = (0, 143, 0)
                self.menu_items.append(MenuPart(img, (int(row[3]),int(row[4])), str(row[0])))

    def draw_menu(self, screen):
        screen.fill((0, 0, 0))
        for item in self.menu_items:
            if item.popis == "pozadi":
                self.draw_pozadi(screen, item)
        # draws map
        for item in self.menu_items:
            img = pygame.transform.scale(item.image, (16, 16))
            rect = img.get_rect()
            rect.center = (item.position[0] + 8, item.position[1] + 8)
            img.set_colorkey((0, 143, 0))
            screen.blit(img, rect)

    def draw_pozadi(self, screen, item):
        for x in range(0, 7):
            for y in range(0, 7):
                img = pygame.transform.scale(item.image, (16, 16))
                rect = img.get_rect()
                rect.center = ((x*16) + 8, (y*16) + 8)
                screen.blit(img, rect)


    def key_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit(0)
            if not hasattr(event, 'key'): continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    sys.exit(0)
        return False
