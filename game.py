import pygame
from Animations.secretAgent import SecretAgent
from Maps.map import Map
from Menu.mainMenu import MainMenu

SOURCE_PICTURE = "Properties/SecretAgent.png"
SIDEBAR_PICTURE = "Properties/Sidebar.png"
TEST_MAP = "Properties/map2.csv"
MENU_FILE = "Properties/menu.csv"
BACKGROUND_COLOR = (86, 118, 255)
DISPLAY_SIZE = (500, 320)


def main():
    while 1:
        screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.DOUBLEBUF)
        clock = pygame.time.Clock()
        entire_map = Map(SOURCE_PICTURE, TEST_MAP)
        menu = MainMenu(SIDEBAR_PICTURE, MENU_FILE)
        agent = SecretAgent(SOURCE_PICTURE)
        while 1:
            if menu.key_check():
                break
            menu.draw_menu(screen)
            pygame.display.flip()

        while 1:
            clock.tick(30)
            agent.moveAgent()
            entire_map.move(agent.position)
            entire_map.collisionDetection(agent)
            screen.fill(BACKGROUND_COLOR)
            entire_map.draw(screen, DISPLAY_SIZE)
            agent.draw(screen, DISPLAY_SIZE)
            pygame.display.flip()
            if agent.return_to_menu and not agent.jump and not agent.isJumping:
                break


if __name__ == "__main__":
    main()
