import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest
import pygame
from unittest.mock import MagicMock, patch
from collections import defaultdict

from sound import SoundManager
from game import Game, GameState
from settings import SCREEN_W, SCREEN_H, SPRITE_SIZE


@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def make_sounds():
    return {'laser': MagicMock(), 'deathcry': MagicMock(), 'explode': MagicMock()}


def make_snd(sounds=None):
    return SoundManager(sounds or make_sounds())


def make_game():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    assets = MagicMock()
    assets.sprites = defaultdict(lambda: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)))
    assets.sounds = make_sounds()
    return Game(screen, assets)


# AUD-01: Laser SFX
def test_play_laser_calls_sound():
    """play_laser() calls laser.play() when not muted."""
    sounds = make_sounds()
    snd = make_snd(sounds)
    snd.play_laser()
    sounds['laser'].play.assert_called_once()

def test_play_laser_muted_skips_sound():
    """play_laser() does not call laser.play() when muted."""
    sounds = make_sounds()
    snd = make_snd(sounds)
    snd._muted = True
    snd.play_laser()
    sounds['laser'].play.assert_not_called()


# AUD-02: Death Cry SFX
def test_play_death_cry_calls_sound():
    """play_death_cry() calls deathcry.play() when not muted."""
    sounds = make_sounds()
    snd = make_snd(sounds)
    snd.play_death_cry()
    sounds['deathcry'].play.assert_called_once()

def test_play_death_cry_muted_skips_sound():
    """play_death_cry() does not call deathcry.play() when muted."""
    sounds = make_sounds()
    snd = make_snd(sounds)
    snd._muted = True
    snd.play_death_cry()
    sounds['deathcry'].play.assert_not_called()


# AUD-03: Explode SFX
def test_play_explode_calls_sound():
    """play_explode() calls explode.play() when not muted."""
    sounds = make_sounds()
    snd = make_snd(sounds)
    snd.play_explode()
    sounds['explode'].play.assert_called_once()

def test_play_explode_muted_skips_sound():
    """play_explode() does not call explode.play() when muted."""
    sounds = make_sounds()
    snd = make_snd(sounds)
    snd._muted = True
    snd.play_explode()
    sounds['explode'].play.assert_not_called()


# AUD-04: Background Music
def test_play_playing_music_stops_first():
    """play_playing_music() calls music.stop() before loading."""
    snd = make_snd()
    with patch('pygame.mixer.music') as mm:
        snd.play_playing_music()
        mm.stop.assert_called_once()

def test_play_playing_music_loads_passport_and_loops():
    """play_playing_music() loads passport.wav and calls play(-1)."""
    snd = make_snd()
    with patch('pygame.mixer.music') as mm:
        snd.play_playing_music()
        assert mm.load.call_count == 1
        load_arg = str(mm.load.call_args[0][0])
        assert 'passport.wav' in load_arg
        mm.play.assert_called_once_with(-1)


# AUD-05: Intro Music
def test_play_splash_music_stops_first():
    """play_splash_music() calls music.stop() before loading."""
    snd = make_snd()
    with patch('pygame.mixer.music') as mm:
        snd.play_splash_music()
        mm.stop.assert_called_once()

def test_play_splash_music_loads_canyon_and_loops():
    """play_splash_music() loads canyon.wav and calls play(-1)."""
    snd = make_snd()
    with patch('pygame.mixer.music') as mm:
        snd.play_splash_music()
        assert mm.load.call_count == 1
        load_arg = str(mm.load.call_args[0][0])
        assert 'canyon.wav' in load_arg
        mm.play.assert_called_once_with(-1)


# stop_music
def test_stop_music():
    """stop_music() calls pygame.mixer.music.stop()."""
    snd = make_snd()
    with patch('pygame.mixer.music') as mm:
        snd.stop_music()
        mm.stop.assert_called_once()


# AUD-06: Mute Toggle
def test_toggle_mute_sets_muted_flag():
    """toggle_mute() flips _muted from False to True."""
    snd = make_snd()
    assert snd._muted is False
    with patch('pygame.mixer.pause'), patch('pygame.mixer.music'):
        snd.toggle_mute()
    assert snd._muted is True

def test_toggle_mute_mutes_channels_and_music():
    """toggle_mute() (unmuted to muted) calls mixer.pause() and music.pause()."""
    snd = make_snd()
    with patch('pygame.mixer.pause') as mp, patch('pygame.mixer.music') as mm:
        snd.toggle_mute()
        mp.assert_called_once()
        mm.pause.assert_called_once()

def test_toggle_mute_unmutes_channels_and_music():
    """toggle_mute() (muted to unmuted) calls mixer.unpause() and music.unpause()."""
    snd = make_snd()
    snd._muted = True
    with patch('pygame.mixer.unpause') as mu, patch('pygame.mixer.music') as mm:
        snd.toggle_mute()
        mu.assert_called_once()
        mm.unpause.assert_called_once()

def test_toggle_mute_double_toggle_restores_unmuted():
    """Two toggle_mute() calls restore _muted to False."""
    snd = make_snd()
    with patch('pygame.mixer.pause'), patch('pygame.mixer.music'), \
         patch('pygame.mixer.unpause'):
        snd.toggle_mute()
        snd.toggle_mute()
    assert snd._muted is False


# Integration: game.py wiring checks
def test_game_has_sound_manager():
    """Game.__init__ creates self.snd as SoundManager."""
    g = make_game()
    assert hasattr(g, 'snd')
    assert isinstance(g.snd, SoundManager)

def test_game_update_contains_explode_trigger():
    """game.update() source contains CRASHING to DEAD detection and play_explode call."""
    import inspect
    g = make_game()
    src = inspect.getsource(g.update)
    assert 'was_crashing' in src
    assert 'play_explode' in src

def test_game_update_contains_death_cry_trigger():
    """game.update() source contains play_death_cry after collision start_crash."""
    import inspect
    g = make_game()
    src = inspect.getsource(g.update)
    assert 'play_death_cry' in src

def test_game_update_contains_stop_music_on_game_over():
    """game.update() source contains stop_music on GAME_OVER transition."""
    import inspect
    g = make_game()
    src = inspect.getsource(g.update)
    assert 'stop_music' in src

def test_game_run_contains_laser_and_mute_handlers():
    """game.run() source contains play_laser and K_m mute handler."""
    import inspect
    g = make_game()
    src = inspect.getsource(g.run)
    assert 'play_laser' in src
    assert 'K_m' in src
    assert 'toggle_mute' in src
