---
phase: 02-two-characters-move
plan: "02"
subsystem: player
tags: [player, movement, animation, charstate, pygame]

dependency_graph:
  requires:
    - "02-01"   # settings.py constants (PLAYER_SPEED_*, ANIM_INTERVAL, DIR_*)
  provides:
    - player.py  # Player class and CharState enum for all subsequent phases
  affects:
    - game.py    # Phase 2 plan 03 will wire Player into Game.update/Game.draw

tech_stack:
  added: []
  patterns:
    - "Plain class with update(dt, keys) / draw(screen) — no pygame.sprite.Sprite"
    - "Class-level sprite tables keyed by direction constant (never runtime string format)"
    - "dt-scaled position increments for frame-rate independence"
    - "Animation timer via elapsed accumulator (subtract ANIM_INTERVAL, don't reset to 0)"

key_files:
  created:
    - player.py
  modified: []

decisions:
  - "Superman starts at SCREEN_W*0.75, facing DIR_LEFT; Goblin at SCREEN_W*0.25, facing DIR_RIGHT"
  - "Ground is visual-only (D-08): CharState stays ALIVE, sprites switch to CKent/GEvil walk"
  - "Down key suppressed when on_ground (D-11) — prevents tunnelling through floor"
  - "Animation always ticks (D-04): idle air sprite alternates superman/superman (no-op visually)"
  - "Walk cycle uses 4-step index list [0,1,0,2] into 3-sprite array (D-10: 1->2->1->3)"
  - "pygame.key.get_pressed() called by game.py, keys passed in as argument (MOV-03)"

metrics:
  duration: "~20 minutes"
  completed: "2026-05-16"
  tasks_completed: 1
  files_created: 1
  files_modified: 0
---

# Phase 2 Plan 02: Player Class Summary

One-liner: Player class with CharState enum, dt-scaled movement, 2-frame air animation, and 4-step ground walk cycle for both Superman and Goblin.

## What Was Built

`player.py` containing:

1. **`CharState` enum** — `ALIVE`, `CRASHING`, `DEAD`, `POSING`, `RESPAWNING`. Phase 2 uses only `ALIVE`; the others are stubs for Phases 3–4.

2. **`Player` class** — parameterised by `character` ("superman" or "goblin"). Single class, no subclasses (D-12).

## Player Public API

### Attributes (set in `__init__`, readable by callers)

| Attribute | Type | Description |
|-----------|------|-------------|
| `character` | `str` | `"superman"` or `"goblin"` |
| `assets` | `AssetCache` | Sprite/sound store; not mutated by Player |
| `state` | `CharState` | Lifecycle state; Phase 2 = always `ALIVE` |
| `x` | `float` | Horizontal position (pixels, left edge of sprite) |
| `y` | `float` | Vertical position (pixels, top edge of sprite) |
| `facing` | `int` | Last non-idle direction constant (used by Phase 3 beam firing) |

### Methods

| Signature | Description |
|-----------|-------------|
| `update(dt: float, keys) -> None` | Advance player by `dt` seconds given `pygame.key.get_pressed()` snapshot |
| `draw(screen: pygame.Surface) -> None` | Blit current animation frame |
| `rect` (property) | `pygame.Rect(int(x), int(y), SPRITE_SIZE, SPRITE_SIZE)` — for Phase 3 beam collision |

### Internal (not for callers)

`_get_sprite_key()`, `_anim_timer`, `_anim_frame`, `_ground_walk_step`, `_direction`, `_on_ground`, `_moving_h`

## Starting Positions and Facing Directions

| Character | x | y | facing |
|-----------|---|---|--------|
| superman | `SCREEN_W * 0.75` = 960.0 | `SCREEN_H // 2` = 400.0 | `DIR_LEFT` (3) |
| goblin | `SCREEN_W * 0.25` = 320.0 | `SCREEN_H // 2` = 400.0 | `DIR_RIGHT` (4) |

Characters face each other at game start.

## Sprite Key Tables

### Air sprites (2-frame alternation, one entry per direction)

| Direction | Superman frames | Goblin frames |
|-----------|----------------|--------------|
| `DIR_UP` | `sup1`, `sup2` | `gup1`, `gup2` |
| `DIR_DOWN` | `sdown1`, `sdown2` | `gdown1`, `gdown2` |
| `DIR_LEFT` | `sleft1`, `sleft2` | `gleft1`, `gleft2` |
| `DIR_RIGHT` | `sright1`, `sright2` | `gright1`, `gright2` |
| `DIR_IDLE` | `superman`, `superman` | `gevil`, `gevil` |

### Ground sprites

| | Superman | Goblin |
|---|---------|-------|
| Idle | `ckent` | `gevil` |
| Walk cycle (`[0,1,0,2]` index into list) | `ckent1`, `ckent2`, `ckent3` | `gevil1`, `gevil2`, `gevil3` |

### Key bindings

| Direction | Superman | Goblin |
|-----------|----------|--------|
| Up | `K_UP` | `K_e` |
| Down | `K_DOWN` | `K_d` |
| Left | `K_LEFT` | `K_s` |
| Right | `K_RIGHT` | `K_f` |

## Boundary Logic

- **Horizontal wrap (MOV-04):** `x < -SPRITE_SIZE` → `x = SCREEN_W`; `x > SCREEN_W` → `x = -SPRITE_SIZE`
- **Ceiling clamp (MOV-06):** `y` never < `CEILING_H` (50)
- **Ground clamp (MOV-05):** `y` never > `GROUND_Y` (750)
- **Down suppressed on ground (D-11):** `elif keys[ctrl[DIR_DOWN]] and not on_ground`

## Verification Output

```
pygame-ce 2.5.7 (SDL 2.32.10, Python 3.11.2)
player.py OK

pygame-ce 2.5.7 (SDL 2.32.10, Python 3.11.2)
Movement OK: 30.0 px right
Ground clamp OK
Wrap OK

pygame-ce 2.5.7 (SDL 2.32.10, Python 3.11.2)
rect OK

CharState members: ['ALIVE', 'CRASHING', 'DEAD', 'POSING', 'RESPAWNING']
```

All plan assertions passed headlessly via `SDL_VIDEODRIVER=dummy`.

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

`CharState.CRASHING`, `CharState.DEAD`, `CharState.POSING`, `CharState.RESPAWNING` are defined but never set in Phase 2. They are intentional stubs for Phases 3–4 (crash/death/pose mechanics). The `update()` guard `if self.state != CharState.ALIVE: return` is the hook for those phases.

## Threat Flags

None — no new network endpoints, auth paths, file access, or schema changes introduced.

## Self-Check: PASSED

- `d:/dev/repo/slappy-ai/player.py` — exists
- Commit `a25106c` — `feat(02-02): create player.py — CharState enum and Player class` — verified in git log
