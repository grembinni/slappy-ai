---
phase: 03-combat
plan: 04
status: complete
date: 2026-05-16
---

# 03-04 Summary: Wire Beam System into game.py

## What Was Done

Made 4 targeted additions to `game.py` to connect the beam system (beam.py, player.beams, player.fire()) into the live game loop. No existing code was modified — only additions.

### Change 1 — Imports
- Added `from collections import deque` (stdlib, needed for deque rebuild in update)
- Added `CharState` to the `from player import Player` line
- Extended `from settings import ...` with `DIR_LEFT, DIR_RIGHT`

### Change 2 — KEYDOWN fire handlers in `Game.run()`
Added two branches after the `K_DELETE` handler:
- `K_LSHIFT` / `K_RSHIFT` → Superman fires; facing fallback to `DIR_LEFT` if vertical/idle
- `K_r` → Goblin fires; facing fallback to `DIR_RIGHT` if vertical/idle
- Both guards: only `ALIVE` players can fire (CRASHING/DEAD silently ignored)

### Change 3 — Beam update + collision in `Game.update(dt)`
After the existing `player.update()` loop:
- **Step A**: For each player, rebuild `player.beams` as a `deque(maxlen=10)` keeping only beams where `b.update(dt)` returns True (expired beams auto-dropped, CMB-06)
- **Step B**: Collision loop — for each ALIVE player, iterate `list(opponent.beams)`, check `beam.direction in (DIR_LEFT, DIR_RIGHT)` (CMB-08 VB6 Or-bug fix), then `player.rect.clipline(beam.start, beam.end)`; on hit set `player.state = CharState.CRASHING` and break

### Change 4 — Beam draw in `Game.draw()`
After the player draw loop but before `pygame.display.flip()`, added a nested loop that calls `beam.draw(self.screen)` for every beam owned by every player.

## Files Changed

- `d:\dev\repo\slappy-ai\game.py` — 4 additions (imports, KEYDOWN handlers, beam update+collision, beam draw)

## Verify Output

```
pygame-ce 2.5.7 (SDL 2.32.10, Python 3.11.2)
game.py phase3 OK
```

All assertions passed:
- Superman beam created on `fire(DIR_LEFT)` ✓
- Beam teleported into goblin rect intersects via `clipline()` ✓
- `gob.state == CharState.CRASHING` after `g.update(0.016)` ✓
- CRASHING goblin does not move on subsequent update ✓
- `'beam.direction in (DIR_LEFT, DIR_RIGHT)'` present in source ✓
- `'beam.direction == DIR_LEFT or DIR_RIGHT'` absent from source ✓

## Full Test Suite

```
50 passed in 3.30s
```

No regressions from Phases 1/2.

## Requirements Met

| Req | Description | Status |
|-----|-------------|--------|
| CMB-01 | Shift fires Superman beam on KEYDOWN | done |
| CMB-02 | R fires Goblin beam on KEYDOWN | done |
| CMB-03 | Firing direction fallback (vertical → default) | done |
| CMB-06 | Beams update each frame, expired removed | done |
| CMB-07 | Collision via player.rect.clipline() | done |
| CMB-08 | VB6 Or-bug fix: `in (DIR_LEFT, DIR_RIGHT)` | done |
| DTH-01 | Hit player enters CharState.CRASHING | done |
