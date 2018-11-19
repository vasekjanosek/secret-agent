import pygame, sys, threading, time
from Animations.stripAnimObject import AnimationObject

DEFAULT_VELOCITY = 8
FLOOR_POSITION = 160
START_POSITION = (208, 160)
SOURCE_PICTURE = "Properties/agent_sprites.png"


# represent secret agent
class SecretAgent(object):

    def __init__(self, start_position):
        # sprites definition
        self.leftDirectionSprite = None
        self.rightDirectionSprite = None
        self.jumpSprite = None
        self.deathSprite = None

        # load sprites
        self.load_agent()

        # should he shoot
        self.shoot = False
        # direction of agent
        self.direction = 0
        # should he jump
        self.jump = False
        self.isJumping = False
        # is he moving
        self.move = False
        # start position of agent
        self.position = start_position
        # jump velocity(speed)
        self.velocity = DEFAULT_VELOCITY
        self.mass = 2
        # gravity
        self.onGround = True

        # load special images
        sidebarImgSource = pygame.image.load("Properties/Sidebar.png")
        rect = pygame.Rect((88, 16, 8, 8))
        sidebarImg = pygame.Surface(rect.size).convert()
        sidebarImg.set_colorkey((0,0,0))
        sidebarImg.blit(sidebarImgSource, (0, 0), rect)
        self.livesImg = sidebarImg

        # active keys registry
        self.enabledKeys = []
        self.move_vector = None
        self.lives = 3
        self.immortal = False
        self.death_anim_speed = 5
        self.death_path = 0
        self.return_to_menu = False

    def load_agent(self):
        self.leftDirectionSprite = AnimationObject(SOURCE_PICTURE, 0, 16, 4)
        self.rightDirectionSprite = AnimationObject(SOURCE_PICTURE, 0, 0, 4)
        self.jumpSprite = AnimationObject(SOURCE_PICTURE, 0, 48, 2)
        self.deathSprite = AnimationObject(SOURCE_PICTURE, 32, 48, 2)

    def draw(self, screen, display_size):
        img = self.leftDirectionSprite.images[0]
        if self.lives == 0:
            self.death_path += 1
            if self.death_path > self.death_anim_speed:
                self.death_path = 0
            img = self.deathSprite.images[self.deathSprite.next(self.death_path%self.death_anim_speed)]
        elif self.isJumping:
            if self.direction == -1:
                img = self.jumpSprite.images[1]
            else:
                img = self.jumpSprite.images[0]
        elif not self.onGround:
            if self.direction == -1:
                img = self.jumpSprite.images[1]
            else:
                img = self.jumpSprite.images[0]
        elif self.move:
            if self.direction == -1:
                img = self.leftDirectionSprite.images[self.leftDirectionSprite.next()]
            else:
                img = self.rightDirectionSprite.images[self.rightDirectionSprite.next()]
        else:
            if self.direction == -1:
                img = self.leftDirectionSprite.images[0]
            else:
                img = self.rightDirectionSprite.images[0]
        
        img = pygame.transform.scale(img, (32, 32))
        rect = img.get_rect()
        rect.center = self.position
        screen.blit(img, rect)

        # draw lives
        img = pygame.transform.scale(self.livesImg, (16, 16))
        rect = img.get_rect()
        for i in range(0, self.lives):
            rect.center = (display_size[0] - ((7-i)*16), display_size[1]-9)
            screen.blit(img, rect)
    
    def jumpAgent(self):
        if self.velocity > 0:
            F = ( 0.15 * self.mass * (self.velocity*self.velocity))
        else:
            F = - ( 0.15 * self.mass * (self.velocity*self.velocity))
 
        # Change position
        self.position = (self.position[0], self.position[1] - F)
        
        # Change velocity
        if self.velocity == 1:
            self.velocity = -1
        else:
            self.velocity = self.velocity - 1
        
        # If ground is reached, reset variables.
        if self.position[1] > FLOOR_POSITION:
            if self.return_to_menu:
                self.jump = False
                self.isJumping = False
            self.groundReached(FLOOR_POSITION)

        return F
    
    def groundReached(self, ground):
        self.position = (self.position[0], ground)
        self.velocity = DEFAULT_VELOCITY
        if not self.enabledKeys.__contains__(pygame.K_UP):
            self.jump = False
            self.isJumping = False

    def fall(self):
        self.isJumping = True
        self.jump = True
        self.velocity = -5
        self.jumpAgent()

    def die(self):
        self.jump = True
        self.isJumping = True
        self.jumpAgent()
        self.return_to_menu = True
        
    def moveAgent(self):
        if self.lives == 0 and not self.return_to_menu:
            self.die()
            return (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit(0)
            if not hasattr(event, 'key'): continue
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if not self.enabledKeys.__contains__(pygame.K_RIGHT):
                        self.enabledKeys.append(pygame.K_RIGHT)
                    self.move = True
                    self.direction = 1
                elif event.key == pygame.K_LEFT:
                    if not self.enabledKeys.__contains__(pygame.K_LEFT):
                        self.enabledKeys.append(pygame.K_LEFT)
                    self.move = True
                    self.direction = -1
                elif event.key == pygame.K_UP:
                    self.jump = True
                    self.isJumping = True
                    if not self.enabledKeys.__contains__(pygame.K_UP):
                        self.enabledKeys.append(pygame.K_UP)
                elif event.key == pygame.K_SPACE:
                    #shoot
                    shoot = True
                elif event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.enabledKeys.remove(pygame.K_RIGHT)
                    self.move = False
                    if self.enabledKeys.__contains__(pygame.K_LEFT):
                        self.direction = -1
                        self.move = True
    
                elif event.key == pygame.K_LEFT:
                    self.move = False
                    self.enabledKeys.remove(pygame.K_LEFT)
                    if self.enabledKeys.__contains__(pygame.K_RIGHT):
                        self.direction = 1
                        self.move = True
                
                elif event.key == pygame.K_UP:
                    self.enabledKeys.remove(pygame.K_UP)
                    self.jump = False

        if self.move:
            if self.direction == -1:
                    self.position = (self.position[0] - 5, self.position[1])
            else:
                    self.position = (self.position[0] + 5, self.position[1])

        F = 0
        if self.jump or self.isJumping:
            F = self.jumpAgent()

        moveX = 0
        if self.direction == -1 and self.enabledKeys.__contains__(pygame.K_LEFT):
            moveX = -1
        elif self.direction == 1 and self.enabledKeys.__contains__(pygame.K_RIGHT):
            moveX = 1

        self.move_vector = (moveX, F)

    def lower_life(self):
        if not self.immortal:
            print(self.lives)
            self.immortal = True
            self.lives -= 1
            if self.lives == 0:
                return False
            countdown_handler = threading.Thread(target=immortality_countdown, args=(self,))
            countdown_handler.start()
        return True

def immortality_countdown(self):
    time.sleep(3)
    self.immortal = False
