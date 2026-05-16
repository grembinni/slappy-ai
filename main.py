import pygame
from settings import SCREEN_W, SCREEN_H
from assets import AssetCache
from game import Game


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Goblin vs. Superman")
    assets = AssetCache()
    game = Game(screen, assets)
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
