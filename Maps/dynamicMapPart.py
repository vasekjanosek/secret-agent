import pygame, csv
from Maps.mapPart import MapPart


class DynamicMapPart(MapPart):
    def __init__(self, img_filename):
        self.img_filename = img_filename
        self.collection = []

    def move(self, agent_position):
        for item in self.collection:
            item.move(agent_position)

    def draw(self, screen):
        for item in self.collection:
            item.draw(screen)
