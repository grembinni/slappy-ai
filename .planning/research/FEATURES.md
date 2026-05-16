# Feature Landscape

**Domain:** 2-player local-multiplayer arcade brawler (Python/pygame port)
**Project:** Goblin vs. Superman
**Researched:** 2026-05-16
**Confidence:** MEDIUM — patterns are stable and well-understood in the pygame community; web search was unavailable for verification, so findings rely on established pygame conventions and training knowledge current through August 2025.

---

## Framing: Port vs. Rewrite Tension

The project mandate is explicit: same core gameplay, same controls, same scoring — lightly modernized, not reimagined. Every feature decision must be weighed against that constraint. "Table stakes" here means "a 2025 Python/pygame game that omits this feels broken or unfinished." "Anti-features" are improvements that would drift the game away from being a faithful port.

---

## Table Stakes

Features that a 2025 pygame port must have to feel complete and non-broken. Missing any of these and the game feels like an unfinished prototype regardless of how faithful the core mechanics are.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| In-game HUD score display | Window title bar scores are invisible during play; players cannot see the score without alt-tabbing or squinting at the frame border. Every arcade game since the 1980s renders scores on screen. | Low | Render score text with `pygame.font` at top of play area. Retains OmnipotentShootingGuy slot. |
| Explicit game states (at minimum: SPLASH, PLAYING, GAME_OVER) | Without state separation, input handling and rendering logic tangle into a single loop with boolean flags, causing bugs when adding any new behavior (pause, death screen, etc.). | Low–Med | A simple `enum` + `current_state` variable + per-state `handle_event / update / draw` dispatch is sufficient. No framework needed. |
| Pause state (P or Escape to pause) | Players on the same keyboard will accidentally bump keys, need bathroom breaks, or want to show someone the game. Absence of pause feels like a missing basic feature in 2025. | Low | Freeze update loop; overlay "PAUSED" text. No menu needed. |
| Clean GAME_OVER screen | The original VB6 game presumably ends abruptly or stays in a running state. A clear "Game Over" screen with final scores and a prompt to press F2 / Enter to play again closes the gameplay loop properly. | Low | Display final scores, winner announcement if win conditions added, and restart prompt. |
| Delta-time or fixed-rate frame update | VB6 used a timer control that fires at a fixed interval. pygame's game loop runs as fast as the CPU allows unless capped. Without `clock.tick(FPS)` capping, the game will run at wildly different speeds on different machines. | Low | `pygame.time.Clock.tick(60)` is one line. Required for cross-machine consistency. |
| Keyboard event handling via event queue | VB6 keyboard handling is event-driven per keypress. pygame's `pygame.key.get_pressed()` is the correct equivalent for held-key movement; `KEYDOWN` events handle single-press actions (shoot, pose, respawn). Mixing these incorrectly causes stuck inputs. | Low | Standard pattern; no library needed. |
| Graceful window close (quit event) | Clicking the X button must cleanly exit. VB6 handles this automatically; pygame requires explicit `pygame.QUIT` event handling or the window becomes unresponsive. | Low | One event check in the main loop. |
| Sound on/off toggle or volume control | WAV audio must be mute-able without closing the game. If music or SFX are obnoxious (and in a chaotic brawler they often are), players need an escape that isn't quitting. | Low | `pygame.mixer.music.set_volume(0)` toggled by a key (M). No settings screen needed. |
| Consistent asset loading with error messages | If a sprite or WAV file is missing, pygame raises an exception that prints nothing useful to a non-developer. A port being shared with others (even just family) should fail gracefully with a clear message. | Low | Wrap `pygame.image.load` / `pygame.mixer.Sound` in try/except with descriptive output. |

---

## Differentiators

