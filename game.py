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

    def __init__(self, screen: pygame.Surface, assets, win_score: int = WIN_SCORE):
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
        self.win_score = win_score
        self._go_font  = pygame.font.Font(None, 56)
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
                if player.score >= self.win_score:
                    self.state = GameState.GAME_OVER
            if self.osg_score >= self.win_score:
                self.state = GameState.GAME_OVER
            if self.state == GameState.GAME_OVER:
                self.snd.stop_music()

    def draw(self) -> None:
        """Render one frame based on current game state."""
        if self.state == GameState.GAME_OVER:
            self._draw_game_over()
        else:
            self.screen.blit(self.background, (0, 0))
            for player in self.players:
                player.draw(self.screen)
            for player in self.players:
                for beam in player.beams:
                    beam.draw(self.screen)
            draw_hud(self.screen, self.players, self.osg_score, self._hud_font)
            if self.state == GameState.PAUSED:
                self._draw_pause_overlay()
        pygame.display.flip()

    def _draw_game_over(self) -> None:
        """GAME_OVER screen: dark navy background, final scores, restart prompt (D-17–D-19)."""
        self.screen.fill((0, 0, 64))
        sup, gob = self.players

        def _blit_center(text: str, font: pygame.font.Font, y: int,
                         color=(255, 255, 255)) -> None:
            surf = font.render(text, True, color)
            self.screen.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2, y))

        _blit_center("GAME OVER", self._go_font, SCREEN_H // 2 - 160, (255, 60, 60))
        _blit_center(f"Superman: {sup.score}",  self._hud_font, SCREEN_H // 2 - 60)
        _blit_center(f"Goblin: {gob.score}",    self._hud_font, SCREEN_H // 2 - 20)
        if self.osg_score > 0:
            _blit_center(
                f"OmnipotentShootingGuy: {self.osg_score}",
                self._hud_font, SCREEN_H // 2 + 20,
            )
        _blit_center("F2 or Enter to restart", self._hud_font,
                     SCREEN_H // 2 + 80, (200, 200, 200))

    def _draw_pause_overlay(self) -> None:
        """Semi-transparent dark overlay with centered PAUSED text (UI-05)."""
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))
        pause_font = pygame.font.Font(None, 96)
        surf = pause_font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2,
                                SCREEN_H // 2 - surf.get_height() // 2))

    def run(self):
        """Main loop. Returns 'restart' when F2/Enter pressed in GAME_OVER, else None."""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # Hard quit — always active
                    if event.key == pygame.K_DELETE:
                        running = False

                    # Mute — active in any game state
                    elif event.key == pygame.K_m:
                        self.snd.toggle_mute()

                    # Pause toggle — only when PLAYING or PAUSED
                    elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                        if self.state == GameState.PLAYING:
                            self.state = GameState.PAUSED
                            self.snd.pause_game()
                        elif self.state == GameState.PAUSED:
                            self.state = GameState.PLAYING
                            self.snd.resume_game()

                    # Restart — only from GAME_OVER
                    elif event.key in (pygame.K_F2, pygame.K_RETURN):
                        if self.state == GameState.GAME_OVER:
                            return "restart"

                    # All remaining keys only active during PLAYING
                    elif self.state == GameState.PLAYING:
                        if event.key == pygame.K_KP0:
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

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == GameState.PLAYING:
                        for player in self.players:
                            if player.state == CharState.ALIVE and player.rect.collidepoint(event.pos):
                                player.start_crash()
                                self.snd.play_death_cry()
                                self.osg_score += 1

            # Update only when actively playing
            if self.state == GameState.PLAYING:
                self.update(dt)

            self.draw()
