from collections import deque

import pygame
from enum import Enum, auto
from player import Player, CharState
from hud import draw_hud
from sound import SoundManager
from settings import (
    SCREEN_W,
    SCREEN_H,
    CEILING_H,
    GROUND_Y,
    SKY_COLOR,
    CEILING_COLOR,
    GROUND_COLOR,
    FPS,
    DIR_LEFT,
    DIR_RIGHT,
    DIR_IDLE,
    WIN_SCORE,
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
        self.osg_score: int = 0
        self._hud_font = pygame.font.Font(None, 28)
        self.snd = SoundManager(assets.sounds)
        self.snd.play_playing_music()

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
        was_crashing = [p.state == CharState.CRASHING for p in self.players]
        for player in self.players:
            player.update(dt, keys)
        for i, player in enumerate(self.players):
            if was_crashing[i] and player.state == CharState.DEAD:
                self.snd.play_explode()

        # Update beams and remove expired ones (CMB-06)
        for player in self.players:
            player.beams = deque(
                (b for b in player.beams if b.update(dt)),
                maxlen=10,
            )

        # Collision detection: beam hits living opponent → CRASHING (CMB-07, CMB-08)
        for i, player in enumerate(self.players):
            if player.state != CharState.ALIVE:
                continue
            opponent = self.players[1 - i]
            for beam in list(opponent.beams):
                if beam.direction in (DIR_LEFT, DIR_RIGHT):  # CMB-08: VB6 Or-bug fix
                    if player.rect.clipline(beam.start, beam.end):
                        player.start_crash()
                        self.snd.play_death_cry()
                        self.players[1 - i].hit_bonus += 10
                        break

        # Pose score: +1 per frame idle-airborne (SCR-02)
        for player in self.players:
            if (player.state == CharState.ALIVE
                    and player._direction == DIR_IDLE
                    and not player._on_ground):
                player.raw_pose += 1

        # Win condition (SCR-06)
        if self.state == GameState.PLAYING:
            for player in self.players:
                if player.score >= WIN_SCORE:
                    self.state = GameState.GAME_OVER
            if self.osg_score >= WIN_SCORE:
                self.state = GameState.GAME_OVER
            if self.state == GameState.GAME_OVER:
                self.snd.stop_music()

    def draw(self) -> None:
        """Render one frame: blit background then flip display."""
        self.screen.blit(self.background, (0, 0))
        for player in self.players:
            player.draw(self.screen)
        for player in self.players:
            for beam in player.beams:
                beam.draw(self.screen)
        draw_hud(self.screen, self.players, self.osg_score, self._hud_font)
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
                    elif event.key == pygame.K_KP0:
                        sup = self.players[0]
                        if sup.state == CharState.ALIVE:
                            d = sup.facing if sup.facing in (DIR_LEFT, DIR_RIGHT) else DIR_LEFT
                            sup.fire(d)
                            self.snd.play_laser()
                    elif event.key == pygame.K_e:
                        gob = self.players[1]
                        if gob.state == CharState.ALIVE:
                            d = gob.facing if gob.facing in (DIR_LEFT, DIR_RIGHT) else DIR_RIGHT
                            gob.fire(d)
                            self.snd.play_laser()
                    elif event.key == pygame.K_UP:
                        sup = self.players[0]
                        if sup.state == CharState.DEAD:
                            sup.respawn()
                    elif event.key == pygame.K_w:
                        gob = self.players[1]
                        if gob.state == CharState.DEAD:
                            gob.respawn()
                    elif event.key == pygame.K_m:
                        self.snd.toggle_mute()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for player in self.players:
                        if player.state == CharState.ALIVE and player.rect.collidepoint(event.pos):
                            player.start_crash()
                            self.snd.play_death_cry()
                            self.osg_score += 1
            self.update(dt)
            self.draw()
