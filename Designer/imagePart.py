import pygame


class ImagePart(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self, screen, posX, posY):
        img = pygame.transform.scale(self.img, (32, 32))
        rect = img.get_rect()
        rect.center = (posX, posY)
        screen.blit(img, rect)
