import pathlib
import random
import sys

import pygame

from settings import (
    SCREEN_W, SCREEN_H, WIN_SCORE, DISPLAY_SPRITE_SIZE,
    SKY_COLOR, CEILING_COLOR, GROUND_COLOR, CEILING_H, GROUND_Y,
)

_MUSIC_PATH = pathlib.Path(__file__).parent / "assets" / "sounds" / "canyon.wav"

# 25 VB6 credits lines — moved to GAME_OVER screen; kept here for tests (UI-01)
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

# Controls summary — referenced by tests (UI-03)
_CONTROLS = (
    "Superman: Arrows / Shift / Ctrl / Enter   |   Goblin: ESDF / R / Space / W"
)

# VB6 lblIntro controls block (frmSuperman.frm lines 332-348)
_SUP_CONTROLS = [
    ("Superman's Controls", True),   # (text, is_header)
    ("UP ARROW   = Up",    False),
    ("DOWN ARROW  = Down", False),
    ("LEFT ARROW  = Left", False),
    ("RIGHT ARROW = Right",False),
    ("SHIFT       = Shoots",False),
    ("CONTROL     = Poses", False),
    ("ENTER       = Restart after death", False),
]

_GOB_CONTROLS = [
    ("Goblin's Controls", True),
    ("E     = Up",    False),
    ("D     = Down",  False),
    ("S     = Left",  False),
    ("F     = Right", False),
    ("R     = Shoots",False),
    ("SPACE = Poses", False),
    ("W     = Restart after death", False),
]


def _bake_background() -> pygame.Surface:
    """Gameplay backdrop: cyan sky, white ceiling strip, green ground."""
    surf = pygame.Surface((SCREEN_W, SCREEN_H))
    surf.fill(SKY_COLOR)
    pygame.draw.rect(surf, CEILING_COLOR, (0, 0, SCREEN_W, CEILING_H))
    pygame.draw.rect(surf, GROUND_COLOR, (0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y))
    return surf


def _draw(screen, background, font_title, font_welcome, font_ctrl_hdr,
          font_ctrl, font_hint, sprite, win_score):
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

    # ── Title ─────────────────────────────────────────────────────────────────
    _blit_center("Hurdle's Mom Inc. Intl.", font_title, 10)

    # ── Welcome lines (VB6 lblIntro lines 1–2) ────────────────────────────────
    _blit_center("Welcome to the best game ever.", font_welcome, 76)
    _blit_center("They aren't bugs, they're features.", font_welcome, 104)

    # ── Character sprite ───────────────────────────────────────────────────────
    scaled = pygame.transform.scale(sprite, (DISPLAY_SPRITE_SIZE, DISPLAY_SPRITE_SIZE))
    screen.blit(scaled, (cx - DISPLAY_SPRITE_SIZE // 2, 138))

    # ── Controls — two columns, centered as a pair ────────────────────────────
    # Column widths measured conservatively so total block straddles cx evenly.
    # Left col 250px + 60px gap + right col 220px = 530px total → starts at cx-265
    left_x  = cx - 265       # = 375
    right_x = left_x + 310   # = 685  (250 col + 60 gap)
    ctrl_y  = 268
    line_h  = 23

    for i, (text, is_hdr) in enumerate(_SUP_CONTROLS):
        font  = font_ctrl_hdr if is_hdr else font_ctrl
        color = (255, 255, 150) if is_hdr else (255, 255, 255)
        _blit_left(text, font, left_x, ctrl_y + i * line_h, color=color)

    for i, (text, is_hdr) in enumerate(_GOB_CONTROLS):
        font  = font_ctrl_hdr if is_hdr else font_ctrl
        color = (255, 255, 150) if is_hdr else (255, 255, 255)
        _blit_left(text, font, right_x, ctrl_y + i * line_h, color=color)

    # ── Win score selector ────────────────────────────────────────────────────
    _blit_center(f"Win Score: {win_score}  (Up/Down to change)", font_hint, 480)

    # ── Dismiss hint ──────────────────────────────────────────────────────────
    _blit_center("Press any key or click to start", font_hint, 524,
                 color=(200, 200, 200))

    pygame.display.flip()


def run_splash(screen: pygame.Surface, assets) -> int:
    """Display the start-game splash and return the selected win score.

    Background is the gameplay backdrop. Canyon.wav plays once.
    Up/Down adjust win score (10–500). Any other key or click starts the game.
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load(str(_MUSIC_PATH))
    pygame.mixer.music.play(0)   # once, not looped

    background = _bake_background()

    font_title    = pygame.font.Font(None, 56)
    font_welcome  = pygame.font.Font(None, 24)
    font_ctrl_hdr = pygame.font.Font(None, 22)
    font_ctrl     = pygame.font.Font(None, 19)
    font_hint     = pygame.font.Font(None, 22)

    sprite_surfaces = list(assets.sprites.values())
    current_sprite  = random.choice(sprite_surfaces)
    sprite_timer    = 0.0
    win_score       = WIN_SCORE
    clock           = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        sprite_timer += dt

        if sprite_timer >= 0.75:
            sprite_timer -= 0.75
            current_sprite = random.choice(sprite_surfaces)

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
              font_ctrl, font_hint, current_sprite, win_score)

    return win_score
