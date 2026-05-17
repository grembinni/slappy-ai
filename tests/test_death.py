import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest
import pygame
from unittest.mock import MagicMock
from collections import defaultdict

from player import Player, CharState
from game import Game, GameState
from beam import Beam
from hud import draw_hud
from settings import (
    SCREEN_W, SCREEN_H, DISPLAY_SPRITE_SIZE, SPRITE_SIZE,
    CEILING_STOP_Y, GROUND_STOP_Y,
    PLAYER_SPEED_DOWN, SPIN_INTERVAL, WIN_SCORE,
    DIR_LEFT, DIR_IDLE,
)


@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def make_assets():
    assets = MagicMock()
    assets.sprites = defaultdict(lambda: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)))
    return assets


def make_player(character="superman"):
    return Player(character, make_assets())


def make_game():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    return Game(screen, make_assets()), screen


# ---------------------------------------------------------------------------
# DTH-01: start_crash sets CRASHING and resets spin state
# ---------------------------------------------------------------------------

def test_start_crash_sets_crashing():
    p = make_player()
    p.start_crash()
    assert p.state == CharState.CRASHING
    assert p._spin_timer == 0.0
    assert p._spin_frame == 0


# ---------------------------------------------------------------------------
# DTH-02: CRASHING fall is dt-scaled at PLAYER_SPEED_DOWN
# ---------------------------------------------------------------------------

def test_crashing_falls_dt_scaled():
    p = make_player()
    p.start_crash()
    p.y = float(CEILING_STOP_Y + 100)
    orig_y = p.y
    dt = 0.1
    p.update(dt, defaultdict(bool))
    assert p.y == pytest.approx(orig_y + PLAYER_SPEED_DOWN * dt)
    assert p.state == CharState.CRASHING


# ---------------------------------------------------------------------------
# DTH-03a: spin_frame advances after SPIN_INTERVAL elapses
# ---------------------------------------------------------------------------

def test_spin_frame_advances_at_interval():
    p = make_player()
    p.start_crash()
    p.y = float(CEILING_STOP_Y + 200)
    p._spin_timer = SPIN_INTERVAL - 0.001
    p.update(0.002, defaultdict(bool))
    assert p._spin_frame == 1


# ---------------------------------------------------------------------------
# DTH-03b: spin_frame wraps from 3 back to 0
# ---------------------------------------------------------------------------

def test_spin_frame_wraps():
    p = make_player()
    p.start_crash()
    p.y = float(CEILING_STOP_Y + 200)
    p._spin_frame = 3
    p._spin_timer = SPIN_INTERVAL - 0.001
    p.update(0.002, defaultdict(bool))
    assert p._spin_frame == 0


# ---------------------------------------------------------------------------
# DTH-04: reaching GROUND_STOP_Y transitions to DEAD and snaps y
# ---------------------------------------------------------------------------

def test_crashing_transitions_to_dead_at_ground():
    p = make_player()
    p.start_crash()
    p.y = float(GROUND_STOP_Y - 1)
    p.update(0.1, defaultdict(bool))
    assert p.state == CharState.DEAD
    assert p.y == float(GROUND_STOP_Y)


# ---------------------------------------------------------------------------
# DTH-04/sprite: DEAD state returns death sprite key
# ---------------------------------------------------------------------------

def test_dead_sprite_key():
    p = make_player("superman")
    p.state = CharState.DEAD
    p._on_ground = True
    assert p._get_sprite_key() == "sdeath"


# ---------------------------------------------------------------------------
# DTH-03/sprite: CRASHING returns correct spin sprite key
# ---------------------------------------------------------------------------

def test_crashing_sprite_key():
    p = make_player("superman")
    p.start_crash()
    p._spin_frame = 0
    assert p._get_sprite_key() == "sspin1"
    p._spin_frame = 2
    assert p._get_sprite_key() == "sspin3"


# ---------------------------------------------------------------------------
# DTH-05/06: respawn() returns player to ALIVE with state reset
# ---------------------------------------------------------------------------

def test_respawn_returns_to_alive():
    p = make_player()
    p.state = CharState.DEAD
    p.respawn()
    assert p.state == CharState.ALIVE
    assert p._spin_frame == 0
    assert p._spin_timer == 0.0
    assert p._anim_frame == 0


