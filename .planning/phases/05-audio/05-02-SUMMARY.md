---
phase: 05-audio
plan: "02"
subsystem: game
tags: [audio, sound, wiring, game-loop]
dependency_graph:
  requires: ["05-01"]
  provides: ["AUD-01", "AUD-02", "AUD-03", "AUD-04", "AUD-05", "AUD-06"]
  affects: ["game.py"]
tech_stack:
  added: []
  patterns: ["SoundManager dependency injection via assets.sounds dict"]
key_files:
  created: []
  modified:
    - game.py
decisions:
  - "was_crashing snapshot taken before player.update() so CRASHING→DEAD transition is detectable within the same frame"
  - "stop_music() placed inside 'if self.state == GameState.PLAYING:' guard to fire exactly once on transition"
  - "K_m handled as KEYDOWN (one-shot) per CLAUDE.md constraint — not get_pressed()"
metrics:
  duration: "5 minutes"
  completed: "2026-05-17T02:36:43Z"
  tasks_completed: 1
  files_modified: 1
---

# Phase 05 Plan 02: Wire SoundManager into game.py Summary

**One-liner:** Wired SoundManager into Game with 8 targeted insertions — startup music, laser SFX, death cry (collision + mouse click), explode on CRASHING→DEAD transition, mute toggle (K_m), and stop on GAME_OVER.

## What Was Done

Made 8 targeted changes to `game.py` only. No other files were modified.

| # | Change | Location |
|---|--------|----------|
| 1 | `from sound import SoundManager` import | Top of file |
| 2 | `self.snd = SoundManager(assets.sounds)` + `play_playing_music()` | `Game.__init__` after `_hud_font` |
| 3 | `was_crashing` snapshot + `play_explode()` on CRASHING→DEAD | `Game.update()` around player loop |
| 4 | `self.snd.play_death_cry()` after `player.start_crash()` | `Game.update()` collision block |
| 5 | `self.snd.stop_music()` on GAME_OVER transition | `Game.update()` win condition block |
| 6 | `self.snd.play_death_cry()` after `player.start_crash()` | `Game.run()` MOUSEBUTTONDOWN block |
| 7 | `self.snd.play_laser()` after `sup.fire(d)` and `gob.fire(d)` | `Game.run()` KEYDOWN block |
| 8 | `elif event.key == pygame.K_m: self.snd.toggle_mute()` | `Game.run()` KEYDOWN block |

## Verification

- Audio wiring assertion script: PASSED (`game.py audio wiring OK`)
- Regression tests: 16/16 passed (`tests/test_death.py`)

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None.

## Threat Flags

None — no new network endpoints, auth paths, or trust boundaries introduced. All changes are local game-loop event wiring.

## Self-Check: PASSED

- `game.py` exists and contains all 8 changes (confirmed by verification script)
- All assertions in the verify script passed with exit 0
- All 16 regression tests passed
