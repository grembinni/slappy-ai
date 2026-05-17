# Phase 5: Audio - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Wire all audio so the game sounds like the original: laser fires, death cries, and explosion-on-landing play as SFX; background music (passport.wav) loops continuously during PLAYING state; intro music (canyon.wav) plays during SPLASH state; M key toggles global mute.

**Requirements in scope:** AUD-01, AUD-02, AUD-03, AUD-04, AUD-05, AUD-06
**Out of scope:** SPLASH screen implementation (Phase 6), GAME_OVER screen audio (Phase 6), stereo panning by character position (v2 backlog)

</domain>

<decisions>
## Implementation Decisions

### SoundManager Architecture (AUD-01 through AUD-06)
- **D-01:** All sound trigger call sites live in `game.py` — Player stays clean with no SoundManager reference. game.py already owns all the events (fire KEYDOWN, collision detection, state transitions) so no Player changes are needed.
- **D-02:** `SoundManager` (in `sound.py`) owns SFX playback + music playback + mute state — the single audio authority. game.py calls `self.snd.*` methods; it never touches `pygame.mixer` directly.
- **D-03:** `SoundManager` is instantiated inside `Game.__init__` as `self.snd = SoundManager(assets.sounds)`. main.py stays unchanged. Same pattern as `self._hud_font`.

### Music Backend (AUD-04, AUD-05)
- **D-04:** Background music and intro music use `pygame.mixer.music` (not `pygame.mixer.Sound`). Streaming backend, seamless looping, no mixer channel consumed. `pygame.mixer.music.play(-1)` for infinite loop.
- **D-05:** `SoundManager` derives music file paths from `pathlib.Path(__file__).parent / "assets" / "sounds"` — same pattern as `AssetCache`'s `ASSETS_DIR`. No path constants needed in `settings.py`.
- **D-06:** Named music methods: `play_playing_music()` (loads passport.wav, plays -1) and `play_splash_music()` (loads canyon.wav, plays -1). No generic `play_music(name)` string-key API.

### SFX Trigger Points in game.py
- **D-07:** `snd.play_laser()` → called in game.py's KEYDOWN block immediately after `player.fire(d)` for both Superman (K_KP0) and Goblin (K_e).
- **D-08:** `snd.play_death_cry()` → called in game.py's collision detection block immediately after `player.start_crash()`.
- **D-09:** `snd.play_explode()` → game.py detects CRASHING→DEAD transition by checking `was_crashing = player.state == CharState.CRASHING` before `player.update()`, then `if was_crashing and player.state == CharState.DEAD: snd.play_explode()`.

### Mute Behavior (AUD-06)
- **D-10:** Muting pauses mid-play SFX (`pygame.mixer.pause()`) and pauses music (`pygame.mixer.music.pause()`). In-flight sounds pause — they do not finish.
- **D-11:** Unmuting resumes SFX channels (`pygame.mixer.unpause()`) and resumes music from its paused position (`pygame.mixer.music.unpause()`). Music feels continuous, not restarted.
- **D-12:** `SoundManager.toggle_mute()` — single method; game.py calls it on `K_m` KEYDOWN. SoundManager maintains `self._muted: bool` flag and handles all pygame.mixer calls internally.

### AUD-05 Scope (Intro Music)
- **D-13:** `SoundManager.play_splash_music()` is fully implemented in Phase 5. game.py wires music to game state: on startup (PLAYING) call `snd.play_playing_music()`; Phase 6 will call `snd.play_splash_music()` when it sets the initial state to SPLASH. Phase 6 needs zero audio code for AUD-05.
- **D-14:** When `game.state` transitions to `GAME_OVER`, call `snd.stop_music()`. Music stops at the end of the match — Phase 6 can add GAME_OVER fanfare separately.

