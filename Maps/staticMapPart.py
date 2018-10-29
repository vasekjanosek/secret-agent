import pygame, csv
from Maps.mapPart import MapPart


class StaticMapPart(MapPart):
    def __init__(self, name, x, y, image, opacity):
        MapPart.__init__(self, name, x, y)
        self.image = image
        self.opacity = opacity

    def draw(self, screen):
        i = 0
        for static_part in self.static_parts:
            img = pygame.transform.scale(static_part.image, (32, 32))
            rect = img.get_rect()
            rect.center = static_part.position
            screen.blit(img, rect)
            i += 1

    def collisionLeft(self, part, agent):
        if agent.position[0] + agent.X_BORDER_COLLISION > part.position[0] > agent.position[0]:
            if agent.position[1] + agent.Y_BORDER_COLLISION > part.position[1] and agent.position[1] < part.position[1] + agent.Y_BORDER_COLLISION:
                agent.position = (part.position[0] - agent.X_BORDER_COLLISION, agent.position[1])

    def collisionRight(self, part, agent):
        if agent.position[0] < part.position[0] + agent.X_BORDER_COLLISION < agent.position[0] + agent.X_BORDER_COLLISION:
            if agent.position[1] + agent.Y_BORDER_COLLISION > part.position[1] and agent.position[1] < part.position[1] + agent.Y_BORDER_COLLISION:
                agent.position = (part.position[0] + agent.X_BORDER_COLLISION, agent.position[1])

    def collisionDown(self, part, agent):
        if agent.position[1] + agent.Y_BORDER_COLLISION >= part.position[1] >= agent.position[1]:
            if agent.position[0] + agent.X_BORDER_COLLISION > part.position[0] and agent.position[0] < part.position[0] + agent.X_BORDER_COLLISION:
                agent.groundReached(part.position[1] - agent.Y_BORDER_COLLISION)

    def collisionUp(self, part, agent):
        if agent.position[1] - agent.Y_BORDER_COLLISION <= part.position[1] <= agent.position[1]:
            if agent.position[0] + agent.X_BORDER_COLLISION > part.position[0] > agent.position[0] and agent.position[0] < part.position[0] + agent.X_BORDER_COLLISION:
                agent.position = (agent.position[0], part.position[1] + agent.Y_BORDER_COLLISION)
                agent.velocity = 0