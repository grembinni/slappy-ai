# Phase 6: Screens & Packaging - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Make the game shippable: implement the full state machine (SPLASH → PLAYING → PAUSED → GAME_OVER), build each screen's rendering and input handling, add a win score selector on the splash screen, and produce a standalone Windows .exe via PyInstaller.

**Requirements in scope:** UI-01, UI-02, UI-03, UI-04, UI-05, UI-06, UI-07, PKG-01 — plus win-score input (folded from v2 backlog per user decision)
**Out of scope:** Sprite sheet migration, key rebinding, macOS/Linux packaging, online multiplayer, AI opponent

</domain>

<decisions>
## Implementation Decisions

### Pause Mechanic (UI-05)
- **D-01:** P and Escape both toggle pause, but ONLY when `game.state == GameState.PLAYING`. No effect from SPLASH or GAME_OVER.
- **D-02:** Delete is the only hard quit key. Escape does NOT quit — it only pauses.
- **D-03:** When entering PAUSED: call `snd.pause_game()` to freeze audio. When resuming: call `snd.resume_game()`. These are SEPARATE from `toggle_mute()` so that mute state is preserved across pauses. `SoundManager` needs two new methods: `pause_game()` (pygame.mixer.pause() + music.pause(), without touching `_muted`) and `resume_game()` (pygame.mixer.unpause() + music.unpause(), without touching `_muted`).

### Splash Screen (UI-01, UI-02, UI-03, UI-04)
- **D-04:** All 25 credits lines are hardcoded verbatim from the VB6 source (Form1.frm, strarrCredits[1..25]). Lines as extracted:
  1. "President: Senior Airman"
  2. "CEO: Senior Airman"
  3. "CFO: Senior Airman"
  4. "Board of Directors: Senior Airman"
  5. "Lead Designer: Airman Hurdle"
  6. "Lead Artist: Airman Hurdle"
  7. "Lead Programmer: Airman Hurdle"
  8. "Lead Level Designer: Airman Hurdle"
  9. "Senior Assistant Designer: Senior Airman"
  10. "Senior Hardware Administrator: Airman Jarvis"
  11. "Senior Assistant Artist: Airman Hurdle"
  12. "Senior Assistant Programmer: Airman Hurdle"
  13. "Senior Assistant Level Designer: Airman Hurdle"
  14. "Junior Assistant Designer: Airman Basic Parrott"
  15. "Junior Assistant Artist: Airman Basic Kollars"
  16. "Junior Assistant Programmer: Airman Basic Anderson"
  17. "Junior Assistant Level Designer: Airman Basic Kollars"
  18. "Junior Code Realigner: Airman Basic Barney"
  19. "Software Design Style Consultant: Airman Basic Christen"
  20. "Secondary Motivator: Staff Sergeant Drennen"
  21. "Best Boy Grip: Airman Basic Zernicke"
  22. "Token Retard: Airman Carlson"
  23. "Token Cuban A1C: Airman First Class Magby"
  24. ""  (blank)
  25. "Special Thanks To Hurdle's Mom"
- **D-05:** Sprite cycling: pick randomly from ALL available character sprites in `assets/sprites/` every 750ms — matches VB6 Timer2 behavior (not just 2 alternating sprites as written in REQUIREMENTS).
- **D-06:** Splash background color: dark navy blue `(0, 0, 64)` — matches VB6 `BackColor = &H00400000&` (OLE format AABBGGRR → B=0x40=64, G=0, R=0).
- **D-07:** Layout (adapted from VB6 Form1):
  - Top: "Hurdle's Mom Inc. Intl." title with 2px dark offset shadow (two labels, same as VB6)
  - Second row: "Presents:" and "A Hurdle's Mom Inc. Intl. production" side by side
  - Center: randomized character sprite (large, centered vertically in remaining space)
  - Scrolling credits text in the lower-center area (above controls)
  - Bottom: win score selector ("Win Score: 50", Up/Down to adjust)
  - Very bottom: controls reference text, fixed position
- **D-08:** Controls text layout (UI-03): fixed at bottom of screen — "Superman: ↑↓←→ / Shift / Ctrl / Enter  |  Goblin: ESDF / R / Space / W"
- **D-09:** Dismiss: any key press OR mouse click starts the game with the current win score (UI-04). Exception: Up/Down arrow keys adjust win score rather than dismissing.

