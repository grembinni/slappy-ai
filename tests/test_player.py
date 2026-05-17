import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest
import pygame
from unittest.mock import MagicMock
from collections import defaultdict
from enum import Enum
import settings
from player import Player, CharState
from settings import (
    SCREEN_W, SCREEN_H, SPRITE_SIZE, DISPLAY_SPRITE_SIZE,
    CEILING_H, GROUND_Y, CEILING_STOP_Y, GROUND_STOP_Y,
    PLAYER_SPEED_H, PLAYER_SPEED_UP, PLAYER_SPEED_DOWN, ANIM_INTERVAL,
    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_IDLE,
)


@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def make_assets():
    """MagicMock AssetCache — all sprite keys return a 128x128 Surface."""
    assets = MagicMock()
    assets.sprites = defaultdict(lambda: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)))
    return assets


def make_keys(*keys_down):
    """Simulate pygame.key.get_pressed() — returns defaultdict(bool) with given key constants True."""
    d = defaultdict(bool)
    for k in keys_down:
        d[k] = True
    return d


# ---------------------------------------------------------------------------
# 1. CharState enum
# ---------------------------------------------------------------------------

def test_charstate_enum():
    # MOV-07
    assert issubclass(CharState, Enum)
    for name in ("ALIVE", "CRASHING", "DEAD"):
        assert hasattr(CharState, name), f"CharState missing {name}"


# ---------------------------------------------------------------------------
# 2–3. Initial state
# ---------------------------------------------------------------------------

def test_player_initial_state_superman():
    # MOV-07
    p = Player("superman", make_assets())
    assert p.state == CharState.ALIVE
    assert p.x == pytest.approx(SCREEN_W * 0.75)
    assert p.y == SCREEN_H // 2


def test_player_initial_state_goblin():
    # MOV-07
    p = Player("goblin", make_assets())
    assert p.state == CharState.ALIVE
    assert p.x == pytest.approx(SCREEN_W * 0.25)
    assert p.y == SCREEN_H // 2


# ---------------------------------------------------------------------------
# 4–8. Basic movement — dt-scaled
# ---------------------------------------------------------------------------

def test_superman_moves_right():
    # MOV-01, MOV-03
    p = Player("superman", make_assets())
    orig_x = p.x
    p.update(0.1, make_keys(pygame.K_RIGHT))
    assert p.x == pytest.approx(orig_x + PLAYER_SPEED_H * 0.1)


def test_superman_moves_left():
    # MOV-01, MOV-03
    p = Player("superman", make_assets())
    orig_x = p.x
    p.update(0.1, make_keys(pygame.K_LEFT))
    assert p.x == pytest.approx(orig_x - PLAYER_SPEED_H * 0.1)


def test_superman_moves_up():
    # MOV-01, MOV-03
    p = Player("superman", make_assets())
    orig_y = p.y
    p.update(0.1, make_keys(pygame.K_UP))
    assert p.y == pytest.approx(orig_y - PLAYER_SPEED_UP * 0.1)