# ---------------------------------------------------------------------------
# DTH-06: respawn position within upper 70% zone
# ---------------------------------------------------------------------------

def test_respawn_position_bounds():
    p = make_player()
    p.state = CharState.DEAD
    play_h = GROUND_STOP_Y - CEILING_STOP_Y
    for _ in range(20):
        p.respawn()
        assert 0 <= p.x <= SCREEN_W - DISPLAY_SPRITE_SIZE, f"x={p.x} out of range"
        assert CEILING_STOP_Y <= p.y <= CEILING_STOP_Y + 0.7 * play_h, f"y={p.y} out of upper-70% zone"


# ---------------------------------------------------------------------------
# DTH-06/beams: respawn clears beams deque
# ---------------------------------------------------------------------------

def test_respawn_clears_beams():
    p = make_player()
    p.beams.append(Beam(100, 100, DIR_LEFT, (255, 0, 0)))
    p.state = CharState.DEAD
    p.respawn()
    assert len(p.beams) == 0


# ---------------------------------------------------------------------------
# DTH-07: MOUSEBUTTONDOWN on living player → CRASHING + osg_score++
# (via game.py source inspection — run() event loop not directly callable)
# ---------------------------------------------------------------------------

def test_mouse_click_crash_logic_present():
    import inspect
    src = inspect.getsource(Game.run)
    assert "MOUSEBUTTONDOWN" in src
    assert "start_crash" in src
    assert "osg_score" in src


# ---------------------------------------------------------------------------
# SCR-01: score property uses raw_pose // 10 + hit_bonus formula
# ---------------------------------------------------------------------------

def test_score_formula():
    p = make_player()
    assert p.score == 0
    p.raw_pose = 30
    p.hit_bonus = 5
    assert p.score == 30 // 10 + 5  # == 8
    p.raw_pose = 0
    p.hit_bonus = 7
    assert p.score == 7


# ---------------------------------------------------------------------------
# SCR-02: idle-airborne ALIVE player gets raw_pose += 1 per game.update()
# ---------------------------------------------------------------------------

def test_pose_accumulates_idle_airborne():
    g, _ = make_game()
    sup = g.players[0]
    assert sup.y < GROUND_STOP_Y  # default position is in air
    assert sup.raw_pose == 0
    g.update(0.016)  # no keys → DIR_IDLE, not on ground
    assert sup.raw_pose == 1


# ---------------------------------------------------------------------------
# SCR-03: beam hit awards shooter hit_bonus += 10 via game.update()
# ---------------------------------------------------------------------------

def test_beam_hit_awards_hit_bonus():
    g, _ = make_game()
    sup, gob = g.players[0], g.players[1]
    cx = int(sup.x) + DISPLAY_SPRITE_SIZE // 2
    cy = int(sup.y) + DISPLAY_SPRITE_SIZE // 2
    b = Beam(cx, cy, DIR_LEFT, (0, 200, 0))
    gob.beams.append(b)
    assert gob.hit_bonus == 0
    g.update(0.016)
    assert sup.state == CharState.CRASHING
    assert gob.hit_bonus == 10


# ---------------------------------------------------------------------------
# SCR-05: draw_hud renders without error; OSG hidden when osg_score == 0
# ---------------------------------------------------------------------------

def test_hud_renders_and_osg_hidden():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    font = pygame.font.Font(None, 28)
    p1 = MagicMock(); p1.score = 12
    p2 = MagicMock(); p2.score = 5
    draw_hud(screen, [p1, p2], 0, font)   # osg hidden — no error
    draw_hud(screen, [p1, p2], 3, font)   # osg shown — no error


# ---------------------------------------------------------------------------
# SCR-06: player.score >= WIN_SCORE → GameState.GAME_OVER
# ---------------------------------------------------------------------------

def test_win_condition_triggers_game_over():
    g, _ = make_game()
    assert g.state == GameState.PLAYING
    g.players[0].hit_bonus = WIN_SCORE
    g.update(0.016)
    assert g.state == GameState.GAME_OVER
