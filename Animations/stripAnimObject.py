import pygame


# represent one animation object
class StripAnimObject(object):
    def __init__(self, filename, x, y, count_to_right):
        self.filename = filename
        self.count_to_right = count_to_right
        self.x = x
        self.y = y
        self.images = []
        self.img = pygame.image.load(filename)
        self.actualPicture = 0

        for i in range(0, count_to_right):
            rect = pygame.Rect((x + (i * 16), y, 16, 16))
            img = pygame.Surface(rect.size).convert()
            img.set_colorkey((86, 118, 255))
            img.blit(self.img, (0, 0), rect)
            self.images.append(img)

    def next(self, slowdown=0):
        if slowdown == 0:
            self.actualPicture += 1
        if self.actualPicture == self.count_to_right:
            self.actualPicture = 0
            return self.actualPicture

        return self.actualPicture
