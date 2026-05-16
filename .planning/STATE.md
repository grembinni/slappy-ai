# Project State

## Current Status
- Phase: 2
- Status: Planning complete — ready to execute
- Last updated: 2026-05-16
- Current Plan: 1/4

## Project Reference
See: .planning/PROJECT.md (updated 2026-05-16)

**Core value:** Two players on the same keyboard can immediately start blasting each other.
**Current focus:** Phase 2 — Two Characters Move

## Phase History
- Phase 1: Foundation — Complete (2026-05-16) — 5/5 plans, 15 tests passing

---

## Performance Metrics

- Requirements total: 50
- Requirements complete: 3 (ENG-01, ENG-02, ENG-03)
- Phases total: 6
- Phases complete: 1

| Phase | Plan | Duration (s) | Tasks | Files |
|-------|------|-------------|-------|-------|
| 01 | 05 | 162 | 3 | 5 |

## Accumulated Context

### Key Decisions
- Python 3.11 + pygame-ce 2.5.x (not original pygame)
- Pillow NEAREST resampling for ICO→PNG upscaling (preserves pixel art)
- FluidSynth for MIDI→WAV conversion at 44100 Hz
- PyInstaller 6.x --onedir --windowed for packaging
- Fix VB6 Or-bug: use `beam.direction in (LEFT, RIGHT)` not `== LEFT or RIGHT`
- All movement dt-scaled via `clock.tick(60) / 1000.0`
- Plain classes with `update(dt)` / `draw(screen)` — no `pygame.sprite.Sprite`
- pygame.mixer.init() in main.py only; AssetCache is caller-agnostic re: mixer
- convert_alpha() requires display.set_mode() first — tests use SDL_VIDEODRIVER=dummy

### Critical Pitfalls to Watch
- VB6 `Or 4` bug survives verbatim in Python — unit test required
- Twip values from VB6 source are 15x off pixels — define all geometry fresh in settings.py
- Do NOT use `pygame.time.set_timer` to replicate VB6 timers — one Clock.tick(60) loop only
- Clear-then-draw pattern: blit background_surface at frame start, never per-beam erasure

### Open Questions
- Win condition: WIN_SCORE = 50 (match-based, chosen for roadmap)
- OmnipotentShootingGuy score: shown plainly in HUD

### Phase 2 Decisions
- PLAYER_SPEED_UP = 200, PLAYER_SPEED_H = 300, PLAYER_SPEED_DOWN = 400 (px/s)
- Animation interval: ANIM_INTERVAL = 0.15s (~7 Hz); always ticks
- Idle sprite: Superman.ico / GEvil.ico (dedicated, not last-frame-held)
- Ground walk sprites (CKent/GEvil) in Phase 2; cycle 1→2→1→3 at 150ms each
- Ground is visual floor only — characters fly back up freely from GROUND_Y
- SPRITE_SIZE = 128 confirmed; all Superman sprites confirmed present

## Session Continuity

Last session: 2026-05-16
Stopped at: 02-01 complete — Phase 2 movement constants added to settings.py
Resume file: .planning/phases/02-two-characters-move/02-02-PLAN.md
Next: /gsd:execute-phase 2

Phase 2 wave structure:
  Wave 1: 02-01 (settings.py)
  Wave 2: 02-02 (player.py) — blocked on Wave 1
  Wave 3: 02-03 (game.py) + 02-04 (test_player.py) — parallel, blocked on Wave 2

Start each session by reading:
1. `.planning/STATE.md` (this file) — current position
2. `.planning/ROADMAP.md` — phase goals and success criteria
3. `.planning/REQUIREMENTS.md` — requirement details for current phase
