# Research Summary — Goblin vs. Superman Python Port

**Project:** Goblin vs. Superman (Python/pygame port)
**Domain:** VB6 → Python/pygame 2-player local multiplayer arcade brawler
**Researched:** 2026-05-16
**Confidence:** HIGH (architecture derived from direct VB6 source reading; stack from established pygame community consensus)

---

## Executive Summary

This is a faithful port of a ~1,400-line VB6 brawler to Python/pygame-ce. The original game has two forms (credits/intro + gameplay), a timer-driven game loop, two player-controlled characters, axis-aligned laser beams, and MIDI background music. The correct approach is a flat 7-file Python module layout — approximately 700 lines of clean Python replacing the VB6 spaghetti — driven by a single `pygame.time.Clock`-based game loop at 60 FPS with a `GameState` enum controlling active subsystems. No third-party game framework beyond pygame-ce is needed or appropriate.

The recommended stack is Python 3.11 + pygame-ce 2.5.x. Asset conversion (ICO→PNG via Pillow, MIDI→WAV via FluidSynth) is a one-time build-time step — the only runtime dependency is pygame-ce. PyInstaller 6.x handles Windows packaging.

The top risks are not new feature complexity — they are subtle translation traps: the VB6 `Or 4` collision bug survives verbatim in Python syntax, twip-to-pixel numeric values look plausible but are off by 15x, and the VB6 timer architecture tempts developers to replicate it with `pygame.time.set_timer` when a single `clock.tick(60)` loop is the correct replacement.

---

## Recommended Stack

- **Python 3.11** — best PyInstaller 6.x compatibility; avoid 3.12+ edge cases
- **pygame-ce 2.5.x** — actively maintained fork of pygame, identical API, better Python 3.11+ support; no reason to use original pygame for new projects
- **Pillow 10.x** — dev-time ICO→PNG conversion; use `Image.NEAREST` resampling to preserve pixel art edges
- **FluidSynth 2.3.x + GeneralUser GS sf2** — dev-time MIDI→WAV at 44100 Hz to match pygame mixer default
- **PyInstaller 6.x** — Windows packaging with `--onedir --windowed`; bundles SDL2 DLLs automatically
- **pytest 7.x** — unit testing game logic (collision, scoring, state machine) without a display

**Do not use:** original pygame, arcade/pyglet (OpenGL overhead), `pygame.time.set_timer` to replicate VB6 timers, `Image.LANCZOS` for upscaling (blurs pixel art), `pygame.midi` at runtime (unreliable on Windows 11).

---

## Table Stakes Features

**Must have:**
- Delta-time frame capping (`clock.tick(60)`) — game speed varies by machine without it
- `GameState` enum (SPLASH, PLAYING, PAUSED, GAME_OVER) — structural foundation; absent leads to boolean-flag spaghetti
- In-game HUD score display — window title scores are invisible during play
- Splash/credits screen — explicitly required by PROJECT.md
- Pause state (P or Escape)
- GAME_OVER screen with restart prompt
- Sound mute toggle (M key)
- Graceful quit handling via `pygame.QUIT` event

**Should have:**
- Win condition constant (`WIN_SCORE`, off by default at 0)
- Hit flash on death (1-2 frame white overlay)
- Upscaled sprites with nearest-neighbor

**Anti-features (do not add):** settings screen, key rebinding, fullscreen toggle, online multiplayer, AI opponent, persistent high scores, new characters or modes.

---

## Architecture Approach

A flat 7-file module layout driven by a single `pygame.time.Clock` game loop. The VB6's five separate timers all collapse into one 60 Hz loop with delta-time-scaled movement and internal frame counters. Do not use `pygame.sprite.Sprite` / `Group` — plain classes with `update(dt)` / `draw(screen)` are simpler and don't fight the manual frame-selection logic.

**Components:**
1. `main.py` — bootstrap pygame, create Game, call `game.run()`
2. `game.py` — main loop, `GameState` enum, event dispatch, score integers
3. `player.py` — position, velocity, direction, `CharState` enum (ALIVE/CRASHING/DEAD/POSING/RESPAWNING)
4. `beam.py` — axis-aligned line segment, dt-scaled velocity, 2-wrap expiry, 10-beam ring buffer, `clipline()` hit detection
5. `sound.py` — `SoundManager`: effects on dedicated `Channel(0)`, music via `pygame.mixer.music`
6. `assets.py` — loads and caches all surfaces and sounds at startup; never called from draw loop
7. `settings.py` — all magic numbers as named constants; no logic
8. `hud.py` — in-game score overlay

---

## Build Order

1. **Foundation** — coordinate system constants, asset conversion pipeline (ICO→PNG, MIDI→WAV), `settings.py`
2. **Game loop skeleton** — `clock.tick(60)` with correct `dt`, `GameState` enum, window open/close
3. **Player movement** — `CharState` enum, `get_pressed()` input, dt-scaled movement, screen wrap, directional sprites
4. **Beam system + collision** — axis-aligned line segment, `clipline()` hit detection, `in (3, 4)` direction checks, ring buffer
5. **Death, scoring, HUD** — `CharState` transitions, crash animation, respawn, score display, win condition
6. **Audio** — `SoundManager`, dedicated SFX channel, trimmed WAV loop, mute toggle
7. **Screens** — SPLASH credits scroll, GAME_OVER with restart prompt
8. **Polish + packaging** — upscaled sprites, hit flash, mouse-click mechanic, PyInstaller `.exe`

---

## Critical Pitfalls

1. **VB6 `Or 4` bug survives in Python** — `if beam.dir == 3 or 4:` is always True. Write `if beam.dir in (3, 4):`. Add a unit test.
2. **Twip values look like pixel values but are 15x off** — `intImgHeight = 850` is twips (~57px). Define all geometry from scratch in pixels.
3. **Frame-rate-dependent movement** — use `dt = clock.tick(60) / 1000.0` and multiply ALL position increments by `dt`.
4. **Replicating VB6 timers with `pygame.time.set_timer`** — wrong approach. One `Clock.tick(60)` loop replaces all five VB6 timers.
5. **Boolean crash flags instead of a state enum** — VB6's `blnSCrash` set in two places creates race conditions. Use `CharState` enum per character.
6. **VB6 draw-then-erase vs pygame clear-then-draw** — blit a pre-baked `background_surface` at frame start; never do per-beam erasure.

---

## Open Questions (Decisions Needed Before Planning)

1. **Sprite scale target: 2x (64×64) or 4x (128×128)?** — determines `SCREEN_WIDTH`, beam length, all geometry constants
2. **Win condition on or off by default?** — `WIN_SCORE = 0` (infinite, matching original) vs. `WIN_SCORE = 50` (match-based)
3. **In-game HUD vs. window title for scores?** — pick one before Phase 5
4. **OGG vs. WAV for background music?** — OGG supports loop-point metadata; WAV is simpler
5. **OmnipotentShootingGuy score: shown plainly in HUD or hinted as secret?**
