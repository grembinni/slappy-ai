# Phase 3: Combat - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 3-Combat
**Areas discussed:** Beam visuals, Firing direction, CRASHING state depth, Beam ownership

---

## Beam Visuals

| Option | Description | Selected |
|--------|-------------|----------|
| Short bolt (~40px) | Looks like a discrete projectile — you see it moving across the screen | ✓ |
| Medium beam (~80px) | Good balance — visible laser feel without dominating the screen | |
| Long beam (~120–160px) | Feels more like a sustained laser blast | |

**User's choice:** Short bolt (~40px)
**Notes:** —

| Option | Description | Selected |
|--------|-------------|----------|
| 2px — thin laser | Crisp, pixel-art feel. Matches the small sprite aesthetic | |
| 4px — chunky bolt | More visible, easier to see mid-flight | |
| You decide | Use 3px — split the difference | ✓ |

**User's choice:** You decide (3px)
**Notes:** Deferred to Claude — 3px selected as split between thin and chunky.

---

## Firing Direction

| Option | Description | Selected |
|--------|-------------|----------|
| LEFT/RIGHT only | Beam always fires horizontally; if player.facing is UP/DOWN, fall back to start direction | ✓ |
| All 4 directions, all collide | UP/DOWN beams travel vertically and can hit players | |
| All 4 directions, only LEFT/RIGHT collide | UP/DOWN beams travel but pass through players | |

**User's choice:** LEFT/RIGHT only
**Notes:** Resolves the CMB-03 vs CLAUDE.md tension — game uses horizontal beams only. Aligns with original VB6 side-scroller feel.

| Option | Description | Selected |
|--------|-------------|----------|
| Default to start direction | Superman=LEFT, Goblin=RIGHT when facing is UP/DOWN | ✓ |
| Track separate horizontal facing | Player tracks beam_facing updated only on L/R key presses | |

**User's choice:** Default to player's start direction
**Notes:** Superman defaults to LEFT, Goblin defaults to RIGHT for the UP/DOWN edge case.

---

## CRASHING State Depth

| Option | Description | Selected |
|--------|-------------|----------|
| Freeze in place (pure stub) | Hit player stops at last sprite, no visual change — Phase 4 fills in | ✓ |
| Show first spin frame (sspin1/gspin1) | Minimal visual hit feedback using existing assets | |

**User's choice:** Freeze in place (pure stub)
**Notes:** Phase 4 owns all crash visual behavior. Phase 3 just sets the state.

---

## Beam Ownership

| Option | Description | Selected |
|--------|-------------|----------|
| Player-owned (player.beams deque) | Each Player has self.beams = deque(maxlen=10); game.py loops over opposing player's beams for collision | ✓ |
| Game-owned (game.beams list) | game.beams holds all beams with owner attribute; game handles all logic centrally | |

**User's choice:** Player-owned (player.beams deque)
**Notes:** Keeps beam logic close to the firer; deque(maxlen=10) handles ring buffer eviction automatically.

---

## Claude's Discretion

- **Beam thickness:** 3px (user deferred to Claude)
- **Beam leading edge position:** `beam.x`/`beam.y` is the leading edge; rendering calculates trailing end from direction
- **Beam spawn position:** player center (`player.x + DISPLAY_SPRITE_SIZE // 2`, same for y)
- **Beam continues after firer enters CRASHING:** once fired, beams are independent of firer state

## Deferred Ideas

- Vertical beam support (UP/DOWN beams with collision) — user chose horizontal only; deferred to potential future phase
- CRASHING visual feedback (spin frame on hit) — user chose pure stub; Phase 4 scope
- Beam sound effect (LASER.WAV) — Phase 5 scope per roadmap
