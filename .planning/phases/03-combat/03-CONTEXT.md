# Phase 3: Combat - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Create `beam.py` with the `Beam` class. Players fire colored line beams (LEFT/RIGHT only) that travel at `BEAM_SPEED`, wrap horizontally, and expire after 2 full wraps. When a beam's line segment intersects the opponent's rect, the opponent enters `CRASHING` state (frozen in place — Phase 4 adds the animation). Each player owns a `deque(maxlen=10)` of active beams.

**Requirements in scope:** CMB-01, CMB-02, CMB-03, CMB-04, CMB-05, CMB-06, CMB-07, CMB-08
**Out of scope:** Crash animation, fall-to-ground physics, death state, respawn, scoring, HUD (Phases 4+); vertical beam travel; audio (Phase 5)

</domain>

<decisions>
## Implementation Decisions

### Beam Visual Appearance
- **D-01:** Beam is rendered as a `pygame.draw.line` — length **40px**, width **3px**. No sprite asset needed.
- **D-02:** Colors are already defined in `settings.py`: `SUPERMAN_BEAM_COLOR = (200, 0, 0)`, `GOBLIN_BEAM_COLOR = (0, 200, 0)`. Use them directly.

### Firing Direction
- **D-03:** Beams fire **LEFT/RIGHT only**. If `player.facing` is `DIR_UP` or `DIR_DOWN` at fire time, fall back to the player's start direction: Superman → `DIR_LEFT`, Goblin → `DIR_RIGHT`.
- **D-04:** Firing is triggered by `KEYDOWN` (one-shot). Superman fires on `pygame.K_LSHIFT` / `pygame.K_RSHIFT`; Goblin fires on `pygame.K_r`. Both handled in `game.py`'s event loop, which calls `player.fire()`.
- **D-05:** Beam direction at fire time is `player.facing` if it is `DIR_LEFT` or `DIR_RIGHT`, otherwise the fallback above.

### Beam Wrap and Expiry
- **D-06:** Beams track `distance_traveled` (float, px). A horizontal beam expires when `distance_traveled >= SCREEN_W * 2` (2 full wraps). Wrap: when `beam.x < -BEAM_LENGTH` → `beam.x = SCREEN_W`; when `beam.x > SCREEN_W` → `beam.x = -BEAM_LENGTH`.
- **D-07:** `BEAM_LENGTH = 40` (the visual length constant, in `settings.py`). Used for both rendering and wrap threshold.

### Beam Ownership
- **D-08:** Each `Player` owns `self.beams = collections.deque(maxlen=10)`. Oldest beam is replaced automatically when the limit is hit (deque handles this).
- **D-09:** `Player.fire(direction)` creates a `Beam` and appends to `self.beams`. `Player.update(dt, keys)` updates beams only when `state == ALIVE`.
- **D-10:** Collision checked in `game.py`: for each player, iterate over the opposing player's `beams` and call `player.rect.clipline(beam.start, beam.end)`. If a hit is detected, set `player.state = CharState.CRASHING`.

### Collision Check (VB6 Or-bug fix)
- **D-11:** Collision guard MUST use `if beam.direction in (DIR_LEFT, DIR_RIGHT):` — never `beam.direction == DIR_LEFT or DIR_RIGHT`. This is enforced by CLAUDE.md and CMB-08. Since beams only ever carry `DIR_LEFT` or `DIR_RIGHT` (D-03), this check always passes — but the pattern must be written correctly regardless.

### CRASHING State in Phase 3
- **D-12:** When a beam hits, the opponent's state is set to `CharState.CRASHING`. Player freezes in place at their last rendered sprite (`player.update()` already returns early for non-ALIVE states). No visual change beyond frozen movement — Phase 4 adds spin frames, fall animation, and death state.
- **D-13:** CRASHING is a terminal state in Phase 3 (no recovery mechanism). Phase 4 adds respawn keys and the dead→alive transition.

