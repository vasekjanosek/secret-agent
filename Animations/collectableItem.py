import pygame


class CollectableItem(object):
    def __init__(self, filename, x, y, source_x, source_y):
        self.x = x
        self.y = y
        self.img = pygame.image.load(filename)
        rect = pygame.Rect((source_x , source_y, 16, 16))
        self.img = pygame.Surface(rect.size).convert()
        self.img.set_colorkey((86, 118, 255))
        self.img.blit(self.img, (0, 0), rect)