Features that would make this port better than the original without compromising faithfulness. These are improvements, not new mechanics.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Win condition (first to N points) | The original has no defined end state — the game runs forever. A configurable target score (e.g. first to 50) gives sessions a natural conclusion and makes the OmnipotentShootingGuy score meaningful as a spoiler mechanic. Preserves the original feel while adding closure. | Low | Configurable constant `WIN_SCORE = 50`. Trigger GAME_OVER state when any score reaches it. |
| Hit flash / screen shake on death | Visual feedback when a laser connects is missing in most VB6-era games. A one-frame white flash on the hit character (not full-screen) communicates the kill clearly and adds impact without changing mechanics. | Low | Draw a white rect over the character sprite for 1–2 frames on death event. |
| Upscaled sprite rendering with nearest-neighbor scaling | Tiny 32x32 ICOs look blurry or incorrectly scaled at modern resolutions. `pygame.transform.scale` with the default filter gives blocky pixel-art look which is appropriate for this genre. Nearest-neighbor is the correct choice; bilinear is wrong for pixel art. | Low–Med | Load sprite at original size; scale up with `pygame.transform.scale` (not `smoothscale`). Done once at load time, not per frame. |
| Configurable FPS cap | The original VB6 timer interval implicitly defined game speed. A `TARGET_FPS = 60` constant at the top of the main file makes it easy to tune feel without hunting through the code. | Low | One constant. |
| Death sound positioned in stereo | When a player on the left side of the screen dies, panning the explosion slightly left adds spatial feedback. pygame mixer supports basic panning. | Low | Optional enhancement; skip if it complicates the audio system. |
| Sprite sheet support for animations | Loading individual frame files (one PNG per frame) is fine for small sprite counts, but a sprite sheet (all frames in one image, sliced by rect) reduces file I/O and is the standard pattern for pygame animation. | Med | Implement a simple `SpriteSheet` class with `get_image(row, col, width, height)`. Worth doing up front if redrawing sprites anyway. |
| Credits/splash screen with scrolling text | PROJECT.md explicitly requires this ("Hurdle's Mom Inc. Intl." credits). It is a differentiator from a bare-bones port because it gives the game personality and respects the original's charm. | Low–Med | Scroll a surface upward at a fixed pixel rate; transition to PLAYING state on any key. |

---

## Anti-Features

Things to deliberately NOT add. Each one would expand scope, add complexity, or drift the game away from being a faithful port.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Settings/config screen or menu | A menu system (resolution, key rebinding, volume sliders) is a significant UI project that adds no gameplay value. This game is meant to be launched and played immediately. | Put configurable values (FPS, win score, volume) as constants in a `config.py` file. Developers edit it; players don't need to. |
| Key rebinding UI | The original has fixed controls and they are part of the game's identity. Rebinding adds a menu system, persistence (config file write), and complexity for zero gameplay gain. | Document controls on the splash screen. Done. |
| Fullscreen toggle | PROJECT.md explicitly lists this as Out of Scope. A fixed resolution is simpler and the game was designed for a windowed experience. | Keep fixed window size (e.g. 800x600 or 1024x768 scaled from original). |
| Online/network multiplayer | Out of Scope per PROJECT.md. Would require a networking library (enet, twisted, or websockets), lag compensation, and state synchronization — a complete rewrite of the game model. | Local keyboard sharing only. |
| AI/CPU opponent | Out of Scope per PROJECT.md. This game's identity is two humans on one keyboard. An AI would require behavior design that doesn't exist in the original. | Two human players only. |
| Save/load or persistent high scores | There is no win condition in the original, so persistent scores have no context. Adding a leaderboard changes the game's social dynamic. | Scores reset on F2. No file I/O for scores. |
| Achievement system | Scope creep. Completely foreign to the original experience. | — |
| Multiple game modes | Same reason. The original has one mode. | — |
| New characters or stages | This is a port. Adding characters is game design, not porting. | Preserve Goblin and Superman only. |

---

## Feature Dependencies

```
SPLASH state → PLAYING state → GAME_OVER state
                    |
                PAUSE state (overlay, returns to PLAYING)

Score display (HUD) requires: font loading, score state
Win condition requires: score tracking + GAME_OVER trigger
Hit flash requires: death event detection (already needed for crash animation)
Sprite sheet requires: redrawing sprites as PNGs (already required for upscaling)
```

---

## Specific Questions Answered

