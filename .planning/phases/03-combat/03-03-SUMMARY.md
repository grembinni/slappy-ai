---
phase: 03-combat
plan: 03
status: complete
---

# 03-03 SUMMARY — Player beam support (self.beams + fire())

## What was done

Extended `player.py` with the minimum changes required for beam firing:

1. **Imports added** at the top of `player.py`:
   - `from collections import deque` (stdlib, before pygame)
   - `from beam import Beam` (after pygame import)
   - `SUPERMAN_BEAM_COLOR, GOBLIN_BEAM_COLOR` added to the existing `from settings import` block

2. **`self.beams` deque** added at the end of `Player.__init__`:
   - `self.beams: deque = deque(maxlen=10)` — ring buffer capped at 10 beams (D-08)

3. **`Player.fire(direction: int) -> None`** method added between `update()` and `draw()`:
   - No-op guard: returns immediately if `self.state != CharState.ALIVE` (CRASHING/DEAD cannot fire)
   - Spawns beam at player center: `cx = self.x + DISPLAY_SPRITE_SIZE // 2`, `cy = self.y + DISPLAY_SPRITE_SIZE // 2`
   - Selects color by character: `SUPERMAN_BEAM_COLOR` for superman, `GOBLIN_BEAM_COLOR` for goblin
   - Appends `Beam(cx, cy, direction, color)` to `self.beams`

No other code was touched — `update()`, `draw()`, `_get_sprite_key()`, and class-level tables are unchanged.

## Files changed

- `player.py` — imports extended, `self.beams` added to `__init__`, `fire()` method added

## Verify output

### Plan automated verify script
```
pygame-ce 2.5.7 (SDL 2.32.10, Python 3.11.2)
player.py phase3 OK
```
All assertions passed:
- `self.beams` exists, is a `deque`, has `maxlen == 10`
- `fire(DIR_LEFT)` on superman produces 1 beam with correct direction and `SUPERMAN_BEAM_COLOR`
- Beam x-position matches player center within 1px
- CRASHING player cannot fire (beam count stays at 1)
- Goblin beam color is `GOBLIN_BEAM_COLOR`
- Firing 11 times caps at 10 beams (deque eviction confirmed)

### Player tests (regression)
```
tests/test_player.py .................... 20 passed in 1.44s
```

### Full test suite
```
tests/test_assets.py .....
tests/test_convert.py ...
tests/test_player.py ....................
tests/test_settings.py .......
35 passed in 2.26s
```
