---
phase: 05-audio
plan: 01
subsystem: audio
tags: [sound, SoundManager, pygame.mixer, mute]
dependency_graph:
  requires: []
  provides: [sound.SoundManager]
  affects: [game.py]
tech_stack:
  added: []
  patterns: [pygame.mixer.music for streaming, pygame.mixer.Sound for SFX, pause/unpause for mute]
key_files:
  created: [sound.py]
  modified: []
decisions:
  - "Use pygame.mixer.music for background music (streaming, not loaded into RAM)"
  - "Mute uses pause/unpause, not stop/restart, so playback position is preserved"
  - "Music methods do not guard on _muted; toggle_mute handles pause after the fact"
  - "_MUSIC_DIR derived from pathlib.Path(__file__).parent so it works from any cwd"
metrics:
  duration: "< 5 minutes"
  completed: "2026-05-16"
  tasks_completed: 1
  tasks_total: 1
  files_created: 1
  files_modified: 0
---

# Phase 05 Plan 01: SoundManager Summary

## One-liner

Created `sound.py` with `SoundManager` — single audio authority for SFX (laser, death cry, explode), streaming background music via `pygame.mixer.music`, and a pause-preserving mute toggle.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Create sound.py with SoundManager | 9386b4d | sound.py (created) |

## Decisions Made

- `pygame.mixer.music` used for streaming WAV music (passport.wav, canyon.wav) — not loaded as Sound objects
- Mute implemented via `pygame.mixer.pause()` / `pygame.mixer.music.pause()` so mid-play sounds resume from their exact position on unmute
- SFX methods (`play_laser`, `play_death_cry`, `play_explode`) each guard with `if self._muted: return` before calling `.play()`
- Music methods (`play_playing_music`, `play_splash_music`) call `music.stop()` first to cleanly switch tracks
- `_MUSIC_DIR` is a module-level constant derived from `pathlib.Path(__file__).parent / "assets" / "sounds"`
- `intro.wav` exists on disk but has no AUD requirement; not referenced

## Deviations from Plan

None — plan executed exactly as written.

## Verification

Automated verification passed:
- All 7 public methods present
- `_muted` starts `False`
- Mute guard prevents SFX `.play()` when muted
- Mute guard allows SFX `.play()` when unmuted
- `toggle_mute()` flips flag and calls `mixer.pause()` / `music.pause()` when muting
- `toggle_mute()` flips flag and calls `mixer.unpause()` / `music.unpause()` when unmuting

Output: `sound.py OK`

## Known Stubs

None.

## Threat Flags

None — all threats accepted per plan threat model (local dev files, no external input paths).

## Self-Check: PASSED

- `d:\dev\repo\slappy-ai\sound.py` exists
- Commit `9386b4d` exists in git log
