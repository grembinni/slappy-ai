import pygame
from settings import SCREEN_W, SCREEN_H
from assets import AssetCache
from splash import run_splash
from game import Game


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Goblin vs. Superman")
    assets = AssetCache()
    while True:
        win_score = run_splash(screen, assets)
        game = Game(screen, assets, win_score)
        result = game.run()
        if result != "restart":
            break
    pygame.quit()


if __name__ == "__main__":
    main()
