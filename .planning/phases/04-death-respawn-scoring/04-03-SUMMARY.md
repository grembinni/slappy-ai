---
phase: 04-death-respawn-scoring
plan: "03"
subsystem: hud
tags: [hud, scoring, rendering, pygame]
dependency_graph:
  requires: [settings.py]
  provides: [hud.py — draw_hud() function for score overlay]
  affects: [game.py — calls draw_hud() each frame before flip()]
tech_stack:
  added: []
  patterns: [shadow-then-foreground text blit, anchor-aware text placement]
key_files:
  created: [hud.py]
  modified: []
decisions:
  - "Shadow rendered before foreground text: shadow at (+2,+2) in black, then white text at (x,y)"
  - "Anchor modes (left/right/center) in single _blit() helper avoid code duplication"
  - "OmnipotentShootingGuy label hidden via if osg_score > 0 guard — no blit at all when 0"
metrics:
  duration_seconds: 55
  completed: "2026-05-17"
  tasks_completed: 1
  files_created: 1
---

# Phase 4 Plan 03: HUD Overlay Summary

**One-liner:** HUD score overlay with left/right/center anchoring, 2px shadow, and conditional OSG display using pygame font blitting.

## Tasks Completed

| # | Task | Commit | Files |
|---|------|--------|-------|
| 1 | Create hud.py with draw_hud() function | bf288c2 | hud.py |

## What Was Built

`hud.py` implements `draw_hud(screen, players, osg_score, font) -> None`:

- Superman score rendered top-left at (10, 10), left-anchored
- Goblin score rendered top-right at (SCREEN_W-10, 10), right-anchored (text width subtracted)
- OmnipotentShootingGuy score rendered top-center at (SCREEN_W//2, 10), center-anchored — only when `osg_score > 0`
- White text (255, 255, 255) with 2px dark shadow at (+2, +2) for sky readability
- Single `_blit()` inner function handles all three anchor modes, eliminating duplication
- Imports `SCREEN_W` from `settings.py` — no hardcoded pixel values per CLAUDE.md constraint

## Verification

- `python -c "from hud import draw_hud; print('import OK')"` — passed
- Full pygame render verification (dummy display, mock players with .score) — passed, printed "hud.py OK"
- Both `osg_score=0` (OSG hidden) and `osg_score=3` (OSG shown) tested without error

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None.

## Threat Flags

None — hud.py only reads `player.score` (int) and `osg_score` (int), renders to screen. No new network endpoints, auth paths, file access, or schema changes.

## Self-Check: PASSED

- hud.py exists at project root: FOUND
- Commit bf288c2 exists: FOUND
- draw_hud() renders without error for osg_score=0 and osg_score>0: VERIFIED
- No STATE.md or ROADMAP.md modifications: CONFIRMED