### Game State Management

**Recommended approach:** A single `GameState` enum with values `SPLASH`, `PLAYING`, `PAUSED`, `GAME_OVER`. The main loop reads `current_state` and dispatches to per-state `handle_events()`, `update()`, and `draw()` methods or functions. No framework needed — this is 50–80 lines of Python.

Avoid: a single monolithic loop with `if playing and not paused and not game_over` boolean spaghetti. This is the #1 structural mistake in beginner pygame projects and becomes unmaintainable fast.

### Score Display

**Recommendation:** Move scores to an in-game HUD immediately. The window title bar approach is invisible during play, not accessible on windowed fullscreen, and unavailable if the game ever goes borderless. Render three score values at the top of the screen using a pixel/arcade-style font (e.g. the free "Press Start 2P" TTF, or pygame's built-in font). Keep the OmnipotentShootingGuy score in the HUD — it adds mystery for players who don't know the mechanic.

Confidence: HIGH — this is unambiguous; title bar scores are a known limitation of the original.

### Win Conditions

**Recommendation:** Add a first-to-N win condition, configurable via a constant (`WIN_SCORE = 50` is a reasonable default for a chaotic brawler). This is the single highest-value improvement over the original that does not alter mechanics. It gives sessions a natural end, makes F2 meaningful as "rematch," and lets the OmnipotentShootingGuy score matter as a spoiler that can steal a win.

Faithfulness concern: Adding a win condition changes the game from "chaotic infinite sandbox" to "match-based brawler." Set `WIN_SCORE = 0` (disabled) if the original feel is preferred — make it opt-in via the config constant.

### Player Feedback

**Recommendation:** Add only a hit flash (1–2 frame white overlay on the dying character). Skip screen shake — it adds motion that wasn't in the original and can feel wrong. The existing crash/spin animation already communicates death clearly; the flash adds a kill-confirmation frame that reads well at the moment of impact.

### Settings/Config

**Recommendation:** A `config.py` file with module-level constants. No settings screen. Values:
- `TARGET_FPS = 60`
- `WIN_SCORE = 50` (0 to disable)
- `MUSIC_VOLUME = 0.7`
- `SFX_VOLUME = 1.0`
- `WINDOW_WIDTH = 800`, `WINDOW_HEIGHT = 600`

### Asset Loading

**Recommendation:** Individual PNG files per animation frame is fine for this project's sprite count (8 directions × ~3 characters × ~4 animation states = ~96 frames maximum). A sprite sheet is worth implementing if redrawing sprites, because it is the industry standard pattern and makes adding frames trivial. If reusing upscaled ICOs directly, individual file loading is simpler and equally correct for this scale.

---

## MVP Recommendation

For a faithful, polished port, prioritize in order:

1. Delta-time frame capping (`clock.tick(60)`) — prevents cross-machine speed variance
2. Game state enum (SPLASH, PLAYING, PAUSED, GAME_OVER) — structural foundation
3. In-game HUD score display — replaces invisible title bar scores
4. Graceful quit and keyboard event handling — basic correctness
5. Splash/credits screen — explicitly required by PROJECT.md
6. Pause state — expected by any 2025 player
7. GAME_OVER screen with restart prompt — closes the gameplay loop
8. Hit flash on death — low effort, high impact feedback
9. Win condition constant — off by default, easy to enable

Defer unless explicitly requested:
- Sprite sheet class (individual PNGs are fine for this scale)
- Stereo-panned death sounds
- Any settings UI

---

## Sources

- PROJECT.md (d:/dev/repo/slappy-ai/.planning/PROJECT.md) — authoritative on scope, mechanics, and explicit Out of Scope items
- pygame documentation (training knowledge, current through August 2025) — `pygame.time.Clock`, `pygame.font`, `pygame.mixer`, `pygame.key.get_pressed` vs `KEYDOWN` event patterns
- General arcade/brawler game state conventions — HIGH confidence, stable patterns unchanged since pygame 1.9+
- Web search unavailable in this session — findings relying on external sources are noted as MEDIUM confidence
