---
plan: 04-02
phase: 04-death-respawn-scoring
status: complete
---

# Plan 04-02: player.py — crash/death/respawn/scoring

## What was built

Extended `player.py` with 10 targeted changes implementing the full Phase 4 player lifecycle:

1. `import random` added at top
2. `SPIN_INTERVAL` added to settings import
3. `_SPIN_SPRITES` and `_DEATH_SPRITE` class-level tables added (after `_GROUND_IDLE_SPRITE`)
4. Scoring attributes in `__init__`: `raw_pose=0`, `hit_bonus=0`, `_spin_timer=0.0`, `_spin_frame=0`
5. `score` property: `raw_pose // 10 + hit_bonus`
6. `update()` restructured: CRASHING dispatch added before the ALIVE early-return guard
7. `_update_crashing(dt)`: falls at `PLAYER_SPEED_DOWN*dt`, advances spin frame at `SPIN_INTERVAL` (while loop for large dt), transitions to DEAD at `GROUND_STOP_Y`
8. `start_crash()`: sets CRASHING, resets spin state
9. `respawn()`: random x/y in upper 70% play area, returns to ALIVE, clears beams
10. `_get_sprite_key()`: DEAD → death sprite, CRASHING → spin sprite (checks before existing on_ground logic)

## Verification

- `player.py phase4 OK` — all assertions passed
- `py -3.11 -m pytest tests/test_player.py -v` — 20/20 passed (no regressions)

## Requirements covered

DTH-01 (start_crash), DTH-02 (fall speed), DTH-03 (spin cycle), DTH-04 (DEAD at ground), DTH-05 (respawn method), SCR-01 (score property), SCR-03 (hit_bonus attribute)
