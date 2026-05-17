import pathlib
import pygame

_MUSIC_DIR = pathlib.Path(__file__).parent / "assets" / "sounds"


class SoundManager:

    def __init__(self, sounds: dict) -> None:
        self._sounds = sounds
        self._muted: bool = False

    def play_laser(self) -> None:
        if self._muted:
            return
        self._sounds['laser'].play()

    def play_death_cry(self) -> None:
        if self._muted:
            return
        self._sounds['deathcry'].play()

    def play_explode(self) -> None:
        if self._muted:
            return
        self._sounds['explode'].play()

    def play_playing_music(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(str(_MUSIC_DIR / "passport.wav"))
        pygame.mixer.music.play(-1)

    def play_splash_music(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(str(_MUSIC_DIR / "canyon.wav"))
        pygame.mixer.music.play(-1)

    def stop_music(self) -> None:
        pygame.mixer.music.stop()

    def toggle_mute(self) -> None:
        self._muted = not self._muted
        if self._muted:
            pygame.mixer.pause()
            pygame.mixer.music.pause()
        else:
            pygame.mixer.unpause()
            pygame.mixer.music.unpause()

    def pause_game(self) -> None:
        if not self._muted:
            pygame.mixer.pause()
            pygame.mixer.music.pause()

    def resume_game(self) -> None:
        if not self._muted:
            pygame.mixer.unpause()
            pygame.mixer.music.unpause()