### Claude's Discretion
- `SoundManager.play_laser()`, `play_death_cry()`, `play_explode()` each call `self._sounds['laser'].play()` (etc.) with a mute guard: `if self._muted: return`. Sound object keys are lowercase stems matching AssetCache's loading convention.
- `intro.wav` exists in `assets/sounds/` but is not referenced in AUD-01 through AUD-06. Leave it unused in Phase 5.
- `SoundManager.stop_music()` calls `pygame.mixer.music.stop()` — used on GAME_OVER transition and any future state that needs silence.
- On `play_playing_music()` / `play_splash_music()`: call `pygame.mixer.music.stop()` first to cleanly switch tracks if one is already playing (prevents overlap on rapid state changes).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` §Audio (AUD-01–06) — exact Phase 5 deliverables
- `.planning/ROADMAP.md` §Phase 5 — success criteria; all 4 must pass

### Project Constraints (non-negotiable)
- `CLAUDE.md` — ALL key constraints: geometry in `settings.py`, `KEYDOWN` for one-shot actions, dt-scaling, no `pygame.sprite.Sprite`, `pygame.key.get_pressed()` for movement
- `.planning/PROJECT.md` §Constraints — port fidelity rules

### Existing Code (read before writing any Phase 5 code)
- `game.py` — `Game` class; Phase 5 adds `self.snd = SoundManager(assets.sounds)` in `__init__`; adds `snd.play_playing_music()` at startup; adds `K_m` KEYDOWN handler; adds `snd.play_laser()` + `snd.play_death_cry()` trigger calls; adds CRASHING→DEAD detection for `snd.play_explode()`; adds `snd.stop_music()` on GAME_OVER transition
- `assets.py` — `AssetCache.sounds` dict (keyed by lowercase WAV stem): `laser`, `deathcry`, `explode`, `passport`, `canyon`, `intro`. Phase 5 passes `assets.sounds` to `SoundManager`
- `main.py` — `pygame.mixer.init()` already called before `AssetCache()`. Phase 5 makes no changes here.
- `player.py` — Phase 5 makes NO changes to player.py. State transitions (CRASHING→DEAD) are read from outside, not modified.

### Prior Phase Context
- `.planning/phases/04-death-respawn-scoring/04-CONTEXT.md` — D-03/D-04: CRASHING state, GROUND_STOP_Y snap, DEAD state transition. Phase 5 reads player.state to detect this transition from game.py.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `AssetCache.sounds` dict — already loaded at startup; keys are lowercase WAV stems (`laser`, `deathcry`, `explode`, `passport`, `canyon`). SoundManager receives this dict and uses it for SFX.
- `CharState.CRASHING`, `CharState.DEAD` — already defined in player.py; game.py checks these before/after `player.update()` to detect CRASHING→DEAD transitions for explode SFX.
- `GameState.SPLASH`, `GameState.PLAYING`, `GameState.GAME_OVER` — already defined in game.py; Phase 5 maps PLAYING→passport music, GAME_OVER→stop music. SPLASH→canyon music wired now, fires when Phase 6 uses SPLASH state.

### Established Patterns
- `KEYDOWN` one-shot events in `game.py Game.run()` — M mute handler follows same pattern as beam fire (K_KP0 / K_e) and respawn (K_UP / K_w)
- `game.py` owns all event detection — no sound triggers in player.py, beam.py, or hud.py; keeps audio centralized in the same file that already detects collisions and fires
- `pathlib.Path(__file__).parent` pattern — already used in `assets.py`; SoundManager uses same idiom to locate `assets/sounds/passport.wav` and `assets/sounds/canyon.wav` for `pygame.mixer.music.load()`

### Integration Points
- `game.py Game.__init__`: add `from sound import SoundManager` import; add `self.snd = SoundManager(assets.sounds)`; add `self.snd.play_playing_music()`
- `game.py Game.run()` KEYDOWN block: add `elif event.key == pygame.K_m: self.snd.toggle_mute()`; add `self.snd.play_laser()` after each `player.fire(d)` call
- `game.py Game.update()` collision block: add `self.snd.play_death_cry()` after `player.start_crash()`
- `game.py Game.update()` or `Game.run()` loop: add CRASHING→DEAD detection; call `self.snd.play_explode()` when transition detected
- `game.py Game.update()` win condition block: add `self.snd.stop_music()` when `self.state = GameState.GAME_OVER`
- New module: `sound.py` — `SoundManager` class with `__init__(sounds)`, `play_laser()`, `play_death_cry()`, `play_explode()`, `play_playing_music()`, `play_splash_music()`, `stop_music()`, `toggle_mute()`

</code_context>

<specifics>
## Specific Ideas

- Mute is a hard pause (not volume-zero): in-flight sounds freeze mid-play; music resumes from exact position. This preserves the feel of a proper mute toggle rather than a fade.
- SoundManager is instantiated in Game, not main.py — keeps main.py at 15 lines.
- play_splash_music() is fully implemented now so Phase 6 can call it with zero audio work.

</specifics>

<deferred>
## Deferred Ideas

- Stereo panning of SFX by character position — v2 backlog (REQUIREMENTS.md §v2)
- GAME_OVER fanfare / jingle — Phase 6 scope
- intro.wav usage — file exists in assets/sounds/ but has no corresponding AUD requirement; defer to post-v1 or discard
- Volume sliders or per-channel volume control — out of scope for v1

</deferred>

---

*Phase: 5-Audio*
*Context gathered: 2026-05-16*
