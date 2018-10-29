import pygame

class Projectile(object):
    def __init__(self, animation, position, vector):
        self.position = (position[0] + (vector[0]*16), position[1] + (vector[1]*16))
        self.animation = animation
        self.vector = vector
        self.move_by = 5
        self.moved = 0
        self.animation_speed = 5

    def move(self):
        self.position = (self.position[0] + (self.vector[0]*5), self.position[1] + (self.vector[1]*5))
        if self.moved <= self.move_by:
            self.moved += 1
        else:
            self.moved = 0

    def draw(self, screen):
        img = self.animation.images[self.animation.next(self.moved % self.animation_speed)]
        img = pygame.transform.scale(img, (32, 32))
        rect = img.get_rect()
        rect.center = self.position
        screen.blit(img, rect)

    def collision(self, agent):
        if agent.position[0] +32 >= self.position[0] >= agent.position[0] and agent.position[1] +32 >= self.position[1] +32 >= agent.position[1]:
            agent.lower_life()
            return True
        return False