### Claude's Discretion
- Beam position: `beam.x`/`beam.y` is the **leading edge** of the 40px line. Rendering: `start = (beam.x, beam.y)`, `end = (beam.x - 40, beam.y)` for LEFT; `end = (beam.x + 40, beam.y)` for RIGHT. Adjust for direction.
- Beam start position at fire time: spawns at the player's center — `player.x + DISPLAY_SPRITE_SIZE // 2` (horizontal), `player.y + DISPLAY_SPRITE_SIZE // 2` (vertical center).
- Beams update independently of player state — once fired, they continue traveling even if the firer enters CRASHING state.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` §Combat — CMB-01 through CMB-08 define Phase 3 deliverables exactly
- `.planning/ROADMAP.md` §Phase 3 — success criteria are the acceptance test; all 5 must pass

### Project Constraints (non-negotiable)
- `CLAUDE.md` — ALL key constraints: geometry constants in `settings.py` only, `KEYDOWN` for one-shot actions, `beam.direction in (LEFT, RIGHT)` collision pattern, dt-scaling, no `pygame.sprite.Sprite`
- `.planning/PROJECT.md` §Constraints — faithfulness rules; port, not reimagination

### Existing Code (read before writing any Phase 3 code)
- `settings.py` — existing constants including `BEAM_SPEED = 400`, `GOBLIN_BEAM_COLOR`, `SUPERMAN_BEAM_COLOR`, `SCREEN_W`, direction constants; Phase 3 adds `BEAM_LENGTH = 40`
- `player.py` — `Player` class, `CharState` enum, `player.facing`, `player.rect` property (used for collision), `player.state`; Phase 3 adds `self.beams` and `fire()` method
- `game.py` — `Game.run()` event loop (Phase 3 adds KEYDOWN handlers for fire); `Game.update()` (Phase 3 adds beam update + collision check); `Game.draw()` (Phase 3 adds beam draw)
- `assets.py` — `AssetCache` key convention (beam is a drawn line — no sprite key needed)

### Prior Phase Context
- `.planning/phases/02-two-characters-move/02-CONTEXT.md` — Phase 2 decisions, especially `player.facing` initialization, `DISPLAY_SPRITE_SIZE`, direction constants

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `Player.rect` property: returns `pygame.Rect(int(x), int(y), DISPLAY_SPRITE_SIZE, DISPLAY_SPRITE_SIZE)` — ready for `clipline()` collision (CMB-07)
- `Player.facing`: already tracks last non-idle direction; Phase 3 reads this directly for beam direction
- `CharState.CRASHING`: already defined in the enum; `player.update()` already early-returns for non-ALIVE states — CRASHING freeze works with zero new code in player.update

### Established Patterns
- Plain class with `update(dt)` / `draw(screen)` — `Beam` follows this same pattern
- All constants in `settings.py`, imported at module top — `BEAM_LENGTH`, `BEAM_SPEED` stay there
- dt-scaled movement: `beam.x += BEAM_SPEED * dt` (LEFT subtracts, RIGHT adds); `distance_traveled += BEAM_SPEED * dt`
- Clear-then-draw: background blit in `game.draw()` already clears beams — no per-beam erasure needed
- KEYDOWN events handled in `game.py Game.run()` loop — beam fire follows the same pattern as Delete-to-quit

### Integration Points
- `game.py Game.run()` event loop: add `elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT): self.players[0].fire(...)` and `elif event.key == pygame.K_r: self.players[1].fire(...)`
- `game.py Game.update(dt)`: after `player.update()` calls, add beam update + collision check loop
- `game.py Game.draw()`: after player draws, add beam draw loop
- `player.py Player.__init__`: add `self.beams = deque(maxlen=10)`
- New module: `beam.py` — `Beam` class, `update(dt)`, `draw(screen)`, position/direction/distance tracking

</code_context>

<specifics>
## Specific Ideas

- The 40px bolt length is intentional — shorter than the 108px sprite, making it feel like a discrete projectile you can track rather than a dominant visual element.
- Firing fallback direction (Superman=LEFT, Goblin=RIGHT) aligns with their starting positions — they always face inward at game start, so a vertical-only player fires toward their opponent by default.
- `deque(maxlen=10)` is the correct Python idiom for the ring buffer (CMB-05) — no manual eviction code needed.

</specifics>

<deferred>
## Deferred Ideas

- Vertical beam support (UP/DOWN beams with collision) — deferred per user decision; LEFT/RIGHT only in Phase 3.
- CRASHING visual feedback (spin frame 1 on hit) — user chose pure stub; Phase 4 adds full crash animation.
- Beam sound effect (`LASER.WAV` on fire) — Phase 5 scope (AUD-01).

</deferred>

---

*Phase: 3-Combat*
*Context gathered: 2026-05-16*
