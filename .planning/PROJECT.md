# Goblin vs. Superman (Python Port)

## What This Is

A Python/pygame port of "Goblin vs. Superman" — a 2-player local-multiplayer game originally written in Visual Basic 6 by Airman Hurdle during his Air Force service. Both players fly around the screen, shoot laser beams at each other, and score points by landing hits or striking a pose. The game is lightly modernized: same mechanics and spirit, bugs fixed, sprites upscaled, and MIDI music converted to WAV.

## Core Value

Two players on the same keyboard can immediately start blasting each other — the moment the game opens, the chaos should feel exactly like the original.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Splash/credits screen with scrolling "Hurdle's Mom Inc. Intl." credits and alternating character art
- [ ] 2-player game on shared keyboard (Superman: arrows + Shift/Ctrl/Enter; Goblin: ESDF + R/Space/W)
- [ ] Both characters fly freely in the play area with ground and ceiling boundaries
- [ ] Horizontal screen wrapping for both characters
- [ ] Directional animated sprites (idle, up, down, left, right, pose, death, spin) for each character
- [ ] Laser beam shooting in current direction, beams travel and wrap horizontally
- [ ] Beam-to-character collision detection (kills the hit player)
- [ ] Death/crash animation: character spins and falls to the ground
- [ ] Respawn after death (Enter for Superman, W for Goblin)
- [ ] Pose scoring: earn points while holding pose key
- [ ] Hit scoring: earn +10 per enemy hit
- [ ] Secret "OmnipotentShootingGuy" mouse-click mechanic: clicking a character kills them and adds to a third score
- [ ] Score displayed in window title bar: "Goblin [N] Superman [N] OmnipotentShootingGuy [N]"
- [ ] New game (F2) and quit (Delete) hotkeys
- [ ] WAV sound effects: laser shot, death cry, explosion
- [ ] Background music: MIDI files (Canyon.mid, Passport.mid) converted to WAV, played on loop during gameplay

### Out of Scope

- Online/network multiplayer — local 2-player only
- New gameplay mechanics — this is a port, not a sequel
- AI/CPU opponent — two human players only
- Resizable window or fullscreen toggle — fixed resolution

## Context

- Original source: `D:\dev\repo\best-game-ever\_old\` (VB6 `.frm` files, `.ico` sprites, WAV/MIDI sounds)
- Sprites are tiny `.ico` files (32x32); they will be upscaled or redrawn to ~64x64 or 128x128 PNG for pygame rendering
- MIDI background music must be converted to WAV before shipping (tools: timidity, fluidsynth, or midiutil + soundfont)
- The original has a known VB6 bug: `ElseIf .bytDir = 3 Or 4 Then` is always true, making all shots detect hits regardless of direction — this will be fixed in the Python version
- "They aren't bugs, they're features." — preserve the chaotic feel even while fixing actual logic errors
- Made by the user when they were in the Air Force; "Hurdle's Mom Inc. Intl." is the fictional studio name from the credits

## Constraints

- **Tech stack**: Python + pygame — no other game frameworks
- **Asset source**: Reuse existing sprites (upscaled) and WAV files from the original repo
- **Faithfulness**: Same core gameplay, same controls, same scoring — lightly modernized, not reimagined

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python + pygame | Standard choice for 2D Python games; direct mapping from VB6 timer/image model | — Pending |
| Upscale/redraw sprites to PNG | Tiny ICOs won't render well at modern resolutions | — Pending |
| Convert MIDI to WAV | pygame's MIDI support is unreliable on Windows 11; WAV works everywhere | — Pending |
| Fix VB6 Or-bug in collision detection | Bug makes all shots hit regardless of direction alignment | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-16 after initialization*
