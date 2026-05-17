import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest
import pygame
from unittest.mock import MagicMock
from collections import defaultdict, deque
import settings
from beam import Beam
from player import Player, CharState
from settings import (
    BEAM_LENGTH, BEAM_WIDTH, BEAM_SPEED, SCREEN_W,
    DIR_LEFT, DIR_RIGHT,
    SUPERMAN_BEAM_COLOR, GOBLIN_BEAM_COLOR,
    DISPLAY_SPRITE_SIZE, SPRITE_SIZE,
)


@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    pygame.display.set_mode((1280, 800))
    yield
    pygame.quit()


def make_assets():
    assets = MagicMock()
    assets.sprites = defaultdict(lambda: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)))
    return assets


# ---------------------------------------------------------------------------
# 1. test_beam_construction_left
# ---------------------------------------------------------------------------

def test_beam_construction_left():
    # CMB-04
    b = Beam(100.0, 200.0, DIR_LEFT, SUPERMAN_BEAM_COLOR)
    assert b.x == 100.0
    assert b.y == 200.0
    assert b.direction == DIR_LEFT
    assert b.color == SUPERMAN_BEAM_COLOR
    assert b.distance_traveled == 0.0


# ---------------------------------------------------------------------------
# 2. test_beam_construction_right
# ---------------------------------------------------------------------------

def test_beam_construction_right():
    # CMB-04
    b = Beam(500.0, 300.0, DIR_RIGHT, GOBLIN_BEAM_COLOR)
    assert b.direction == DIR_RIGHT
    assert b.color == GOBLIN_BEAM_COLOR


# ---------------------------------------------------------------------------
# 3. test_beam_endpoints_left
# ---------------------------------------------------------------------------

def test_beam_endpoints_left():
    # For DIR_LEFT: start=(x,y), end=(x+BEAM_LENGTH,y)
    # CMB-07: endpoints used by clipline()
    b = Beam(100.0, 200.0, DIR_LEFT, SUPERMAN_BEAM_COLOR)
    assert b.start == (100, 200)
    assert b.end == (100 + BEAM_LENGTH, 200)


# ---------------------------------------------------------------------------
# 4. test_beam_endpoints_right
# ---------------------------------------------------------------------------

def test_beam_endpoints_right():
    # For DIR_RIGHT: start=(x-BEAM_LENGTH,y), end=(x,y)
    # CMB-07
    b = Beam(300.0, 200.0, DIR_RIGHT, GOBLIN_BEAM_COLOR)
    assert b.start == (300 - BEAM_LENGTH, 200)
    assert b.end == (300, 200)


# ---------------------------------------------------------------------------
# 5. test_beam_moves_left
# ---------------------------------------------------------------------------

def test_beam_moves_left():
    # CMB-03, dt-scaling
    b = Beam(400.0, 200.0, DIR_LEFT, SUPERMAN_BEAM_COLOR)
    alive = b.update(0.1)
    assert alive, "Beam should still be alive"
    expected_x = 400.0 - BEAM_SPEED * 0.1
    assert b.x == pytest.approx(expected_x), f"Expected {expected_x}, got {b.x}"


# ---------------------------------------------------------------------------
# 6. test_beam_moves_right
# ---------------------------------------------------------------------------

def test_beam_moves_right():
    # CMB-03
    b = Beam(400.0, 200.0, DIR_RIGHT, GOBLIN_BEAM_COLOR)
    b.update(0.1)
    expected_x = 400.0 + BEAM_SPEED * 0.1
    assert b.x == pytest.approx(expected_x)


# ---------------------------------------------------------------------------
# 7. test_beam_wrap_left_edge
# ---------------------------------------------------------------------------

def test_beam_wrap_left_edge():
    # Leftward beam wrapping: x < -BEAM_LENGTH → x = SCREEN_W
    # CMB-06
    b = Beam(-BEAM_LENGTH - 1.0, 200.0, DIR_LEFT, SUPERMAN_BEAM_COLOR)
    b.update(0.001)   # tiny dt — just enough to trigger wrap check
    assert b.x == pytest.approx(float(SCREEN_W)), f"Expected SCREEN_W wrap, got {b.x}"


# ---------------------------------------------------------------------------
# 8. test_beam_wrap_right_edge
# ---------------------------------------------------------------------------

def test_beam_wrap_right_edge():
    # Rightward beam wrapping: x > SCREEN_W → x = -BEAM_LENGTH
    # CMB-06
    b = Beam(float(SCREEN_W + 1), 200.0, DIR_RIGHT, GOBLIN_BEAM_COLOR)
    b.update(0.001)
    assert b.x == pytest.approx(float(-BEAM_LENGTH)), f"Expected -BEAM_LENGTH wrap, got {b.x}"


# ---------------------------------------------------------------------------
# 9. test_beam_expiry_after_two_wraps
# ---------------------------------------------------------------------------

