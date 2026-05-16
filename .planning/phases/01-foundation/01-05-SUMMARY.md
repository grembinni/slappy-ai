---
phase: 01-foundation
plan: "05"
subsystem: game-core
tags: [walking-skeleton, asset-loading, game-loop, gamestate-enum]
dependency_graph:
  requires: ["01-01", "01-02", "01-04"]
  provides: [main.py, game.py, assets.py, tests/test_assets.py]
  affects: [all future phases — Game/AssetCache are the foundation]
tech_stack:
  added: []
  patterns:
    - "Bake-once background surface (blit each frame, no per-entity erasure)"
    - "AssetCache: keyed dict[str, Surface | Sound] loaded at startup"
    - "dt = clock.tick(FPS) / 1000.0 — float seconds, FPS from settings"
key_files:
  created:
    - main.py
    - game.py
    - assets.py
    - tests/test_assets.py
  modified:
    - tests/test_settings.py
decisions:
  - "pygame.mixer.init() called in main.py only — AssetCache is caller-agnostic"
  - "convert_alpha() requires display surface first — tests use SDL_VIDEODRIVER=dummy + set_mode"
  - "autouse pygame_init fixture handles SDL dummy drivers transparently"
metrics:
  duration_seconds: 162
  completed_date: "2026-05-16"
  tasks_completed: 3
  files_changed: 5
---

# Phase 1 Plan 5: Walking Skeleton — Game Loop, AssetCache, and Bootstrap Summary

**One-liner:** Walking skeleton is live — main.py opens a 1280x800 window with cyan/white/green background, loads 40 sprites and 6 sounds via AssetCache, runs at 60 FPS with dt-scaled updates, and exits cleanly.

## What Was Built

Three source files deliver the Phase 1 walking skeleton:

**`assets.py` — AssetCache**
- Loads all `*.png` from `assets/sprites/` as `pygame.Surface` via `.convert_alpha()`
- Loads all `*.wav` from `assets/sounds/` as `pygame.mixer.Sound`
- Keys by `filename_stem.lower()` (e.g. `gevil.png` → `"gevil"`, `laser.wav` → `"laser"`)
- Raises `FileNotFoundError` with actionable message if `assets/` is absent
- Result: 40 sprites, 6 sounds loaded at startup

**`game.py` — GameState enum and Game class**
- `GameState(Enum)`: SPLASH, PLAYING, PAUSED, GAME_OVER via `auto()`
- `Game._bake_background()`: static surface with cyan sky, 50px white ceiling, 50px green ground — all from settings constants
- `Game.run()`: `dt = clock.tick(FPS) / 1000.0`, handles QUIT and K_DELETE
- `Game.update(dt)`: pass stub (Phase 1 — no gameplay entities)
- `Game.draw()`: `screen.blit(self.background, (0,0))` + `pygame.display.flip()`

**`main.py` — Bootstrap entry point**
- `pygame.init()` + `pygame.mixer.init()` → `display.set_mode` → `AssetCache()` → `Game(screen, assets)` → `game.run()` → `pygame.quit()`

**`tests/test_assets.py` — ENG-03 integration tests**
- 5 tests: cache loads, surfaces, sounds, key naming, sprite size (128x128)
- Module-level `skipif` guard when `assets/sprites/` absent
- `autouse` fixture with SDL dummy drivers for headless execution

**`tests/test_settings.py` — Skip removed**
- `@pytest.mark.skip(reason="game.py created in Plan 05")` removed from `test_gamestate_enum`
- Test now passes (imports `GameState` from `game`)

## Verification Results

```
GameState members: ['SPLASH', 'PLAYING', 'PAUSED', 'GAME_OVER']  ✓
AssetCache: 40 sprites, 6 sounds  ✓
pytest tests/ -v: 15 passed, 0 failed, 0 error  ✓
```

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] convert_alpha() requires display surface**
- **Found during:** Task 1 verification
- **Issue:** `pygame.image.load(...).convert_alpha()` raises `pygame.error: No convert format has been set` when no display surface exists
- **Fix:** Test fixture and verification commands call `pygame.display.set_mode((1280, 800))` after `pygame.init()`. The `assets.py` code is correct (display is set by `main.py` in production). Tests use `SDL_VIDEODRIVER=dummy` for headless operation.
- **Files modified:** `tests/test_assets.py` (autouse fixture includes `set_mode`)
- **Commit:** 2182b87

## Known Stubs

- `Game.update(dt)`: `pass` — intentional Phase 1 stub. Phase 2 (player movement) will add entity updates here. No data flows to UI from this stub — `draw()` only blits the static background.

## Threat Flags

None — no new network endpoints, auth paths, file access patterns, or schema changes beyond the controlled `assets/` filesystem boundary already in the plan's threat model.

## Self-Check: PASSED

Files exist:
- `D:/dev/repo/slappy-ai/assets.py` — FOUND
- `D:/dev/repo/slappy-ai/game.py` — FOUND
- `D:/dev/repo/slappy-ai/main.py` — FOUND
- `D:/dev/repo/slappy-ai/tests/test_assets.py` — FOUND

Commits exist:
- 61ccb50 — feat(01-05): implement AssetCache — FOUND
- 3aa1049 — feat(01-05): implement Game class, GameState enum — FOUND
- 2182b87 — feat(01-05): implement main.py bootstrap and test_assets.py — FOUND
