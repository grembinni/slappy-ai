# Phase 4: Death, Respawn & Scoring - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 4-Death-Respawn-Scoring
**Areas discussed:** Crash animation, HUD layout, Pose scoring, Respawn specifics

---

## Crash Animation

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed speed | Falls at PLAYER_SPEED_DOWN (500 px/s) — simple, predictable | ✓ |
| Accelerating (gravity) | Starts slow, accelerates — more realistic but complex | |
| You decide | Claude picks simplest implementation | |

**User's choice:** Fixed speed

---

| Option | Description | Selected |
|--------|-------------|----------|
| Loop sspin1→2→3→4→1 at 100ms | Matches DTH-03, constant rotation throughout fall | ✓ |
| One pass then hold last frame | Goes through once then holds sspin4 | |
| You decide | Claude picks based on VB6 behavior | |

**User's choice:** Loop continuously at 100ms per frame

---

| Option | Description | Selected |
|--------|-------------|----------|
| Snap to GROUND_STOP_Y, show death sprite, enter DEAD | Instant on ground contact | ✓ |
| Bounce animation first | Brief bounce before death sprite | |
| You decide | Claude picks simplest | |

**User's choice:** Snap to ground, instant DEAD state

---

## HUD Layout

| Option | Description | Selected |
|--------|-------------|----------|
| Top corners + center | Superman top-left, Goblin top-right, OSG top-center | ✓ (with condition) |
| All top-left stacked | Three scores in one corner | |
| Bottom of screen | Below the play area | |

**User's choice:** Top corners + center — but OmnipotentShootingGuy score only shows when > 0
**Notes:** OSG score hidden at 0, appears when mouse mechanic is used.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Character name + score number | "Superman: 12" | ✓ |
| Score number only | Just "12" | |
| Short tag + score | "S: 12" / "G: 8" / "OSG: 3" | |

**User's choice:** "Superman: 12" format

---

| Option | Description | Selected |
|--------|-------------|----------|
| pygame default font, size 28 | No asset dependency, white with shadow | ✓ |
| Larger, size 36 | More prominent | |
| You decide | Claude picks readable size | |

**User's choice:** pygame default font, size 28

---

## Pose Scoring

| Option | Description | Selected |
|--------|-------------|----------|
| Show pose sprite while holding key | spose/gpose visible while Ctrl/Space held | |
| Score quietly, no sprite change | Score accumulates silently | |
| You decide | Claude picks based on VB6 | |

**User's choice:** Score posing when in the air and not moving — no button press needed
**Notes:** User overrode SCR-02's Ctrl/Space key requirement. Posing is automatic when idle-airborne. No POSING CharState or visual change needed.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — show pose sprite when idle-airborne | spose/gpose during scoring | |
| No — keep normal idle sprite, score silently | Silent accumulation | ✓ |

**User's choice:** No visual change — silent scoring

---

| Option | Description | Selected |
|--------|-------------|----------|
| Use formula as-is: displayed = raw//10 + hit_bonus | Full formula | ✓ |
| Simplify — just count beam hits | No pose score | |
| You decide | Claude picks | |

**User's choice:** Use formula as-is

---

## Respawn Specifics

| Option | Description | Selected |
|--------|-------------|----------|
| Random x, random y in upper half | Upper 50% of play area | |
| Fixed starting positions | Return to original x=75%/25% | |
| Random x, fixed y at midscreen | Only horizontal randomized | |

**User's choice:** Random x and y in upper 70% of play area
**Notes:** User specified "upper 70%" as the spawn zone.

---

| Option | Description | Selected |
|--------|-------------|----------|
| W works for both Goblin — state-gated | Same key, different state behavior | ✓ |
| Change respawn to a different key | e.g., Tab | |

**User's choice:** W for Goblin respawn (state-gated with UP movement)

**Follow-up:** User also changed Superman's respawn from Enter to K_UP (↑ arrow), making it symmetric — both characters respawn with their UP movement key.

---

| Option | Description | Selected |
|--------|-------------|----------|
| No delay — instant, immediately hittable | Simple, matches VB6 | ✓ |
| Brief invincibility (1-2 seconds) | Fairer but complex | |

**User's choice:** Instant respawn, no invincibility

---

## Claude's Discretion

- `player.score` as a property (`raw_pose // 10 + hit_bonus`) rather than a stored attribute
- `osg_score` owned by `Game` not `Player`
- `_spin_timer` and `_spin_frame` as player attributes for crash animation
- Respawn x/y computed with `random.uniform()`
- HUD in a new `hud.py` module with `draw_hud()` function

## Deferred Ideas

- POSING CharState visual (sprite swap) — not needed; silent auto-pose chosen
- Invincibility frames — deferred (instant respawn chosen)
- GAME_OVER screen content — Phase 6 scope
- Bounce animation on landing — deferred (snap-to-ground chosen)
- Sound effects — Phase 5 scope