def test_beam_expiry_after_two_wraps():
    # Beam expires when distance_traveled >= SCREEN_W (one full traversal)
    # CMB-06
    b = Beam(0.0, 200.0, DIR_LEFT, SUPERMAN_BEAM_COLOR)
    b.distance_traveled = SCREEN_W - 1.0
    alive = b.update(0.016)   # pushes past threshold
    assert not alive, "Beam should expire after one full screen width"


# ---------------------------------------------------------------------------
# 10. test_beam_alive_before_two_wraps
# ---------------------------------------------------------------------------

def test_beam_alive_before_two_wraps():
    # CMB-06
    b = Beam(0.0, 200.0, DIR_LEFT, SUPERMAN_BEAM_COLOR)
    b.distance_traveled = SCREEN_W - 100.0   # just under expiry
    alive = b.update(0.016)   # still under threshold
    assert alive, "Beam should still be alive"


# ---------------------------------------------------------------------------
# 11. test_player_beams_deque_exists
# ---------------------------------------------------------------------------

def test_player_beams_deque_exists():
    # CMB-05
    p = Player("superman", make_assets())
    assert hasattr(p, "beams")
    assert isinstance(p.beams, deque)
    assert p.beams.maxlen == 10


# ---------------------------------------------------------------------------
# 12. test_player_fire_creates_beam
# ---------------------------------------------------------------------------

def test_player_fire_creates_beam():
    # CMB-01, CMB-04, CMB-05
    p = Player("superman", make_assets())
    p.fire(DIR_LEFT)
    assert len(p.beams) == 1
    b = p.beams[0]
    assert b.direction == DIR_LEFT
    assert b.color == SUPERMAN_BEAM_COLOR


# ---------------------------------------------------------------------------
# 13. test_player_fire_deque_maxlen_ring_buffer
# ---------------------------------------------------------------------------

def test_player_fire_deque_maxlen_ring_buffer():
    # After 11 fires, deque still holds only 10 beams (oldest evicted)
    # CMB-05
    p = Player("superman", make_assets())
    for _ in range(11):
        p.fire(DIR_LEFT)
    assert len(p.beams) == 10, f"Expected 10 beams, got {len(p.beams)}"


# ---------------------------------------------------------------------------
# 14. test_beam_collision_via_clipline
# ---------------------------------------------------------------------------

def test_beam_collision_via_clipline():
    # Verify beam.start/end works with pygame.Rect.clipline() for collision detection
    # This tests the primitive used by game.py — game.py itself is not imported.
    # CMB-07
    sup = Player("superman", make_assets())
    gob = Player("goblin", make_assets())
    # Position goblin rect at a known location
    gob.x = 600.0
    gob.y = 300.0
    # Fire a rightward beam from superman aimed to intersect goblin's rect
    # Goblin rect spans x=600..708 (DISPLAY_SPRITE_SIZE=108), y=300..408
    beam = Beam(620.0, 354.0, DIR_RIGHT, SUPERMAN_BEAM_COLOR)   # leading edge inside rect
    result = gob.rect.clipline(beam.start, beam.end)
    assert result, "Beam intersecting opponent rect should return non-empty clipline result"
    # Miss test — beam far above goblin
    beam_miss = Beam(620.0, 100.0, DIR_RIGHT, SUPERMAN_BEAM_COLOR)
    miss_result = gob.rect.clipline(beam_miss.start, beam_miss.end)
    assert not miss_result, "Beam missing opponent rect should return empty clipline result"


# ---------------------------------------------------------------------------
# 15. test_beam_direction_guard
# ---------------------------------------------------------------------------

def test_beam_direction_guard():
    # The VB6 Or-bug fix: beam.direction in (DIR_LEFT, DIR_RIGHT) must evaluate correctly.
    # CMB-08: verify the correct pattern works and the buggy pattern would fail.
    beam_left = Beam(100.0, 200.0, DIR_LEFT, SUPERMAN_BEAM_COLOR)
    beam_right = Beam(200.0, 200.0, DIR_RIGHT, GOBLIN_BEAM_COLOR)
    # Correct pattern — both must be truthy
    assert beam_left.direction in (DIR_LEFT, DIR_RIGHT), "DIR_LEFT should match"
    assert beam_right.direction in (DIR_RIGHT, DIR_LEFT), "DIR_RIGHT should match"
    # Demonstrate why the buggy pattern is dangerous:
    # `beam.direction == DIR_LEFT or DIR_RIGHT` always evaluates True for any beam
    # because `or DIR_RIGHT` evaluates the *int* DIR_RIGHT (=4) as a standalone truthy value.
    # The correct pattern uses `in` which checks membership explicitly.
    buggy_result_for_some_other_direction = (5 == DIR_LEFT or DIR_RIGHT)
    assert buggy_result_for_some_other_direction, (
        "Demonstrates VB6 Or-bug: 'x == LEFT or RIGHT' is always True when RIGHT is truthy"
    )
    # CMB-08: enforce that game.py uses the correct pattern (checked via source grep)
    import re
    src = open("game.py").read()
    assert "beam.direction in (DIR_LEFT, DIR_RIGHT)" in src, (
        "game.py must contain: beam.direction in (DIR_LEFT, DIR_RIGHT)"
    )
