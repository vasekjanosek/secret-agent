import pygame
from Animations.stripAnimObject import StripAnimObject
from Animations.projectile import Projectile


class EnemySoldier(object):
    def __init__(self,filename, x, y, level):
        self.position = (x, y)
        self.level = level
        self.filename = filename
        self.level_one_left_anim = StripAnimObject(self.filename, 320, 224, 4)
        self.level_one_right_anim = StripAnimObject(self.filename, 320, 208, 4)
        self.level_two_left_anim = StripAnimObject(self.filename, 320, 256, 4)
        self.level_two_right_anim = StripAnimObject(self.filename, 320, 240, 4)
        self.level_three_left_anim = StripAnimObject(self.filename, 320, 288, 4)
        self.level_three_right_anim = StripAnimObject(self.filename, 320, 272, 4)
        self.level_four_left_anim = StripAnimObject(self.filename, 320, 320, 4)
        self.level_four_right_anim = StripAnimObject(self.filename, 320, 304, 4)
        self.level_five_left_anim = StripAnimObject(self.filename, 320, 352, 4)
        self.level_five_right_anim = StripAnimObject(self.filename, 320, 336, 4)
        self.direction = -1
        self.path_length = 50
        self.moved = 0
        self.animation_speed = 5
        self.projectile = None

    def move(self, agent_position):
        if self.moved <= self.path_length:
            self.moved += 1
            move_by = 1
            if self.level == 3:
                move_by = 3
            self.position = (self.position[0] + (self.direction * move_by), self.position[1])

        else:
            self.moved = 0
            self.direction *= -1

        if self.in_sight_line(agent_position) and self.projectile is None:
            animation, vector = self.get_projectile_animation()
            if animation is not None:
                self.projectile = Projectile(animation, self.position, vector)

        if self.projectile is not None:
            self.projectile.move()
            if self.projectile.position[0] < 0 or self.projectile.position[0] > 480:
                self.projectile = None

    def draw(self, screen):
        if self.direction == -1:
            img = {
                1: self.level_one_left_anim.images[self.level_one_left_anim.next(self.moved%self.animation_speed)],
                2: self.level_two_left_anim.images[self.level_two_left_anim.next(self.moved%self.animation_speed)],
                3: self.level_three_left_anim.images[self.level_three_left_anim.next(self.moved%self.animation_speed)],
                4: self.level_four_left_anim.images[self.level_four_left_anim.next(self.moved%self.animation_speed)],
                5: self.level_five_left_anim.images[self.level_five_left_anim.next(self.moved%self.animation_speed)]
            }[self.level]
        else:
            img = {
                1: self.level_one_right_anim.images[self.level_one_right_anim.next(self.moved%self.animation_speed)],
                2: self.level_two_right_anim.images[self.level_two_right_anim.next(self.moved%self.animation_speed)],
                3: self.level_three_right_anim.images[self.level_three_right_anim.next(self.moved%self.animation_speed)],
                4: self.level_four_right_anim.images[self.level_four_right_anim.next(self.moved%self.animation_speed)],
                5: self.level_five_right_anim.images[self.level_five_right_anim.next(self.moved%self.animation_speed)]
            }[self.level]

        img = pygame.transform.scale(img, (32, 32))
        rect = img.get_rect()
        rect.center = self.position
        screen.blit(img, rect)

        if self.projectile is not None:
            self.projectile.draw(screen)

    def in_sight_line(self, position):
        if ((self.position[0] > position[0] and self.direction == -1) or (self.position[0] < position[0] and self.direction == 1)) and position[1] == self.position[1]:
            return True
        return False

    def get_projectile_animation(self):
        if self.level == 4 or self.level == 5:
            return StripAnimObject(self.filename, 96, 144, 2), (self.direction, 0)
        else:
            return None, None

    def collision(self, agent):
        if agent.position[0] +32 >= self.position[0] >= agent.position[0] and agent.position[1] +32 >= self.position[1] +32 >= agent.position[1]:
            agent.lower_life()
            return True
        if self.projectile is not None:
            if self.projectile.collision(agent):
                agent.lower_life()
                return True
        return False
