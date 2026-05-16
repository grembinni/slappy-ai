# Project State

## Current Status
- Phase: 1
- Status: Planned — Ready to execute (5 plans, 3 waves)
- Last updated: 2026-05-16

## Project Reference
See: .planning/PROJECT.md (updated 2026-05-16)

**Core value:** Two players on the same keyboard can immediately start blasting each other.
**Current focus:** Phase 1 — Foundation

## Phase History
(none yet)

---

## Performance Metrics

- Requirements total: 50
- Requirements complete: 0
- Phases total: 6
- Phases complete: 0

## Accumulated Context

### Key Decisions
- Python 3.11 + pygame-ce 2.5.x (not original pygame)
- Pillow NEAREST resampling for ICO→PNG upscaling (preserves pixel art)
- FluidSynth for MIDI→WAV conversion at 44100 Hz
- PyInstaller 6.x --onedir --windowed for packaging
- Fix VB6 Or-bug: use `beam.direction in (LEFT, RIGHT)` not `== LEFT or RIGHT`
- All movement dt-scaled via `clock.tick(60) / 1000.0`
- Plain classes with `update(dt)` / `draw(screen)` — no `pygame.sprite.Sprite`

### Critical Pitfalls to Watch
- VB6 `Or 4` bug survives verbatim in Python — unit test required
- Twip values from VB6 source are 15x off pixels — define all geometry fresh in settings.py
- Do NOT use `pygame.time.set_timer` to replicate VB6 timers — one Clock.tick(60) loop only
- Clear-then-draw pattern: blit background_surface at frame start, never per-beam erasure

### Open Questions
- Sprite scale target: 2x (64x64) or 4x (128x128)? → settings.py says 128; confirm before Phase 2
- Win condition: WIN_SCORE = 50 (match-based, chosen for roadmap)
- OmnipotentShootingGuy score: shown plainly in HUD

## Session Continuity

Start each session by reading:
1. `.planning/STATE.md` (this file) — current position
2. `.planning/ROADMAP.md` — phase goals and success criteria
3. `.planning/REQUIREMENTS.md` — requirement details for current phase
