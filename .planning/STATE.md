# Project State

## Current Status
- Phase: 5
- Status: Complete — all 3 plans executed, 86 tests passing
- Last updated: 2026-05-16
- Current Plan: 3/3

## Project Reference
See: .planning/PROJECT.md (updated 2026-05-16)

**Core value:** Two players on the same keyboard can immediately start blasting each other.
**Current focus:** Phase 5 — Audio

## Phase History
- Phase 1: Foundation — Complete (2026-05-16) — 5/5 plans, 15 tests passing
- Phase 2: Two Characters Move — Complete (2026-05-16) — 4/4 plans, 35 tests passing
- Phase 3: Combat — Complete (2026-05-16) — 5/5 plans, 50 tests passing
- Phase 4: Death, Respawn & Scoring — Complete (2026-05-16) — 5/5 plans, 66 tests passing
- Phase 5: Audio — Complete (2026-05-16) — 3/3 plans, 86 tests passing

---

## Performance Metrics

- Requirements total: 50
- Requirements complete: 40 (ENG-01–05, MOV-01–10, CMB-01–08, DTH-01–07, SCR-01–06, AUD-01–06)
- Phases total: 6
- Phases complete: 4

| Phase | Plan | Duration (s) | Tasks | Files |
|-------|------|-------------|-------|-------|
| 01 | 05 | 162 | 3 | 5 |
| 02 | 04 | — | 4 | 4 |
| 03 | 05 | — | 5 | 3 |
| 04 | 05 | — | 5 | 5 |

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

### Phase 3 Decisions
- Beams fire LEFT/RIGHT only; 40px bolt, 3px thick
- Beam ownership: player.beams deque(maxlen=10)
- CRASHING state: freeze in place (pure stub) — Phase 4 adds animation
- VB6 Or-bug fix: `beam.direction in (DIR_LEFT, DIR_RIGHT)` — locked

### Phase 4 Decisions
- SPIN_INTERVAL = 0.1s (100ms per spin frame, loops sspin1→2→3→4→1)
- Fixed fall speed: PLAYER_SPEED_DOWN (500 px/s), dt-scaled, no gravity
- Snap to GROUND_STOP_Y on landing → DEAD state (no bounce)
- Pose scoring: automatic when ALIVE + DIR_IDLE + not on_ground (+1/frame; displayed = raw_pose//10)
- Hit bonus: +10 per beam hit landed (shooter gets hit_bonus += 10)
- Respawn: K_UP for Superman, K_w for Goblin (state-gated to DEAD, no conflict with move-up)
- Respawn zone: random x full width, random y upper 70% of play area
- OSG score: MOUSEBUTTONDOWN on living player → start_crash() + osg_score++; hidden in HUD when 0
- HUD: pygame default font size 28, white text with 2px dark shadow; top-left/right/center
- Win condition: any displayed score >= WIN_SCORE (50) → GAME_OVER

### Phase 6 Decisions
- Escape/P toggle pause (PLAYING only); Delete = hard quit; audio pauses with game
- Splash: dark navy bg (0,0,64), 25 VB6 credits verbatim, random sprite pool at 750ms, controls at bottom
- Win score selector on splash: Up/Down in steps of 10 (range 10–500, default 50); passed to Game constructor
- Restart = full Game reinit back to SPLASH; F2/Enter only from GAME_OVER
- GAME_OVER: black bg, scores + "F2 or Enter to restart", no winner callout
- New splash.py module; GAME_OVER rendering in game.py; SoundManager gets pause_game()/resume_game()

## Session Continuity

Last session: 2026-05-16
Stopped at: Phase 6 context gathered — 06-CONTEXT.md written
Next: /gsd:plan-phase 6 (Screens & Packaging)

Start each session by reading:
1. `.planning/STATE.md` (this file) — current position
2. `.planning/ROADMAP.md` — phase goals and success criteria
3. `.planning/REQUIREMENTS.md` — requirement details for current phase
