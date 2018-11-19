import pygame, csv
from Maps.staticMapPart import StaticMapPart
from Maps.dynamicMapPart import DynamicMapPart
from Animations.enemySoldier import EnemySoldier


# represents Base/Level map
class Map(object):

    # img_filename - grapi
    # map_filename - map definition
    def __init__(self, img_filename, map_filename):
        self.img_filename = img_filename
        self.map_filename = map_filename
        self.dynamic_parts = []
        self.static_parts = []
        self.enemies = []
        self.initialize_map()

    def move(self, agent_position):
        for part in self.dynamic_parts:
            part.move(agent_position)
        for enemy in self.enemies:
            enemy.move(agent_position)
    
    def draw(self, screen, display_size):
        # draws statusbar
        stat_bar_rect = pygame.Rect(0, display_size[1] - 20, display_size[0], 20)
        screen.fill((0, 0, 0), stat_bar_rect)

        # draws map
        for static_part in self.static_parts:
            img = pygame.transform.scale(static_part.image, (32, 32))
            rect = img.get_rect()
            rect.center = static_part.position
            screen.blit(img, rect)

            # deraws enemies
        for enemy in self.enemies:
            enemy.draw(screen)

    def collisionDetection(self, agent):
        axisX = agent.move_vector[0]
        shouldFall = False
        if not agent.isJumping:
            shouldFall = True

        for part in self.static_parts:
            if part.opacity > 0:
                continue
            # jumping
            if agent.move_vector[1] < 0:
                part.collisionDown(part, agent)
            # falling
            if agent.move_vector[1] > 0:
                part.collisionUp(part, agent)

            # moving left
            if axisX < 0:
                part.collisionRight(part, agent)
            # moving right
            if axisX > 0:
                part.collisionLeft(part, agent)

            if agent.position[0] + agent.X_BORDER_COLLISION > part.position[0] and agent.position[0] < part.position[0] + agent.X_BORDER_COLLISION:
                shouldFall = False

        for enemy in self.enemies:
            if enemy.collision(agent):
                agent.lower_life()

        if shouldFall:
            agent.fall()

    def initialize_map(self):
        source_image = pygame.image.load(self.img_filename)
        with open(self.map_filename, 'r') as csv_file:
            file_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in file_reader:
                if str(row[1]) == "s":
                    rect = pygame.Rect((int(row[4]), int(row[5]), 16, 16))
                    img = pygame.Surface(rect.size).convert()
                    img.blit(source_image, (0, 0), rect)
                    self.static_parts.append(StaticMapPart(row[0], int(row[2]), int(row[3]), img, int(row[6])))
                elif str(row[1]) == "e":
                    rect = pygame.Rect((int(row[3]), int(row[4]), 16, 16))
                    img = pygame.Surface(rect.size).convert()
                    img.blit(source_image, (0, 0), rect)
                    self.enemies.append(EnemySoldier(self.img_filename, int(row[2]), int(row[3]), int(row[4])))
