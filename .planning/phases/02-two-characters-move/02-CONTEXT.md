# Phase 2: Two Characters Move - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Create `player.py` with the `Player` class and `CharState` enum. Both characters appear on screen, move smoothly with their respective keyboard controls, wrap horizontally, and respect ground/ceiling boundaries. Ground-walking sprites (CKent/GEvil) display when characters are at the ground boundary. Audio is out of scope; beam firing and combat are Phase 3.

**Requirements in scope:** MOV-01, MOV-02, MOV-03, MOV-04, MOV-05, MOV-06, MOV-07, MOV-08, MOV-09, MOV-10
**Out of scope:** Beam firing, collision detection, scoring, death/respawn mechanics, audio (Phases 3–5)

</domain>

<decisions>
## Implementation Decisions

### Player Speed
- **D-01:** Three directional speed constants go in `settings.py` (never in player.py):
  - `PLAYER_SPEED_UP = 200`     # px/s — slightly sluggish upward, gravity-feel
  - `PLAYER_SPEED_H = 300`      # px/s — left and right
  - `PLAYER_SPEED_DOWN = 400`   # px/s — faster downward fall
- **D-02:** Both Superman and Goblin share the same speed constants — symmetric and fair.

### Animation Cadence
- **D-03:** Frame flip interval is `ANIM_INTERVAL = 0.15` (seconds). Add to `settings.py`. This applies to both air and ground animations.
- **D-04:** Animation always ticks — even when idle (no key held). Characters never freeze to a static pose while alive.
- **D-05:** When no direction key is held (idle in air), show the character's dedicated idle sprite: `superman` (Superman.ico key) for Superman; `gevil` (GEvil.ico key) for Goblin. The idle sprite still alternates via the animation timer between `superman`/`superman` (1-frame effective no-op), preserving the always-animate rule.

### Air Sprite Animation (2-frame alternation)
- **D-06:** Each directional pair alternates frame 0 ↔ frame 1 every 150ms. Sprite key pairs:
  - Superman: up→(`sup1`,`sup2`), down→(`sdown1`,`sdown2`), left→(`sleft1`,`sleft2`), right→(`sright1`,`sright2`)
  - Goblin: up→(`gup1`,`gup2`), down→(`gdown1`,`gdown2`), left→(`gleft1`,`gleft2`), right→(`gright1`,`gright2`)
- **D-07:** All sprite keys follow the AssetCache convention: `png.stem.lower()` (e.g. `SLeft1.ico` → key `sleft1`).

### Ground-Walking Sprites (Phase 2 scope)
- **D-08:** Ground is a **visual floor, not a state change** — when `player.y >= GROUND_Y`, the character is "on the ground" and switches to CKent/GEvil walk sprites, but `CharState` remains `ALIVE`. Characters can freely move left, right, and upward (fly off the ground) without any state transition.
- **D-09:** Ground idle sprite: `ckent` (CKent.ico key) for Superman; `gevil` (GEvil.ico key) for Goblin.
- **D-10:** Ground walk cycle when moving left or right: **1→2→1→3** (4-step loop, 150ms each). Sprite keys:
  - Superman: `ckent1`, `ckent2`, `ckent1`, `ckent3`, repeat
  - Goblin: `gevil1`, `gevil2`, `gevil1`, `gevil3`, repeat
