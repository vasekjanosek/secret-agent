import pygame

# default background color
BACKGROUND_COLOR = (86, 118, 255)
# size of one sprite in pixels
PIXEL_SIZE = 16


# represents one animation object
class AnimationObject(object):

    # initialization of AnimationObject
    # x - x coordinates in image
    # y - y coordinates in image
    # count_to_right - number of sprites creating animation object
    def __init__(self, filename, x, y, count_to_right):

        self.count_to_right = count_to_right
        self.x = x
        self.y = y
        self.images = []
        self.img = pygame.image.load(filename)
        self.actualSpriteIndex = 0

        # loading sprites from given image
        for i in range(0, count_to_right):
            rect = pygame.Rect((x + (i * PIXEL_SIZE), y, PIXEL_SIZE, PIXEL_SIZE))
            img = pygame.Surface(rect.size).convert()
            img.set_colorkey(BACKGROUND_COLOR)
            img.blit(self.img, (0, 0), rect)
            self.images.append(img)

    # sets actualSpriteIndex to next sprite in row
    def next(self, slowdown=0):

        if slowdown == 0:
            self.actualSpriteIndex += 1

        if self.actualSpriteIndex == self.count_to_right:
            self.actualSpriteIndex = 0
            return self.actualSpriteIndex

        return self.actualSpriteIndex
