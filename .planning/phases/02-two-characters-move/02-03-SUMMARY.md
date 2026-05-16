---
phase: 02-two-characters-move
plan: "03"
subsystem: game-loop-integration
tags: [game, player, integration, wiring]
dependency_graph:
  requires: ["02-01", "02-02"]
  provides: ["player-update-draw-loop"]
  affects: ["game.py"]
tech_stack:
  added: []
  patterns: ["clear-then-draw", "dt-based update", "single get_pressed call"]
key_files:
  modified:
    - path: game.py
      role: "Main game controller — Player instances wired into update/draw cycle"
decisions:
  - "pygame.key.get_pressed() called once per frame in Game.update() and passed to each Player.update() — satisfies MOV-03 and CLAUDE.md constraint"
  - "Draw order: background -> superman -> goblin -> display.flip() (clear-then-draw, Phase 1 pattern preserved)"
metrics:
  duration: "< 5 minutes"
  completed: "2026-05-16"
  tasks_completed: 1
  tasks_total: 1
  files_modified: 1
---

# Phase 02 Plan 03: Wire Player into game.py — Summary

## One-liner

Surgical 4-addition patch to game.py: imports Player, creates two player instances in `__init__`, calls `get_pressed`/`player.update` in `update()`, and blits players in `draw()`.

## What Was Done

Four targeted additions were made to `game.py`. No existing code was removed or restructured.

| Addition | Location | Change |
|----------|----------|--------|
| 1 | Top of file (imports) | `from player import Player` added after existing imports |
| 2 | `Game.__init__` | `self.players = [Player("superman", ...), Player("goblin", ...)]` after background bake |
| 3 | `Game.update()` | Replaced `pass` with `keys = pygame.key.get_pressed()` + loop calling `player.update(dt, keys)` |
| 4 | `Game.draw()` | Added player draw loop between background blit and `pygame.display.flip()` |

## Verification

Headless integration test passed:

```
pygame-ce 2.5.7 (SDL 2.32.10, Python 3.11.2)
Structural checks: PASSED
  - from player import Player: found
  - self.players in __init__: found
  - get_pressed in update: found
  - player.draw in draw: found
Integration checks: PASSED
  - game.players has 2 entries
  - players[0] is superman, players[1] is goblin
  - update(0.016) ran without error
  - draw() ran without error

game.py integration OK
```

## Deviations from Plan

None — plan executed exactly as written. The plan specified "three additions" in the title but listed four in the task body; all four were applied as specified.

## Known Stubs

None. Both Player instances are fully constructed from the AssetCache and respond to keyboard input.

## Threat Flags

None. No new network endpoints, auth paths, or file access patterns introduced. The `pygame.key.get_pressed()` call site matches the planned trust boundary (T-02-05 accepted, T-02-06 mitigated by asset validation from Phase 1).

## Self-Check: PASSED

- `game.py` exists and contains all four additions — confirmed by Read tool
- Integration test ran without assertion errors in headless SDL mode
- Phase 1 behavior preserved: background renders, `run()` loop and event handling untouched, `_bake_background()` untouched, `GameState` untouched
