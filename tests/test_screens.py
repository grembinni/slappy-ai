import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pathlib
import pytest
import pygame
from unittest.mock import MagicMock, patch
from collections import defaultdict

from sound import SoundManager
from game import Game, GameState
from player import CharState
from settings import SCREEN_W, SCREEN_H, SPRITE_SIZE, WIN_SCORE
import splash


@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def make_sounds():
    return {'laser': MagicMock(), 'deathcry': MagicMock(), 'explode': MagicMock()}


def make_assets(n_sprites=4):
    assets = MagicMock()
    assets.sprites = defaultdict(lambda: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)))
    for i in range(n_sprites):
        assets.sprites[f'sprite{i}'] = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
    assets.sounds = make_sounds()
    return assets


def make_snd():
    return SoundManager(make_sounds())


def make_game(win_score=None):
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    assets = make_assets()
    if win_score is not None:
        return Game(screen, assets, win_score)
    return Game(screen, assets)


# --- SoundManager.pause_game / resume_game (UI-05 audio freeze) ---

def test_pause_game_calls_mixer_pause_when_not_muted():
    """pause_game() pauses mixer and music when not muted."""
    snd = make_snd()
    with patch('pygame.mixer.pause') as mp, patch('pygame.mixer.music') as mm:
        snd.pause_game()
        mp.assert_called_once()
        mm.pause.assert_called_once()


def test_pause_game_no_op_when_muted():
    """pause_game() is a no-op when already muted."""
    snd = make_snd()
    snd._muted = True
    with patch('pygame.mixer.pause') as mp, patch('pygame.mixer.music') as mm:
        snd.pause_game()
        mp.assert_not_called()
        mm.pause.assert_not_called()


def test_resume_game_calls_mixer_unpause_when_not_muted():
    """resume_game() unpauses mixer and music when not muted."""
    snd = make_snd()
    with patch('pygame.mixer.unpause') as mu, patch('pygame.mixer.music') as mm:
        snd.resume_game()
        mu.assert_called_once()
        mm.unpause.assert_called_once()


def test_resume_game_no_op_when_muted():
    """resume_game() is a no-op when muted — preserves mute state across pauses."""
    snd = make_snd()
    snd._muted = True
    with patch('pygame.mixer.unpause') as mu, patch('pygame.mixer.music') as mm:
        snd.resume_game()
        mu.assert_not_called()
        mm.unpause.assert_not_called()


# --- splash.py constants (UI-01, UI-02, UI-03) ---

def test_splash_credits_count():
    """Splash screen has exactly 25 credits lines (UI-01)."""
    assert len(splash._CREDITS) == 25


def test_splash_credits_first_line():
    """First credits line matches VB6 source (UI-01)."""
    assert splash._CREDITS[0] == "President: Senior Airman"


def test_splash_credits_last_line():
    """Last credits line matches VB6 source (UI-01)."""
    assert splash._CREDITS[24] == "Special Thanks To Hurdle's Mom"


def test_splash_controls_text_content():
    """Controls text references both players' key sets (UI-03)."""
    assert "Superman" in splash._CONTROLS
    assert "Goblin" in splash._CONTROLS
    assert "ESDF" in splash._CONTROLS


# --- win_score parameter ---

def test_game_default_win_score():
    """Game.win_score defaults to the WIN_SCORE constant."""
    g = make_game()
    assert g.win_score == WIN_SCORE


def test_game_custom_win_score():
    """Game.win_score can be overridden at construction time."""
    g = make_game(win_score=100)
    assert g.win_score == 100


def test_win_condition_uses_win_score():
    """Win condition triggers GAME_OVER based on self.win_score, not the constant."""
    g = make_game(win_score=10)
    g.players[0].hit_bonus = 10  # score property = hit_bonus when pose_raw == 0
    g.update(0.016)
    assert g.state == GameState.GAME_OVER


# --- PAUSED state (UI-05) ---

def test_paused_state_can_be_set():
    """Game state can be set to PAUSED."""
    g = make_game()
    g.state = GameState.PAUSED
    assert g.state == GameState.PAUSED


def test_paused_state_update_does_not_raise():
    """update() does not crash when called in PAUSED state."""
    g = make_game()
    g.state = GameState.PAUSED
    g.update(0.1)  # run() guards this, but update() itself must be safe
    assert g.state == GameState.PAUSED


def test_game_over_draw_does_not_raise():
    """draw() does not raise when state is GAME_OVER."""
    g = make_game()
    g.state = GameState.GAME_OVER
    g.draw()


def test_paused_draw_does_not_raise():
    """draw() does not raise when state is PAUSED."""
    g = make_game()
    g.state = GameState.PAUSED
    g.draw()


# --- GAME_OVER screen + restart (UI-06, UI-07) ---

def test_run_returns_restart_on_f2():
    """run() returns 'restart' when F2 is pressed in GAME_OVER state."""
    g = make_game()
    g.state = GameState.GAME_OVER
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2, mod=0, unicode=''))
    result = g.run()
    assert result == "restart"


def test_run_returns_restart_on_enter():
    """run() returns 'restart' when Enter is pressed in GAME_OVER state."""
    g = make_game()
    g.state = GameState.GAME_OVER
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode='\r'))
    result = g.run()
    assert result == "restart"


def test_f2_in_playing_does_not_restart():
    """F2 in PLAYING state does not trigger restart."""
    g = make_game()
    assert g.state == GameState.PLAYING
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2, mod=0, unicode=''))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    result = g.run()
    assert result != "restart"


def test_game_over_draw_game_over_method():
    """_draw_game_over() renders without raising (includes OSG=0 branch)."""
    g = make_game()
    g.state = GameState.GAME_OVER
    g.osg_score = 0
    g._draw_game_over()


# --- PyInstaller spec (PKG-01) ---

def test_spec_file_exists():
    """slappy.spec exists in the project root (PKG-01)."""
    spec = pathlib.Path(__file__).parent.parent / "slappy.spec"
    assert spec.exists(), "slappy.spec not found — run 06-04 plan"


def test_spec_includes_sprites_in_datas():
    """slappy.spec declares assets/sprites in datas so the bundle finds sprites."""
    spec = pathlib.Path(__file__).parent.parent / "slappy.spec"
    content = spec.read_text()
    assert "assets/sprites" in content


def test_spec_includes_sounds_in_datas():
    """slappy.spec declares assets/sounds in datas so the bundle finds sounds."""
    spec = pathlib.Path(__file__).parent.parent / "slappy.spec"
    content = spec.read_text()
    assert "assets/sounds" in content
