import pygame
from enum import Enum, auto
from player import Player
from settings import (
    SCREEN_W,
    SCREEN_H,
    CEILING_H,
    GROUND_Y,
    SKY_COLOR,
    CEILING_COLOR,
    GROUND_COLOR,
    FPS,
)


class GameState(Enum):
    SPLASH = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Game:
    """Main game controller: loop, state machine, and background rendering.

    The background surface is baked once at startup and blitted each frame
    (clear-then-draw pattern — no per-entity erasure).
    """

    def __init__(self, screen: pygame.Surface, assets):
        self.screen = screen
        self.assets = assets
        self.clock = pygame.time.Clock()
        self.state = GameState.PLAYING
        self.background = self._bake_background()
        self.players = [
            Player("superman", self.assets),
            Player("goblin", self.assets),
        ]

    def _bake_background(self) -> pygame.Surface:
        """Create the static background: cyan sky, white ceiling, green ground."""
        surf = pygame.Surface((SCREEN_W, SCREEN_H))
        surf.fill(SKY_COLOR)
        pygame.draw.rect(surf, CEILING_COLOR, (0, 0, SCREEN_W, CEILING_H))
        pygame.draw.rect(surf, GROUND_COLOR, (0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y))
        return surf

    def update(self, dt: float) -> None:
        """Update all game entities by dt seconds."""
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.update(dt, keys)

    def draw(self) -> None:
        """Render one frame: blit background then flip display."""
        self.screen.blit(self.background, (0, 0))
        for player in self.players:
            player.draw(self.screen)
        pygame.display.flip()

    def run(self) -> None:
        """Main loop. Exits on window close (QUIT) or Delete key."""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        running = False
            self.update(dt)
            self.draw()
