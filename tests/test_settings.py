import pathlib
import sys
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import settings


def test_fps_constant():
    assert settings.FPS == 60
    assert isinstance(settings.FPS, int)
    assert 0 < settings.FPS <= 120


def test_gamestate_enum():
    from game import GameState
    assert GameState.SPLASH
    assert GameState.PLAYING
    assert GameState.PAUSED
    assert GameState.GAME_OVER


def test_constants():
    assert settings.SCREEN_W == 1280
    assert settings.SCREEN_H == 800
    assert settings.SPRITE_SIZE == 128
    assert settings.WIN_SCORE == 50
    assert settings.BEAM_SPEED == 800
    assert settings.FPS == 60


def test_zone_constants():
    assert settings.CEILING_H == 50
    assert settings.GROUND_Y == 750
    assert settings.GROUND_Y + (settings.SCREEN_H - settings.GROUND_Y) == settings.SCREEN_H


def test_colors():
    assert settings.SKY_COLOR[0] == 0
    assert settings.SKY_COLOR[1] == 255
    assert settings.SKY_COLOR[2] == 255
    assert settings.CEILING_COLOR == (255, 255, 255)
    assert settings.GROUND_COLOR == (0, 128, 0)


def test_direction_constants():
    assert settings.DIR_UP == 1
    assert settings.DIR_DOWN == 2
    assert settings.DIR_LEFT == 3
    assert settings.DIR_RIGHT == 4
    assert settings.DIR_POSE == 5
    assert settings.DIR_IDLE == 6


def test_beam_colors():
    assert settings.GOBLIN_BEAM_COLOR == (0, 200, 0)
    assert settings.SUPERMAN_BEAM_COLOR == (200, 0, 0)
