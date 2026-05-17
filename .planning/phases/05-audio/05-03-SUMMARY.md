---
phase: 05-audio
plan: "03"
subsystem: tests
tags: [audio, testing, unit-tests, integration-tests, mocking]
dependency_graph:
  requires: ["05-01", "05-02"]
  provides: ["AUD-01-tests", "AUD-02-tests", "AUD-03-tests", "AUD-04-tests", "AUD-05-tests", "AUD-06-tests"]
  affects: []
tech_stack:
  added: []
  patterns: ["unittest.mock.patch for pygame.mixer.music module", "MagicMock for Sound objects", "inspect.getsource for wiring verification"]
key_files:
  created:
    - tests/test_sound.py
  modified: []
decisions:
  - "Patched 'pygame.mixer.music' as a whole module (MagicMock) rather than individual methods — cleaner and matches plan spec"
  - "make_game() passes real sounds dict (not full MagicMock) so SoundManager can key into it by string"
  - "Source inspection tests used for game.py wiring — avoids running the full game loop in tests"
metrics:
  duration: "3 minutes"
  completed_date: "2026-05-17"
  tasks_completed: 1
  tasks_total: 1
  files_created: 1
  files_modified: 0
---

# Phase 5 Plan 03: Audio Tests Summary

20 pytest unit + integration tests covering SoundManager (sound.py) and game.py audio wiring for AUD-01 through AUD-06.

## What Was Built

`tests/test_sound.py` with 20 tests grouped by requirement:

- **AUD-01 (2 tests):** `play_laser()` calls `laser.play()` when unmuted; skips when muted
- **AUD-02 (2 tests):** `play_death_cry()` calls `deathcry.play()` when unmuted; skips when muted
- **AUD-03 (2 tests):** `play_explode()` calls `explode.play()` when unmuted; skips when muted
- **AUD-04 (2 tests):** `play_playing_music()` stops first, then loads `passport.wav` and loops with `play(-1)`
- **AUD-05 (2 tests):** `play_splash_music()` stops first, then loads `canyon.wav` and loops with `play(-1)`
- **stop_music (1 test):** `stop_music()` calls `pygame.mixer.music.stop()`
- **AUD-06 (4 tests):** `toggle_mute()` flips `_muted` flag; calls `mixer.pause()`/`music.pause()` when muting; calls `mixer.unpause()`/`music.unpause()` when unmuting; double-toggle restores to unmuted
- **Integration (5 tests):** Source inspection confirms `Game.__init__` creates `self.snd` as `SoundManager`; `Game.update` contains `was_crashing`/`play_explode`, `play_death_cry`, and `stop_music`; `Game.run` contains `play_laser`, `K_m`, and `toggle_mute`

## Results

- `python -m pytest tests/test_sound.py -v` — 20 passed
- `python -m pytest tests/ -v` — 86 passed (66 prior + 20 new, zero regressions)

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None.

## Threat Flags

None — all mixer calls are mocked in tests; no real audio output.

## Self-Check: PASSED

- `tests/test_sound.py` exists and contains 20 test functions
- All 20 tests collected and pass
- No regressions in prior 66 tests
