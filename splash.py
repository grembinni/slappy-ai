import pathlib
import random
import sys

import pygame

from settings import (
    SCREEN_W, SCREEN_H, WIN_SCORE, DISPLAY_SPRITE_SIZE,
    SKY_COLOR, CEILING_COLOR, GROUND_COLOR, CEILING_H, GROUND_Y,
)

_INTRO_PATH  = pathlib.Path(__file__).parent / "assets" / "sounds" / "intro.wav"
_MUSIC_PATH  = pathlib.Path(__file__).parent / "assets" / "sounds" / "canyon.wav"
_MUSIC_DONE  = pygame.USEREVENT + 1   # fired when intro ends → cue canyon loop

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
    "Token Idiot: Airman Carlson",
    "Token Cuban A1C: Airman First Class Magby",
    "",
    "Special Thanks To Hurdle's Mom",
]

# Controls summary — referenced by tests (UI-03)
_CONTROLS = (
    "Superman: Arrows / Num0   |   Goblin: WASD / E"
)

_SUP_CONTROLS = [
    ("Superman's Controls",           True),
    ("UP ARROW   = Up / Restart",     False),
    ("DOWN ARROW  = Down",            False),
    ("LEFT ARROW  = Left",            False),
    ("RIGHT ARROW = Right",           False),
    ("NUM 0       = Shoots",          False),
]

_GOB_CONTROLS = [
    ("Goblin's Controls",    True),
    ("W     = Up / Restart", False),
    ("S     = Down",         False),
    ("A     = Left",         False),
    ("D     = Right",        False),
    ("E     = Shoots",       False),
]


def _bake_background() -> pygame.Surface:
    """Gameplay backdrop: cyan sky, white ceiling strip, green ground."""
    surf = pygame.Surface((SCREEN_W, SCREEN_H))
    surf.fill(SKY_COLOR)
    pygame.draw.rect(surf, CEILING_COLOR, (0, 0, SCREEN_W, CEILING_H))
    pygame.draw.rect(surf, GROUND_COLOR, (0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y))
    return surf


def _draw(screen, background, font_title, font_welcome, font_ctrl_hdr,
          font_ctrl, font_hint, sup_sprite, gob_sprite, win_score):
    screen.blit(background, (0, 0))
    cx = SCREEN_W // 2

    def _blit_center(text, font, y, color=(0, 0, 0), shadow=(180, 180, 180)):
        sh = font.render(text, True, shadow)
        tx = font.render(text, True, color)
        screen.blit(sh, (cx - sh.get_width() // 2 + 2, y + 2))
        screen.blit(tx, (cx - tx.get_width()  // 2,    y))

    def _blit_left(text, font, x, y, color=(0, 0, 0), shadow=(180, 180, 180)):
        sh = font.render(text, True, shadow)
        tx = font.render(text, True, color)
        screen.blit(sh, (x + 2, y + 2))
        screen.blit(tx, (x,     y))

    # ── Title ─────────────────────────────────────────────────────────────────
    _blit_center("Hurdle's Mom Inc. Intl.", font_title, 10)

    # ── Welcome lines (VB6 lblIntro lines 1–2) ────────────────────────────────
    _blit_center("Welcome to the best game ever.", font_welcome, 76)
    _blit_center("They aren't bugs, they're features.", font_welcome, 104)

    # ── Controls — two columns, centered as a pair ────────────────────────────
    # Left col 250px + 60px gap + right col 220px = 530px total → starts at cx-265
    left_x  = cx - 265       # = 375
    right_x = left_x + 310   # = 685  (250 col + 60 gap)
    ctrl_y  = 268
    line_h  = 23

    for i, (text, is_hdr) in enumerate(_SUP_CONTROLS):
        font  = font_ctrl_hdr if is_hdr else font_ctrl
        color = (0, 80, 0) if is_hdr else (0, 0, 0)
        _blit_left(text, font, left_x, ctrl_y + i * line_h, color=color)

    for i, (text, is_hdr) in enumerate(_GOB_CONTROLS):
        font  = font_ctrl_hdr if is_hdr else font_ctrl
        color = (0, 80, 0) if is_hdr else (0, 0, 0)
        _blit_left(text, font, right_x, ctrl_y + i * line_h, color=color)

    # ── Win score selector ────────────────────────────────────────────────────
    _blit_center(f"Win Score: {win_score}  (Up/Down to change)", font_hint, 480)

    # ── Dismiss hint ──────────────────────────────────────────────────────────
    _blit_center("Press any key or click to start", font_hint, 524,
                 color=(60, 60, 60))

    # ── Characters on ground — Superman 30% from left, Goblin 30% from right ──
    ground_y = GROUND_Y - DISPLAY_SPRITE_SIZE
    sup_x = int(SCREEN_W * 0.30) - DISPLAY_SPRITE_SIZE // 2
    gob_x = int(SCREEN_W * 0.70) - DISPLAY_SPRITE_SIZE // 2
    screen.blit(pygame.transform.scale(sup_sprite, (DISPLAY_SPRITE_SIZE, DISPLAY_SPRITE_SIZE)),
                (sup_x, ground_y))
    screen.blit(pygame.transform.scale(gob_sprite, (DISPLAY_SPRITE_SIZE, DISPLAY_SPRITE_SIZE)),
                (gob_x, ground_y))

    pygame.display.flip()


def run_splash(screen: pygame.Surface, assets) -> int:
    """Display the start-game splash and return the selected win score.

    Plays intro.wav once, then loops canyon.wav. Superman and Goblin stand on
    the ground and alternate between idle and intro frames every 750ms.
    Up/Down adjust win score (10–500). Any other key or click starts the game.
    """
    pygame.event.clear([_MUSIC_DONE])            # discard stale events from previous run
    pygame.mixer.music.stop()
    pygame.mixer.music.load(str(_INTRO_PATH))
    pygame.mixer.music.set_endevent(_MUSIC_DONE) # set AFTER stop — stop() can fire end event
    pygame.mixer.music.play(0)                   # intro once; MUSIC_DONE fires when it ends

    background = _bake_background()

    font_title    = pygame.font.Font(None, 56)
    font_welcome  = pygame.font.Font(None, 24)
    font_ctrl_hdr = pygame.font.Font(None, 22)
    font_ctrl     = pygame.font.Font(None, 19)
    font_hint     = pygame.font.Font(None, 22)

    sup_frames  = [assets.sprites['ckent1'], assets.sprites['ckentintro']]
    gob_frames  = [assets.sprites['gevil1'], assets.sprites['gevilintro']]
    frame_idx   = 0
    sprite_timer = 0.0
    win_score    = WIN_SCORE
    clock        = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        sprite_timer += dt

        if sprite_timer >= 0.75:
            sprite_timer -= 0.75
            frame_idx = 1 - frame_idx

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == _MUSIC_DONE:
                pygame.mixer.music.set_endevent()   # clear — canyon loops forever
                pygame.mixer.music.load(str(_MUSIC_PATH))
                pygame.mixer.music.play(-1)
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
              font_ctrl, font_hint, sup_frames[frame_idx], gob_frames[frame_idx], win_score)

    pygame.mixer.music.set_endevent()   # clear before handing off to Game
    return win_score
