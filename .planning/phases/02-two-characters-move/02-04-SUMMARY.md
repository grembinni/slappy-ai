---
phase: 02-two-characters-move
plan: "04"
subsystem: tests/player
tags: [tests, player, movement, animation, charstate, pytest]

dependency_graph:
  requires:
    - "02-02"   # player.py (Player class and CharState enum)
    - "02-01"   # settings.py constants
  provides:
    - tests/test_player.py  # 20 unit tests covering MOV-01 through MOV-10
  affects: []

tech_stack:
  added: []
  patterns:
    - "SDL dummy drivers set at module level before any pygame import"
    - "MagicMock AssetCache with defaultdict(lambda: pygame.Surface(...))"
    - "make_keys(*keys_down) positional-arg helper — avoids keyword-must-be-string error with int key constants"
    - "autouse pygame_init fixture handles init/quit for every test"

key_files:
  created:
    - tests/test_player.py
  modified: []

decisions:
  - "make_keys uses *args (positional key constants) not **kwargs — pygame key constants are ints, not valid Python identifiers for keyword unpacking"
  - "pygame_init fixture defined in test_player.py (not conftest.py) since conftest has no pygame fixture"
  - "test_superman_moves_down sets p.y = SCREEN_H//2 explicitly to ensure player is in air before testing down movement"
  - "test_horizontal_wrap_right/left set x out-of-bounds before update so wrap triggers regardless of dt-scaled movement"

metrics:
  duration: "~15 minutes"
  completed: "2026-05-16"
  tasks_completed: 1
  files_created: 1
  files_modified: 0
---

# Phase 2 Plan 04: Player Unit Tests Summary

One-liner: 20 headless pytest unit tests for Player/CharState covering all Phase 2 movement, boundary, animation, and sprite-selection requirements (MOV-01 through MOV-10).

## What Was Built

`tests/test_player.py` containing:

1. **Module header** — `SDL_VIDEODRIVER=dummy` and `SDL_AUDIODRIVER=dummy` set before any pygame import, ensuring fully headless execution.

2. **Fixtures and helpers:**
   - `pygame_init` (autouse=True) — handles `pygame.init()` / `pygame.quit()` for every test
   - `make_assets()` — MagicMock AssetCache; every sprite key returns a real `pygame.Surface((128, 128))`
   - `make_keys(*keys_down)` — returns `defaultdict(bool)` with given integer key constants set True

3. **20 test functions** in requirement order:

| # | Test | Requirements |
|---|------|-------------|
| 1 | `test_charstate_enum` | MOV-07 |
| 2 | `test_player_initial_state_superman` | MOV-07 |
| 3 | `test_player_initial_state_goblin` | MOV-07 |
| 4 | `test_superman_moves_right` | MOV-01, MOV-03 |
| 5 | `test_superman_moves_left` | MOV-01, MOV-03 |
| 6 | `test_superman_moves_up` | MOV-01, MOV-03 |
| 7 | `test_superman_moves_down` | MOV-01, MOV-03 |
| 8 | `test_goblin_moves_right` | MOV-02, MOV-03 |
| 9 | `test_ceiling_clamp` | MOV-06 |
| 10 | `test_ground_clamp` | MOV-05 |
| 11 | `test_horizontal_wrap_right` | MOV-04 |
| 12 | `test_horizontal_wrap_left` | MOV-04 |
| 13 | `test_rect_property` | Phase 3 prereq |
| 14 | `test_animation_frame_toggles` | MOV-08 |
| 15 | `test_get_sprite_key_idle_air` | MOV-09 |
| 16 | `test_get_sprite_key_ground_idle` | MOV-09 |
| 17 | `test_get_sprite_key_ground_walk` | MOV-08, MOV-09, D-10 |
| 18 | `test_no_downward_movement_on_ground` | MOV-05, D-11 |
| 19 | `test_dt_scaling` | MOV-03, CLAUDE.md dt constraint |
| 20 | `test_both_players_move_independently` | MOV-01, MOV-02 |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] make_keys changed from **kwargs to *args**
- **Found during:** Task 1 first test run
- **Issue:** Plan specified `make_keys(**{pygame.K_RIGHT: True})` but `pygame.K_RIGHT` is an integer constant, and Python keyword arguments must be strings. This raises `TypeError: keywords must be strings`.
- **Fix:** Changed `make_keys(**pressed)` to `make_keys(*keys_down)` — accepts positional integer key constants and sets each to True in the defaultdict. All call sites updated to `make_keys(pygame.K_RIGHT)` pattern.
- **Files modified:** `tests/test_player.py`
- **Commit:** 39a00c9 (included in the single task commit)

## Verification Output

```
============================= test session starts =============================
platform win32 -- Python 3.11.2, pytest-9.0.3, pluggy-1.6.0
rootdir: d:\dev\repo\slappy-ai
configfile: pytest.ini
collected 20 items

tests\test_player.py ....................                                [100%]

============================= 20 passed in 1.55s ==============================
```

Full suite regression (35 tests, 0 failures):

```
tests\test_assets.py .....   [ 14%]
tests\test_convert.py ...    [ 22%]
tests\test_player.py ......  [ 80%]
tests\test_settings.py ..... [100%]

============================= 35 passed in 2.39s ==============================
```

## Known Stubs

None — all 20 tests exercise real Player behavior. No placeholder assertions.

## Threat Flags

None — test-only file; no new network endpoints, auth paths, file access, or schema changes.

## Self-Check: PASSED

- `d:/dev/repo/slappy-ai/tests/test_player.py` — exists, 20 test functions
- Commit `39a00c9` — `test(02-04): add 20 unit tests for Player class covering MOV-01 through MOV-10` — verified in git log
