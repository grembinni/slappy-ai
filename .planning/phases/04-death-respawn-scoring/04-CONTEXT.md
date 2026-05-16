# Phase 4: Death, Respawn & Scoring - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Animate the CRASHING state (spin sprites + fall to ground), implement DEAD state with respawn, implement scoring (pose auto-score + beam hit bonus, OmnipotentShootingGuy), add the in-game HUD overlay, and wire the GAME_OVER transition when any score reaches WIN_SCORE.

**Requirements in scope:** DTH-01, DTH-02, DTH-03, DTH-04, DTH-05, DTH-06, DTH-07, SCR-01, SCR-02, SCR-03, SCR-04, SCR-05, SCR-06
**Out of scope:** Crash sound (Phase 5), hit sound (Phase 5), splash/credits screen (Phase 6), pause mechanic (Phase 6), F2 restart (Phase 6), PyInstaller packaging (Phase 6)

</domain>

<decisions>
## Implementation Decisions

### Crash Animation (DTH-01, DTH-02, DTH-03, DTH-04)
- **D-01:** CRASHING player falls at **fixed speed** equal to `PLAYER_SPEED_DOWN` (500 px/s), dt-scaled. No gravity acceleration.
- **D-02:** Spin sprite cycle: **loop sspin1→2→3→4→1 at 100ms each** throughout the entire fall. Cycle continues regardless of fall progress, resets on new hit.
- **D-03:** When falling player's `y` reaches `GROUND_STOP_Y`: snap y to `GROUND_STOP_Y`, switch to death sprite (`sdeath` / `gdeath`), enter `DEAD` state. Instant — no bounce.
- **D-04:** During CRASHING, the character falls straight down (dy = PLAYER_SPEED_DOWN * dt, dx = 0). Horizontal position stays fixed from where the hit occurred.
- **D-05:** `player.update()` already early-returns for non-ALIVE states. Phase 4 adds a dedicated CRASHING update path that drives the fall and spin — called before the ALIVE early-return check, or by restructuring the state dispatch.

### Respawn (DTH-05, DTH-06)
- **D-06:** **Superman respawns with `K_UP` (↑ arrow key)** — same as move-up, state-gated (only processed in DEAD state). Symmetrical with Goblin.
- **D-07:** **Goblin respawns with `K_w`** — same as move-up, state-gated (only processed in DEAD state).
- **D-08:** Respawn zone: **random x** across full screen width; **random y in the upper 70% of the play area** — between `CEILING_STOP_Y` and `CEILING_STOP_Y + 0.7 * (GROUND_STOP_Y - CEILING_STOP_Y)`.
- **D-09:** No respawn delay and no invincibility frames. Player appears at random position and is immediately ALIVE and hittable.
- **D-10:** Respawn is a `KEYDOWN` event (one-shot), handled in `game.py`'s event loop. Same pattern as beam fire.

### OmnipotentShootingGuy (DTH-07, SCR-04)
- **D-11:** `MOUSEBUTTONDOWN` event in `game.py`: for each living player (`state == ALIVE`), check if `event.pos` is within `player.rect`. If hit, set `player.state = CharState.CRASHING` and increment the OmnipotentShootingGuy score by 1.

### Scoring Formula (SCR-01, SCR-02, SCR-03)
- **D-12:** Pose scoring triggers **automatically** when a player is ALIVE, idle in the air (`player._direction == DIR_IDLE` and `not player._on_ground`). **No key press required** — overrides SCR-02's Ctrl/Space requirement.
- **D-13:** No visual sprite change during pose scoring — character shows normal idle sprite, score accumulates silently.
- **D-14:** Score accumulation per player: `raw_pose` (+1 per game frame while idle-airborne), `hit_bonus` (+10 each time that player lands a beam hit on the opponent).
- **D-15:** **Displayed score** = `raw_pose // 10 + hit_bonus`. Win condition checks displayed score against `WIN_SCORE = 50`.
- **D-16:** Beam hit scoring: when collision is detected in `game.py`, increment the shooter's `hit_bonus` by 10 (shooter = `self.players[1 - i]` when `players[i]` is hit).