### Win Score Input (folded from v2 backlog)
- **D-10:** Win score selector is displayed on the splash screen. Format: "Win Score: 50" (or current value).
- **D-11:** Up arrow key increments win score by 10 (max 500). Down arrow key decrements by 10 (min 10). Default is 50.
- **D-12:** `WIN_SCORE` in settings.py remains as the default constant (50). The splash returns the selected `win_score: int` to `main.py`, which passes it to `Game.__init__(screen, assets, win_score)`. Game stores it as `self.win_score` and uses it in the win condition check instead of the settings constant.

### Restart Mechanic (UI-06, UI-07)
- **D-13:** "Restart" means full `Game` reinit — `main.py` creates a new `Game` object. All state (players, beams, scores, osg_score, audio) resets cleanly. No in-place state reset.
- **D-14:** After restart, game returns to SPLASH state (not straight to PLAYING). Intro music plays again. User sees the splash and selects a new win score.
- **D-15:** F2 and Enter restart ONLY from `GAME_OVER` state. Not from SPLASH, PLAYING, or PAUSED.
- **D-16:** Implementation: `game.run()` returns a sentinel (e.g., `"restart"`) when F2/Enter pressed in GAME_OVER. `main.py` loops: `while True: result = game.run(); if result != "restart": break`. New Game created at top of loop.

### GAME_OVER Screen (UI-06)
- **D-17:** Black background (fill screen with `(0, 0, 0)`).
- **D-18:** Text displayed: final scores for all three players ("Superman: N", "Goblin: N", "OmnipotentShootingGuy: N") and the prompt "F2 or Enter to restart". OmnipotentShootingGuy line hidden when score is 0 (consistent with HUD behavior from Phase 4).
- **D-19:** No "winner callout" — scores only. Player can infer the winner from scores.
- **D-20:** GAME_OVER rendering lives in `game.py` `draw()` method, in the GAME_OVER branch. No new module needed — it's just a few text blits on black.

### Module Structure
- **D-21:** New `splash.py` module — `SplashScreen` class or `run_splash(screen, assets) -> int` function that handles the splash loop and returns the selected `win_score`. Follows the `hud.py` / `sound.py` extraction pattern.
- **D-22:** `game.py` GameState enum already has SPLASH, PLAYING, PAUSED, GAME_OVER — no additions needed.
- **D-23:** `main.py` orchestrates: `win_score = run_splash(screen, assets)` → `game = Game(screen, assets, win_score)` → `result = game.run()` → loop on restart.

