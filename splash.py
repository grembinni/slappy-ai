import pathlib
import random
import sys

import pygame

from settings import SCREEN_W, SCREEN_H, WIN_SCORE, DISPLAY_SPRITE_SIZE

_MUSIC_PATH = pathlib.Path(__file__).parent / "assets" / "sounds" / "canyon.wav"

_SPLASH_BG = (0, 0, 64)

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

_CONTROLS = (
    "Superman: Arrows / Shift / Ctrl / Enter   |   Goblin: ESDF / R / Space / W"
)


def _draw(screen, font_title, font_sub, font_credits, font_winscore,
          font_controls, sprite, credit_idx, win_score):
    screen.fill(_SPLASH_BG)
    cx = SCREEN_W // 2

    def _blit_centered(text, font, y, color=(255, 255, 255), shadow=(20, 20, 80)):
        shadow_surf = font.render(text, True, shadow)
        text_surf   = font.render(text, True, color)
        screen.blit(shadow_surf, (cx - shadow_surf.get_width() // 2 + 2, y + 2))
        screen.blit(text_surf,   (cx - text_surf.get_width()   // 2,     y))

    # Title with shadow
    _blit_centered("Hurdle's Mom Inc. Intl.", font_title, 25)

    # Subtitle — two centered lines
    _blit_centered("Presents:", font_sub, 110)
    _blit_centered("A Hurdle's Mom Inc. Intl. production", font_sub, 155, color=(200, 200, 200))

    # Character sprite — centered horizontally, below subtitle
    scaled = pygame.transform.scale(sprite, (DISPLAY_SPRITE_SIZE, DISPLAY_SPRITE_SIZE))
    sprite_y = 210 + (350 - DISPLAY_SPRITE_SIZE) // 2
    screen.blit(scaled, (cx - DISPLAY_SPRITE_SIZE // 2, sprite_y))

    # Credits line (discrete: one line shown for 1500ms)
    line = _CREDITS[credit_idx]
    if line:
        _blit_centered(line, font_credits, 590, color=(255, 255, 100))

    # Win score selector
    _blit_centered(f"Win Score: {win_score}  (Up/Down to change)", font_winscore, 650)

    # Controls reference
    _blit_centered(_CONTROLS, font_controls, 720, color=(180, 180, 180))

    pygame.display.flip()


def run_splash(screen: pygame.Surface, assets) -> int:
    """Display the splash screen and return the selected win score.

    Up/Down adjust the win score in steps of 10 (range 10–500).
    Any other key or mouse click dismisses the splash and starts the game.
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load(str(_MUSIC_PATH))
    pygame.mixer.music.play(0)

    font_title    = pygame.font.Font(None, 72)
    font_sub      = pygame.font.Font(None, 36)
    font_credits  = pygame.font.Font(None, 28)
    font_winscore = pygame.font.Font(None, 28)
    font_controls = pygame.font.Font(None, 22)

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

        _draw(screen, font_title, font_sub, font_credits, font_winscore,
              font_controls, current_sprite, credit_idx, win_score)

    return win_score