def test_superman_moves_down():
    # MOV-01, MOV-03
    # Character must be in air (not at GROUND_Y) for down key to work
    p = Player("superman", make_assets())
    p.y = float(SCREEN_H // 2)   # midscreen — in air
    orig_y = p.y
    p.update(0.1, make_keys(pygame.K_DOWN))
    assert p.y > orig_y
    assert p.y == pytest.approx(orig_y + PLAYER_SPEED_DOWN * 0.1)


def test_goblin_moves_right():
    # MOV-02, MOV-03
    p = Player("goblin", make_assets())
    orig_x = p.x
    p.update(0.1, make_keys(pygame.K_d))
    assert p.x == pytest.approx(orig_x + PLAYER_SPEED_H * 0.1)


# ---------------------------------------------------------------------------
# 9–10. Boundary clamping
# ---------------------------------------------------------------------------

def test_ceiling_clamp():
    # MOV-06
    p = Player("superman", make_assets())
    p.y = float(CEILING_H + 1)   # just above ceiling — pressing up should be clamped
    p.update(0.5, make_keys(pygame.K_UP))
    assert p.y >= CEILING_STOP_Y, f"y={p.y} should be >= CEILING_STOP_Y={CEILING_STOP_Y}"


def test_ground_clamp():
    # MOV-05
    p = Player("superman", make_assets())
    p.y = float(SCREEN_H)   # below ground boundary
    p.update(0.016, make_keys())
    assert p.y <= GROUND_STOP_Y, f"y={p.y} should be <= GROUND_STOP_Y={GROUND_STOP_Y}"


# ---------------------------------------------------------------------------
# 11–12. Horizontal wrap
# ---------------------------------------------------------------------------

def test_horizontal_wrap_right():
    # MOV-04
    p = Player("superman", make_assets())
    p.x = float(SCREEN_W + 10)
    p.update(0.016, make_keys(pygame.K_RIGHT))
    assert p.x < SCREEN_W, f"Expected wrap, got x={p.x}"


def test_horizontal_wrap_left():
    # MOV-04
    p = Player("superman", make_assets())
    p.x = float(-DISPLAY_SPRITE_SIZE - 10)
    p.update(0.016, make_keys(pygame.K_LEFT))
    assert p.x >= 0, f"Expected wrap to right side, got x={p.x}"


# ---------------------------------------------------------------------------
# 13. rect property
# ---------------------------------------------------------------------------

def test_rect_property():
    # Phase 3 collision prerequisite
    p = Player("superman", make_assets())
    r = p.rect
    assert isinstance(r, pygame.Rect)
    assert r.x == int(p.x)
    assert r.y == int(p.y)
    assert r.width == DISPLAY_SPRITE_SIZE
    assert r.height == DISPLAY_SPRITE_SIZE


# ---------------------------------------------------------------------------
# 14. Animation frame toggle
# ---------------------------------------------------------------------------

def test_animation_frame_toggles():
    # MOV-08
    p = Player("superman", make_assets())
    p._anim_frame = 0
    p._anim_timer = ANIM_INTERVAL - 0.001
    p.update(0.002, make_keys())   # push timer over threshold
    assert p._anim_frame == 1, "Expected frame to toggle from 0 to 1"


# ---------------------------------------------------------------------------
# 15–17. Sprite key selection
# ---------------------------------------------------------------------------

def test_get_sprite_key_idle_air():
    # MOV-09 — fresh superman is in air at SCREEN_H//2 (well above GROUND_Y=750)
    p = Player("superman", make_assets())
    p._direction = DIR_IDLE
    p._on_ground = False
    p._anim_frame = 0
    key = p._get_sprite_key()
    assert key == "superman", f"Expected 'superman', got '{key}'"


def test_get_sprite_key_ground_idle():
    # MOV-09
    p = Player("superman", make_assets())
    p._on_ground = True
    p._moving_h = False
    key = p._get_sprite_key()
    assert key == "ckent", f"Expected 'ckent', got '{key}'"


def test_get_sprite_key_ground_walk():
    # MOV-08, MOV-09, D-10 — _GROUND_WALK_CYCLE = [0, 1, 0, 2]
    p = Player("superman", make_assets())
    p._on_ground = True
    p._moving_h = True

    p._ground_walk_step = 0   # GROUND_WALK_CYCLE[0] = 0 -> "ckent1"
    key = p._get_sprite_key()
    assert key == "ckent1", f"Expected 'ckent1', got '{key}'"

    p._ground_walk_step = 1   # GROUND_WALK_CYCLE[1] = 1 -> "ckent2"
    key = p._get_sprite_key()
    assert key == "ckent2", f"Expected 'ckent2', got '{key}'"

    p._ground_walk_step = 3   # GROUND_WALK_CYCLE[3] = 2 -> "ckent3"
    key = p._get_sprite_key()
    assert key == "ckent3", f"Expected 'ckent3', got '{key}'"


# ---------------------------------------------------------------------------
# 18. Down key suppressed on ground
# ---------------------------------------------------------------------------

def test_no_downward_movement_on_ground():
    # MOV-05, D-11
    p = Player("superman", make_assets())
    p.y = float(GROUND_STOP_Y)   # at ground stop position
    p.update(0.1, make_keys(pygame.K_DOWN))
    assert p.y == GROUND_STOP_Y, f"Down key should be suppressed on ground, got y={p.y}"


# ---------------------------------------------------------------------------
# 19. dt proportional scaling
# ---------------------------------------------------------------------------

def test_dt_scaling():
    # MOV-03, CLAUDE.md dt constraint — movement distance proportional to dt
    p1 = Player("superman", make_assets())
    p1.update(0.1, make_keys(pygame.K_RIGHT))
    dist1 = p1.x - (SCREEN_W * 0.75)

    p2 = Player("superman", make_assets())
    p2.update(0.05, make_keys(pygame.K_RIGHT))
    dist2 = p2.x - (SCREEN_W * 0.75)

    assert dist1 == pytest.approx(dist2 * 2, rel=1e-5), (
        f"dt scaling broken: 0.1s gave {dist1}px, 0.05s gave {dist2}px (expected 2x ratio)"
    )


# ---------------------------------------------------------------------------
# 20. Both players move independently
# ---------------------------------------------------------------------------

def test_both_players_move_independently():
    # MOV-01, MOV-02 — shared keyboard, independent movement
    sup = Player("superman", make_assets())
    gob = Player("goblin", make_assets())
    sup_orig_x = sup.x
    gob_orig_x = gob.x

    # Press both right keys simultaneously
    keys = make_keys(pygame.K_RIGHT, pygame.K_d)
    sup.update(0.1, keys)
    gob.update(0.1, keys)

    assert sup.x > sup_orig_x, "Superman should have moved right"
    assert gob.x > gob_orig_x, "Goblin should have moved right"
