import pathlib
import random
import sys

import pygame

from settings import (
    SCREEN_W, SCREEN_H, WIN_SCORE, DISPLAY_SPRITE_SIZE,
    SKY_COLOR, CEILING_COLOR, GROUND_COLOR, CEILING_H, GROUND_Y,
)

_MUSIC_PATH = pathlib.Path(__file__).parent / "assets" / "sounds" / "canyon.wav"

_CREDITS = [
    "President: Senior Airman",
    "CEO: Senior Airman",
    "CFO: Senior Airman",
    "Board of Directors: Senior Airman",
    "Lead Designer: Airman Hurdle",
    "Lead Artist: Airman Hurdle",
    "Lead Programmer: Airman Hurdle",
    "Lead Level Designer: Airman Hurdle",
    "Senior Assistant Designer: Senior Airman",
    "Senior Hardware Administrator: Airman Jarvis",
    "Senior Assistant Artist: Airman Hurdle",
    "Senior Assistant Programmer: Airman Hurdle",
    "Senior Assistant Level Designer: Airman Hurdle",
    "Junior Assistant Designer: Airman Basic Parrott",
    "Junior Assistant Artist: Airman Basic Kollars",
    "Junior Assistant Programmer: Airman Basic Anderson",
    "Junior Assistant Level Designer: Airman Basic Kollars",
    "Junior Code Realigner: Airman Basic Barney",
    "Software Design Style Consultant: Airman Basic Christen",
    "Secondary Motivator: Staff Sergeant Drennen",
    "Best Boy Grip: Airman Basic Zernicke",
    "Token Retard: Airman Carlson",
    "Token Cuban A1C: Airman First Class Magby",
    "",
    "Special Thanks To Hurdle's Mom",
]

# Controls strings — referenced by tests (UI-03)
_CONTROLS = (
    "Superman: Arrows / Shift / Ctrl / Enter   |   Goblin: ESDF / R / Space / W"
)

_SUP_CONTROLS = [
    "Superman's Controls",
    "  UP ARROW   = Up",
    "  DOWN ARROW  = Down",
    "  LEFT ARROW  = Left",
    "  RIGHT ARROW = Right",
    "  SHIFT       = Shoots",
    "  CONTROL     = Poses",
    "  ENTER       = Restart after death",
]

_GOB_CONTROLS = [
    "Goblin's Controls",
    "  E     = Up",
    "  D     = Down",
    "  S     = Left",
    "  F     = Right",
    "  R     = Shoots",
    "  SPACE = Poses",
    "  W     = Restart after death",
]


def _bake_background() -> pygame.Surface:
    """Recreate the gameplay backdrop: cyan sky, white ceiling, green ground."""
    surf = pygame.Surface((SCREEN_W, SCREEN_H))
    surf.fill(SKY_COLOR)
    pygame.draw.rect(surf, CEILING_COLOR, (0, 0, SCREEN_W, CEILING_H))
    pygame.draw.rect(surf, GROUND_COLOR, (0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y))
    return surf


def _draw(screen, background, font_title, font_welcome, font_ctrl_hdr,
          font_ctrl, font_credits, font_hint, sprite, credit_idx, win_score):
    screen.blit(background, (0, 0))
    cx = SCREEN_W // 2

    def _blit_center(text, font, y, color=(255, 255, 255), shadow=(20, 20, 80)):
        sh = font.render(text, True, shadow)
        tx = font.render(text, True, color)
        screen.blit(sh, (cx - sh.get_width() // 2 + 2, y + 2))
        screen.blit(tx, (cx - tx.get_width()  // 2,    y))

    def _blit_left(text, font, x, y, color=(255, 255, 255), shadow=(20, 20, 80)):
        sh = font.render(text, True, shadow)
        tx = font.render(text, True, color)
        screen.blit(sh, (x + 2, y + 2))
        screen.blit(tx, (x,     y))

    # ── Title ────────────────────────────────────────────────────────────────
    _blit_center("Hurdle's Mom Inc. Intl.", font_title, 10)

    # ── Welcome text (VB6 lblIntro lines 1-2) ────────────────────────────────
    _blit_center("Welcome to the best game ever.", font_welcome, 78)
    _blit_center("They aren't bugs, they're features.", font_welcome, 106)

    # ── Sprite cycling ────────────────────────────────────────────────────────
    scaled = pygame.transform.scale(sprite, (DISPLAY_SPRITE_SIZE, DISPLAY_SPRITE_SIZE))
    screen.blit(scaled, (cx - DISPLAY_SPRITE_SIZE // 2, 142))

    # ── Controls: two columns (VB6 lblIntro lines 4-end) ─────────────────────
    ctrl_y    = 268
    line_h    = 23
    left_x    = cx - 400
    right_x   = cx + 20
    hdr_color = (255, 255, 180)   # warm white for section headers
    body_color = (255, 255, 255)

    for i, line in enumerate(_SUP_CONTROLS):
        color = hdr_color if i == 0 else body_color
        _blit_left(line, font_ctrl_hdr if i == 0 else font_ctrl,
                   left_x, ctrl_y + i * line_h, color=color)

    for i, line in enumerate(_GOB_CONTROLS):
        color = hdr_color if i == 0 else body_color
        _blit_left(line, font_ctrl_hdr if i == 0 else font_ctrl,
                   right_x, ctrl_y + i * line_h, color=color)

    # ── Credits (cycling) ─────────────────────────────────────────────────────
    line = _CREDITS[credit_idx]
    if line:
        _blit_center(line, font_credits, 468, color=(255, 255, 100))

    # ── Win score selector ────────────────────────────────────────────────────
    _blit_center(f"Win Score: {win_score}  (Up/Down to change)", font_hint, 520)

    # ── Dismiss hint ──────────────────────────────────────────────────────────
    _blit_center("Press any key or click to start", font_hint, 568,
                 color=(200, 200, 200))

    pygame.display.flip()


def run_splash(screen: pygame.Surface, assets) -> int:
    """Display the start-game splash and return the selected win score.

    Background is the gameplay backdrop (sky/ceiling/ground).
    Up/Down adjust win score (10–500 in steps of 10).
    Any other key or mouse click starts the game.
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load(str(_MUSIC_PATH))
    pygame.mixer.music.play(0)   # play once, not looped

    background = _bake_background()

    font_title    = pygame.font.Font(None, 56)
    font_welcome  = pygame.font.Font(None, 24)
    font_ctrl_hdr = pygame.font.Font(None, 22)
    font_ctrl     = pygame.font.Font(None, 19)
    font_credits  = pygame.font.Font(None, 26)
    font_hint     = pygame.font.Font(None, 22)

    sprite_surfaces = list(assets.sprites.values())
    current_sprite  = random.choice(sprite_surfaces)
    sprite_timer    = 0.0
    credit_idx      = 0
    credit_timer    = 0.0
    win_score       = WIN_SCORE
    clock           = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        sprite_timer += dt
        credit_timer += dt

        if sprite_timer >= 0.75:
            sprite_timer -= 0.75
            current_sprite = random.choice(sprite_surfaces)

        if credit_timer >= 1.5:
            credit_timer -= 1.5
            credit_idx = (credit_idx + 1) % len(_CREDITS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    win_score = min(500, win_score + 10)
                elif event.key == pygame.K_DOWN:
                    win_score = max(10, win_score - 10)
                else:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        _draw(screen, background, font_title, font_welcome, font_ctrl_hdr,
              font_ctrl, font_credits, font_hint, current_sprite, credit_idx, win_score)

    return win_score