### Claude's Discretion
- Splash sprite pool: use all PNGs in `assets/sprites/` (same keyed cache as AssetCache). Random pick each 750ms — accumulate a list of surfaces from AssetCache at splash init.
- PAUSED overlay: render a semi-transparent dark rect over the game frame (or just the word "PAUSED" centered in large font on the current frame). Keep it simple — one centered text label is sufficient.
- Font sizes: title uses a larger font (size 48–72); credits use the same size 28 as HUD; controls text uses size 20.
- `snd.play_splash_music()` already implemented in Phase 5 — call it at the start of splash.
- When GAME_OVER, music was already stopped in Phase 5 — no extra audio call needed at GAME_OVER screen entry.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` §UI & Screens (UI-01–07) and §Packaging (PKG-01) — exact Phase 6 deliverables
- `.planning/ROADMAP.md` §Phase 6 — success criteria; all 5 must pass

### Project Constraints (non-negotiable)
- `CLAUDE.md` — ALL key constraints: geometry in `settings.py`, `KEYDOWN` for one-shot actions, dt-scaling, no `pygame.sprite.Sprite`, `pygame.key.get_pressed()` for movement
- `.planning/PROJECT.md` §Constraints — port fidelity rules

### VB6 Source (credits content reference)
- `D:\dev\repo\best-game-ever\_old\Form1.frm` — VB6 splash form: exact credits text (strarrCredits[1..25]), Timer1=1500ms credits cycle, Timer2=750ms sprite cycle, BackColor, Label layout. **Read this before implementing splash.py.**

### Existing Code (read before writing any Phase 6 code)
- `game.py` — `Game` class + `GameState` enum (SPLASH, PLAYING, PAUSED, GAME_OVER already defined); `Game.__init__` (Phase 6 adds `win_score` param); `Game.run()` (Phase 6 adds PAUSED handling, GAME_OVER input, restart return value); `Game.draw()` (Phase 6 adds PAUSED overlay, GAME_OVER screen)
- `main.py` — startup sequence (Phase 6 wraps in restart loop: splash → game → loop)
- `sound.py` — `SoundManager` (Phase 6 adds `pause_game()` and `resume_game()` methods); `play_splash_music()` already implemented
- `settings.py` — `WIN_SCORE = 50` (default; Phase 6 makes this a runtime variable passed via Game constructor)
- `hud.py` — `draw_hud()` pattern (reference for how to extract screen rendering to a module)
- `assets.py` — `AssetCache` (splash.py reads `assets.sprites` dict for the random sprite pool)

### Prior Phase Context
- `.planning/phases/05-audio/05-CONTEXT.md` — D-13: `play_splash_music()` is fully implemented; Phase 6 calls it at SPLASH entry. D-14: `stop_music()` already fires on GAME_OVER transition.
- `.planning/phases/04-death-respawn-scoring/04-CONTEXT.md` — D-17: OmnipotentShootingGuy score hidden in HUD when 0; apply same logic to GAME_OVER screen.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `GameState` enum in `game.py` — SPLASH, PLAYING, PAUSED, GAME_OVER already defined; Phase 6 activates all four branches
- `SoundManager.play_splash_music()` — already implemented in Phase 5; no audio work for splash in Phase 6
- `AssetCache.sprites` dict — all character PNGs loaded; splash picks randomly from these surfaces for sprite cycling
- `draw_hud()` in `hud.py` — reference pattern for standalone drawing function with `(screen, data, font)` signature

### Established Patterns
- Module extraction: `hud.py` and `sound.py` show the pattern — `splash.py` follows the same
- `KEYDOWN` one-shot events in `game.py Game.run()` — P/Escape pause, F2/Enter restart, Delete quit all follow this pattern
- Return value from `run()`: `game.run()` currently returns `None` implicitly; Phase 6 changes it to return `"restart"` or `None` for `main.py` to detect
- `clock.tick(FPS) / 1000.0` loop — PAUSED state still needs to tick the clock (to keep the loop alive), but skips `self.update(dt)` calls

### Integration Points
- `main.py`: wrap `Game` construction + `game.run()` in a `while True` restart loop; add `run_splash()` call before `Game()` to get `win_score`
- `game.py Game.__init__`: add `win_score: int` parameter; store as `self.win_score`; use `self.win_score` in win condition check (replaces `WIN_SCORE` import)
- `game.py Game.run()`: add `GameState.PAUSED` branch that renders pause overlay and skips updates; add F2/Enter handler in GAME_OVER; add return `"restart"` on F2/Enter
- `game.py Game.draw()`: add GAME_OVER branch (black fill + score text + prompt); add PAUSED overlay (semi-transparent or text label)
- `sound.py SoundManager`: add `pause_game()` and `resume_game()` methods

</code_context>

<specifics>
## Specific Ideas

- The original VB6 splash (Form1.frm) uses two overlapping label controls for the title shadow effect (Label1 at position X, Label2 at X-10 offset). The Python version should replicate this with two blit calls for the title: one navy/dark and one white, offset by (2, 2)px.
- The VB6 sprite cycling (Timer2) picks from a pool of 17 specific sprites including Clark Kent, GEvil, pose, death, and spin variants. In Python we can just random-pick from `assets.sprites.values()` (or a curated subset of that dict).
- The win score display ("Win Score: 50") should be prominently placed above the controls text so it's visible when the player is deciding. Up/Down arrows adjust it; any other key/click starts the game.
- Keep `main.py` at ~20 lines — this is important to the project style. All logic goes in `splash.py` and `game.py`, not in `main.py`.

</specifics>

<deferred>
## Deferred Ideas

- GAME_OVER fanfare / jingle — out of scope for v1 (was already deferred in Phase 5)
- Fullscreen toggle — v2 backlog (REQUIREMENTS.md §v2)
- Key rebinding — v2 backlog
- macOS/Linux packaging — out of scope (REQUIREMENTS.md §Out of Scope)
- Winner callout ("Superman Wins!") on GAME_OVER screen — user chose scores-only

</deferred>

---

*Phase: 6-Screens-Packaging*
*Context gathered: 2026-05-16*