- **D-11:** On the ground, vertical movement keys are suppressed (characters can't fly downward through the floor). Pressing Up lifts them into the air, restoring air sprites. Ceiling boundary clamps `player.y` to `CEILING_H`.

### Player Architecture
- **D-12:** Single `Player` class in `player.py`, parameterized by `character` ("superman" or "goblin"). No subclasses — keeps the diff minimal and easy to extend in Phase 3.
- **D-13:** `CharState` enum defined in `player.py`: `ALIVE`, `CRASHING`, `DEAD`, `POSING`, `RESPAWNING`. Phase 2 uses only `ALIVE`.
- **D-14:** Player exposes `update(dt, keys)` and `draw(screen)` — consistent with the plain-class pattern established in Phase 1.

### Sprite Completeness
- **D-15:** All Superman air sprites are confirmed present in `raw_assets/icons/` — both `SLeft1.ico` and `SLeft2.ico` exist. No aliasing or mirroring needed.

### Claude's Discretion
- Direction tracking: Player stores `self.facing` (last non-idle direction) for use in Phase 3 beam firing. Initialize to `DIR_RIGHT` for Superman, `DIR_LEFT` for Goblin (characters face inward at game start).
- Starting positions: Superman starts at (SCREEN_W * 0.75, SCREEN_H // 2); Goblin starts at (SCREEN_W * 0.25, SCREEN_H // 2) — facing each other.
- `game.py` changes: instantiate two `Player` objects in `Game.__init__`; call `player.update(dt, keys)` and `player.draw(screen)` from `Game.update()` and `Game.draw()`.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` §Player Movement — MOV-01 through MOV-10 define Phase 2 deliverables exactly
- `.planning/ROADMAP.md` §Phase 2 — success criteria are the acceptance test; all 5 must pass

### Project Constraints
- `CLAUDE.md` — ALL key constraints: geometry constants in settings.py only, `pygame.key.get_pressed()` for movement, `KEYDOWN` only for one-shot actions, dt-scaling, no `pygame.sprite.Sprite`. **Non-negotiable.**
- `.planning/PROJECT.md` §Constraints — faithfulness rules; port, not reimagination

### Existing Code (read before writing any Phase 2 code)
- `settings.py` — existing constants; Phase 2 adds `PLAYER_SPEED_UP`, `PLAYER_SPEED_H`, `PLAYER_SPEED_DOWN`, `ANIM_INTERVAL`
- `assets.py` — AssetCache key convention: `png.stem.lower()`. All sprite lookups in player.py must use these exact keys.
- `game.py` — `update(dt)` and `draw()` stubs where Player calls are added. Game loop and `dt` calculation already established.

### Asset Manifest (sprite keys)
- `raw_assets/icons/` — all 39 ICO files. Phase 2 uses the movement + ground-walk sprites; spin/death/pose sprites exist but are Phase 3–4 scope.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `AssetCache` (`assets.py`): all sprites pre-loaded into `self.sprites` dict keyed by lowercase filename stem. Player.py accesses via `assets.sprites["sleft1"]` etc. — no loading needed in player.py.
- `settings.py` direction constants: `DIR_UP=1`, `DIR_DOWN=2`, `DIR_LEFT=3`, `DIR_RIGHT=4`, `DIR_POSE=5`, `DIR_IDLE=6` — already defined, use these everywhere.
- `GameState.PLAYING` in `game.py` — player updates should only run in this state (already the only active state in Phase 2).

### Established Patterns
- Plain class with `update(dt)` / `draw(screen)` — same as Game class; Player follows this exactly.
- All constants in `settings.py`, imported at module top — never define pixel values inline.
- `dt`-scaled movement: `pos += speed * dt` for all position updates.
- Clear-then-draw: background blit happens in `game.draw()` before player sprites; player.draw() blits on top.

### Integration Points
- `game.py Game.__init__`: add `self.players = [Player("superman", assets), Player("goblin", assets)]`
- `game.py Game.update(dt)`: add `keys = pygame.key.get_pressed()` and call `p.update(dt, keys)` for each player
- `game.py Game.draw()`: call `p.draw(self.screen)` for each player after background blit

</code_context>

<specifics>
## Specific Ideas

- Asymmetric speed (UP=200, H=300, DOWN=400) is intentional — gives a gravity-influenced feel without real physics. Planner must define all three as separate constants, not a single `PLAYER_SPEED`.
- Ground walk cycle is a 4-step sequence `[1, 2, 1, 3]` (index into this list, advance by 1 each 150ms), not a simple ping-pong. Both characters share this pattern but with their own sprite sets.
- Animation timer is a per-player elapsed accumulator: `self._anim_timer += dt; if self._anim_timer >= ANIM_INTERVAL: flip frame, reset timer`.

</specifics>

<deferred>
## Deferred Ideas

- CKentIntro.ico / GEvilIntro.ico — splash screen sprites; Phase 6 scope.
- SPose.ico / GPose.ico / GPose2.ico — pose sprites; Phase 4 scope (SCR-01/02 pose scoring).
- SSpin1–4 / GSpin1–4 — crash spin animation; Phase 4 scope.
- SDeath.ico / GDeath.ico — death sprites; Phase 4 scope.

</deferred>

---

*Phase: 2-Two-Characters-Move*
*Context gathered: 2026-05-16*
