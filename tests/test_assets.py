import pathlib
import sys
import pytest
import pygame

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

# Module-level skip guard — skip all tests if assets/sprites/ doesn't exist.
SPRITES_DIR = pathlib.Path(__file__).parent.parent / "assets" / "sprites"
pytestmark = pytest.mark.skipif(
    not SPRITES_DIR.exists(),
    reason="assets/sprites/ not found — run convert_assets.py first",
)

from assets import AssetCache  # noqa: E402 — import after sys.path and guard


@pytest.fixture(autouse=True)
def pygame_init():
    """Initialize pygame (with display and mixer) for every test in this module."""
    import os

    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_mode((1280, 800))
    yield
    pygame.quit()


@pytest.fixture
def cache(pygame_init):
    """Return a fully-loaded AssetCache."""
    return AssetCache()


def test_asset_cache_loads(cache):
    """ENG-03: AssetCache loads sprites and sounds without error."""
    assert len(cache.sprites) > 0, "No sprites loaded"
    assert len(cache.sounds) > 0, "No sounds loaded"


def test_sprites_are_surfaces(cache):
    """ENG-03: Every value in sprites dict is a pygame.Surface."""
    for key, surface in cache.sprites.items():
        assert isinstance(surface, pygame.Surface), (
            f"sprites['{key}'] is {type(surface)}, expected pygame.Surface"
        )


def test_sounds_are_sound_objects(cache):
    """ENG-03: Every value in sounds dict is a pygame.mixer.Sound."""
    for key, sound in cache.sounds.items():
        assert isinstance(sound, pygame.mixer.Sound), (
            f"sounds['{key}'] is {type(sound)}, expected pygame.mixer.Sound"
        )


def test_key_naming_convention(cache):
    """ENG-03: Keys are lowercase filename stems (gevil.png -> 'gevil')."""
    assert "gevil" in cache.sprites, "Expected 'gevil' in sprites (from gevil.png)"
    assert "laser" in cache.sounds, "Expected 'laser' in sounds (from laser.wav)"
    assert "deathcry" in cache.sounds, (
        "Expected 'deathcry' in sounds (from deathcry.wav)"
    )


def test_sprite_size(cache):
    """ENG-03: Sprites are loaded at 128x128 pixels (SPRITE_SIZE)."""
    surface = cache.sprites["gevil"]
    assert surface.get_width() == 128, (
        f"Expected width 128, got {surface.get_width()}"
    )
    assert surface.get_height() == 128, (
        f"Expected height 128, got {surface.get_height()}"
    )