### HUD Overlay (SCR-05)
- **D-17:** Superman score: **top-left** of screen. Goblin score: **top-right**. OmnipotentShootingGuy score: **top-center**, hidden when score == 0.
- **D-18:** Label format: `"{Name}: {score}"` — e.g., `"Superman: 12"` and `"Goblin: 8"` and `"OmnipotentShootingGuy: 3"`.
- **D-19:** Font: `pygame.font.Font(None, 28)` (pygame default, size 28). Text color: white `(255, 255, 255)`. Shadow/outline: 1px dark offset at `(2, 2)` for sky readability.
- **D-20:** HUD drawn every frame in `game.py Game.draw()` — after beams, before `pygame.display.flip()`. Lives in a new `hud.py` module with a `draw_hud(screen, players, osg_score, font)` function.

### Win Condition (SCR-06)
- **D-21:** After updating scores each frame, check all displayed scores. If any `>= WIN_SCORE (50)`, set `self.state = GameState.GAME_OVER`. Game loop stops updating/drawing game entities in GAME_OVER state (Phase 6 adds the actual GAME_OVER screen; Phase 4 just transitions the state).

### Claude's Discretion
- `player.raw_pose` and `player.hit_bonus` stored as `int` attributes on `Player`, initialized to 0 in `__init__`.
- `player.score` property: returns `self.raw_pose // 10 + self.hit_bonus` — used by HUD and win check.
- `player.osg_score` is NOT on Player — OmnipotentShootingGuy score is owned by `Game` as `self.osg_score: int = 0`.
- CRASHING fall should set `player._direction = DIR_DOWN` so the existing draw code doesn't need special-casing (renders down sprite momentarily before spin cycle overrides it — spin cycle replaces `_get_sprite_key` logic for CRASHING state).
- Spin timer: `player._spin_timer: float = 0.0`, `player._spin_frame: int = 0` (0–3, maps to sspin1–4 / gspin1–4). Reset to 0 on entering CRASHING.
- Respawn: use `random.uniform(0, SCREEN_W - DISPLAY_SPRITE_SIZE)` for x; `random.uniform(CEILING_STOP_Y, CEILING_STOP_Y + 0.7 * (GROUND_STOP_Y - CEILING_STOP_Y))` for y.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` §Death & Respawn (DTH-01–07) and §Scoring (SCR-01–06) — exact Phase 4 deliverables
- `.planning/ROADMAP.md` §Phase 4 — success criteria; all 5 must pass

### Project Constraints (non-negotiable)
- `CLAUDE.md` — ALL key constraints: geometry in `settings.py`, `KEYDOWN` for one-shot actions, dt-scaling, no `pygame.sprite.Sprite`, `pygame.key.get_pressed()` for movement
- `.planning/PROJECT.md` §Constraints — port fidelity rules

### Existing Code (read before writing any Phase 4 code)
- `player.py` — `Player` class, `CharState` enum, `player._direction`, `player._on_ground`, `player.state`, `player.facing`, `player.rect` property; Phase 4 adds `raw_pose`, `hit_bonus`, `score` property, `_spin_timer`, `_spin_frame`, and CRASHING/DEAD update paths
- `game.py` — `Game.run()` event loop (Phase 4 adds KEYDOWN respawn handlers + MOUSEBUTTONDOWN); `Game.update()` (Phase 4 adds score update + win check); `Game.draw()` (Phase 4 adds HUD draw)
- `settings.py` — `PLAYER_SPEED_DOWN`, `GROUND_STOP_Y`, `CEILING_STOP_Y`, `WIN_SCORE`, `DISPLAY_SPRITE_SIZE`
- `beam.py` — beam collision already produces CRASHING; Phase 4 makes it also increment shooter's hit_bonus

### Sprite Assets (all confirmed present in `assets/sprites/`)
- Superman: `sspin1.png`, `sspin2.png`, `sspin3.png`, `sspin4.png`, `sdeath.png`, `spose.png`
- Goblin: `gspin1.png`, `gspin2.png`, `gspin3.png`, `gspin4.png`, `gdeath.png`, `gpose.png`

### Prior Phase Context
- `.planning/phases/03-combat/03-CONTEXT.md` — beam collision sets `player.state = CharState.CRASHING` (D-12/D-13); Phase 4 animates this state

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `CharState.CRASHING`, `CharState.DEAD`, `CharState.POSING`, `CharState.RESPAWNING` — all defined in enum; Phase 4 activates CRASHING and DEAD (POSING/RESPAWNING may not be needed as states given D-12/D-13 decisions)
- `Player.rect` property — already returns `pygame.Rect` at current x/y; reused for mouse-click hit detection (DTH-07)
- `Player._direction` and `Player._on_ground` — already computed each update; directly drive pose scoring condition (D-12)
- `Game.state = GameState.GAME_OVER` — enum already defined; Phase 4 sets it when win condition met

### Established Patterns
- `player.update(dt, keys)` early-returns for non-ALIVE — Phase 4 must add CRASHING/DEAD handling BEFORE this guard or refactor the state dispatch
- dt-scaled movement: `dy = PLAYER_SPEED_DOWN * dt` for crash fall — same pattern as player movement
- `KEYDOWN` events in `game.py Game.run()` — respawn key handled here (same pattern as beam fire in Phase 3)
- `pygame.key.get_pressed()` for pose scoring condition check — or infer from `player._direction == DIR_IDLE` (already computed in update)
- `_AIR_SPRITES` dict drives `_get_sprite_key()` — spin sprites bypass this for CRASHING state; add a separate sprite key lookup for CRASHING

### Integration Points
- `game.py Game.update()`: after collision detection → increment `opponent.hit_bonus` by 10 when hit detected; check win condition
- `game.py Game.update()`: after player.update() calls → update raw_pose for idle-airborne ALIVE players
- `game.py Game.run()`: add `MOUSEBUTTONDOWN` handler after KEYDOWN block; add respawn KEYDOWN handlers
- `game.py Game.draw()`: add `draw_hud(self.screen, self.players, self.osg_score, self._hud_font)` call before `pygame.display.flip()`
- `player.py Player.__init__`: add `self.raw_pose = 0`, `self.hit_bonus = 0`, `self._spin_timer = 0.0`, `self._spin_frame = 0`
- New module: `hud.py` — `draw_hud(screen, players, osg_score, font)` function

</code_context>

<specifics>
## Specific Ideas

- Pose scoring auto-triggers on idle-in-air — no key required. The VB6 Ctrl/Space pose key mechanic is replaced with this automatic detection. This makes scoring feel more natural and reduces cognitive load.
- OmnipotentShootingGuy score hidden until > 0 — cleaner HUD when the mouse mechanic hasn't been used.
- Superman respawn = ↑ (same as move up), Goblin respawn = W (same as move up) — symmetric design, state-gated so no conflict.

</specifics>

<deferred>
## Deferred Ideas

- POSING CharState visual (spose/gpose sprite swap) — user chose silent pose scoring with no visual change; POSING state not needed in Phase 4
- Invincibility frames after respawn — user chose instant full combat; deferred entirely
- GAME_OVER screen content and restart mechanic — Phase 6 scope (only state transition in Phase 4)
- Bounce animation on ground landing — user chose snap-to-ground; deferred
- Sound effects on crash/hit/landing — Phase 5 scope

</deferred>

---

*Phase: 4-Death-Respawn-Scoring*
*Context gathered: 2026-05-16*
