# Phase 2: Two Characters Move - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 2-Two-Characters-Move
**Areas discussed:** Player speed, Animation cadence, Ground-walking sprites, Superman's missing SLeft1

---

## Player Speed

| Option | Description | Selected |
|--------|-------------|----------|
| 300 px/s | Covers ~23% of screen width per second. Responsive without chaotic. | |
| 200 px/s | Slower, more deliberate feel. | |
| 400 px/s | Same as BEAM_SPEED. | |
| You decide | Claude picks a reasonable default. | |

**User's choice:** 300 px/s (horizontal baseline)

**Follow-up — vertical asymmetry:**

| Option | Description | Selected |
|--------|-------------|----------|
| Same speed both axes | 300 px/s up/down/left/right. Symmetric. | |
| Slower vertical | e.g. 200 up, 300 horizontal. Gravity-influenced. | |
| You decide | Claude picks. | |

**User's choice (free text):** "200 up 300 side to side 400 down"
**Notes:** Asymmetric vertical speeds give a gravity-influenced feel without real physics — rising is harder, falling is faster.

**Follow-up — per-character speeds:**

| Option | Description | Selected |
|--------|-------------|----------|
| Same speeds for both | One set of constants, fair and symmetric. | ✓ |
| Different per character | e.g. Goblin slightly faster. | |

**User's choice:** Same speeds for both

---

## Animation Cadence

| Option | Description | Selected |
|--------|-------------|----------|
| Every 100ms (~10 Hz) | Closest to VB6 timer-based feel. | |
| Every frame (60 Hz) | Literal MOV-08 interpretation — very fast flickering. | |
| Every 150ms (~7 Hz) | Slower, chunkier pixel-art feel. | ✓ |
| You decide | Claude picks. | |

**User's choice:** Every 150ms (~7 Hz)

**Follow-up — when to animate:**

| Option | Description | Selected |
|--------|-------------|----------|
| Only while moving | Frame stays at 0 when no key held. | |
| Always animate | Ticks even when idle. | ✓ |

**User's choice:** Always animate

**Follow-up — idle sprite:**

| Option | Description | Selected |
|--------|-------------|----------|
| Last direction's first frame | Hold the frame at key release. | |
| Dedicated idle sprite | Use Superman.ico / GEvil.ico as explicit idle. | ✓ |

**User's choice:** Dedicated idle sprite

---

## Ground-walking sprites (Phase 2 or later?)

| Option | Description | Selected |
|--------|-------------|----------|
| Save for Phase 4 | Phase 2 enforces boundary only; CKent/GEvil are death/respawn scope. | |
| Add it in Phase 2 | When at GROUND_Y, switch to CKent/GEvil walk sprites. | ✓ |

**User's choice:** Add it in Phase 2

**Follow-up — ground movement freedom:**

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — ground is just a visual floor | Characters at GROUND_Y walk but can fly back up. | ✓ |
| No — ground locks horizontal walk only | Pressing Up lifts off; more complex state machine. | |

**User's choice:** Yes — ground is just a visual floor

**Follow-up — walk cycle:**

| Option | Description | Selected |
|--------|-------------|----------|
| Cycle 1→2→3→1 | All 3 frames in a loop at 150ms each. | |
| Use only frames 1→2 | 2-frame, ignores frame 3. | |

**User's choice (free text):** "1→2→1→3"
**Notes:** 4-step cycle: CKent1→CKent2→CKent1→CKent3→repeat (same for GEvil). Frame 1 is the neutral/plant position.

---

## Superman's Missing SLeft1 Sprite

| Option | Description | Selected |
|--------|-------------|----------|
| Use SLeft2 for both frames | Effectively 1-frame left animation. | |
| Mirror SRight1 horizontally | Generate SLeft1.png by flipping in convert_assets.py. | |
| I'll add SLeft1.ico manually | Manual sprite work. | |

**User's choice (free text):** "check again, both sprites should be there"
**Notes:** User was correct — targeted glob confirmed both `SLeft1.ico` and `SLeft2.ico` exist. The initial scan listed files by modification time and missed SLeft1. No action needed; Superman's sprite set is complete.

---

## Claude's Discretion

- **Starting positions:** Superman at (SCREEN_W * 0.75, SCREEN_H // 2), Goblin at (SCREEN_W * 0.25, SCREEN_H // 2) — facing inward at game start.
- **Initial facing direction:** Superman faces left (DIR_LEFT), Goblin faces right (DIR_RIGHT) — characters face each other.
- **Player architecture:** Single `Player` class with `character` parameter, not subclasses.
- **game.py integration:** Two Player instances in `Game.__init__`; `update(dt, keys)` and `draw(screen)` called from Game's update/draw.

## Deferred Ideas

- CKentIntro.ico / GEvilIntro.ico — splash/credits sprites; Phase 6 scope
- SPose / GPose / GPose2 — pose sprites; Phase 4 scope
- SSpin1–4 / GSpin1–4 — crash spin; Phase 4 scope
- SDeath / GDeath — death sprites; Phase 4 scope
