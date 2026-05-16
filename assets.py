import pathlib
import pygame
from settings import SPRITE_SIZE  # noqa: F401 — 128px; actual size determined by PNG files

ASSETS_DIR = pathlib.Path(__file__).parent / "assets"


class AssetCache:
    """Loads and caches all game assets at startup.

    Sprites are 128x128 RGBA PNGs (SPRITE_SIZE x SPRITE_SIZE).
    Sounds are WAV files compatible with pygame.mixer.

    pygame.mixer must be initialized before instantiating AssetCache.
    """

    def __init__(self):
        if not ASSETS_DIR.exists():
            raise FileNotFoundError(
                "assets/ not found — run: python convert_assets.py"
            )
        self.sprites: dict = {}
        self.sounds: dict = {}
        self._load_sprites()
        self._load_sounds()

    def _load_sprites(self):
        sprites_dir = ASSETS_DIR / "sprites"
        for png in sorted(sprites_dir.glob("*.png")):
            key = png.stem.lower()
            self.sprites[key] = pygame.image.load(str(png)).convert_alpha()

    def _load_sounds(self):
        sounds_dir = ASSETS_DIR / "sounds"
        for wav in sorted(sounds_dir.glob("*.wav")):
            key = wav.stem.lower()
            self.sounds[key] = pygame.mixer.Sound(str(wav))
