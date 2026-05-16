# Requirements — Goblin vs. Superman (Python Port)

**Version:** v1
**Date:** 2026-05-16
**Source:** PROJECT.md + research synthesis + user scoping session

---

## v1 Requirements

### Core Engine

- [ ] **ENG-01**: Game runs at a fixed 60 FPS loop using `pygame.time.Clock` with delta-time (`dt = clock.tick(60) / 1000.0`)
- [ ] **ENG-02**: `GameState` enum controls active subsystems: `SPLASH`, `PLAYING`, `PAUSED`, `GAME_OVER`
- [ ] **ENG-03**: All game assets (PNG sprites, WAV sounds) loaded once at startup via `assets.py` into a keyed cache
- [ ] **ENG-04**: `settings.py` defines all geometry constants: `SCREEN_W = 1280`, `SCREEN_H = 800`, `SPRITE_SIZE = 128`, `WIN_SCORE = 50`, `BEAM_SPEED`, `FPS = 60`
- [ ] **ENG-05**: Dev-time asset conversion script converts all `.ico` sprites to `.png` (128×128, nearest-neighbor) and `.mid` music to `.wav` using FluidSynth

### Player Movement

- [ ] **MOV-01**: Superman moves with arrow keys — Up/Down/Left/Right update direction and position each frame
- [ ] **MOV-02**: Goblin moves with E (up) / D (down) / S (left) / F (right)
- [ ] **MOV-03**: All movement uses `pygame.key.get_pressed()` for smooth continuous input (not `KEYDOWN` events)
- [ ] **MOV-04**: Both characters wrap horizontally — exiting left edge reappears on right and vice versa
- [ ] **MOV-05**: Ground boundary — neither character can move below the green ground zone
- [ ] **MOV-06**: Ceiling boundary — neither character can move above the white ceiling zone
- [ ] **MOV-07**: `CharState` enum per player: `ALIVE`, `CRASHING`, `DEAD`, `POSING`, `RESPAWNING`
- [ ] **MOV-08**: Directional sprite frames swap each game tick to animate movement (2-frame alternation per direction)
- [ ] **MOV-09**: Superman sprite set covers: idle, right×2, left×2, up×2, down×2 (air), ground walking variants (Clark Kent), pose, death, spin×4
- [ ] **MOV-10**: Goblin sprite set covers: idle, right×2, left×2, up×2, down×2 (air), ground variants (GEvil), pose, death, spin×4

### Combat

- [ ] **CMB-01**: Superman shoots a laser beam when Shift is pressed (one-shot `KEYDOWN` event), fired in current movement direction
- [ ] **CMB-02**: Goblin shoots a laser beam when R is pressed, fired in current movement direction
- [ ] **CMB-03**: Beams travel axis-aligned (up, down, left, or right only); if character is idle/posing, beam fires in last known direction
- [ ] **CMB-04**: Superman beams render as red lines; Goblin beams render as green lines
- [ ] **CMB-05**: Each player supports up to 10 simultaneous active beams (ring buffer — oldest beam replaced when limit hit)
- [ ] **CMB-06**: Beams wrap horizontally and expire after 2 full wraps
- [ ] **CMB-07**: Beam collision detected per frame using `pygame.Rect.clipline()` against opponent's rect
- [ ] **CMB-08**: Collision direction check uses `if beam.direction in (LEFT, RIGHT):` — never `or RIGHT` alone (fixes VB6 Or-bug)

### Death & Respawn

- [ ] **DTH-01**: When a beam hits a living player, that player enters `CRASHING` state immediately
- [ ] **DTH-02**: Crashing player's movement is locked — no input accepted during `CRASHING`
- [ ] **DTH-03**: Crashing player rotates through spin sprites (SSpin1→4 / GSpin1→4) at 100 ms cadence while falling to ground
- [ ] **DTH-04**: When crashing player reaches the ground, they switch to death sprite and enter `DEAD` state
- [ ] **DTH-05**: Superman respawns with Enter key; Goblin respawns with W key — only processed in `DEAD` state
- [ ] **DTH-06**: Respawn places player at a random valid position (above ground, within bounds)
- [ ] **DTH-07**: Mouse-clicking a living character triggers their death (OmnipotentShootingGuy mechanic) and awards 1 point to the mouse player's score

### Scoring

- [ ] **SCR-01**: Holding the pose key while alive earns +1 to that player's raw pose score per game tick; displayed score is `raw / 10 + hit_bonus`
- [ ] **SCR-02**: Superman's pose key is Ctrl; Goblin's pose key is Space
- [ ] **SCR-03**: Landing a beam hit on a living opponent earns +10 to the shooter's displayed score
- [ ] **SCR-04**: Mouse-click kills increment the "OmnipotentShootingGuy" score by 1
- [ ] **SCR-05**: In-game HUD overlay displays all three scores in a fixed position during `PLAYING` state
- [ ] **SCR-06**: When any player's score reaches `WIN_SCORE (50)`, game transitions to `GAME_OVER` state

### Audio

- [ ] **AUD-01**: Laser WAV (`LASER.WAV`) plays when either player shoots
- [ ] **AUD-02**: DeathCry WAV (`DeathCry.WAV`) plays when a player is hit
- [ ] **AUD-03**: Explosion WAV (`EXPLODE.WAV`) plays when a crashing player hits the ground
- [ ] **AUD-04**: Background music (converted `passport.mid` → WAV) loops continuously during `PLAYING` state
- [ ] **AUD-05**: Intro music (converted `canyon.mid` → WAV) plays during `SPLASH` state
- [ ] **AUD-06**: M key toggles mute — silences all audio channels; pressing again restores

### UI & Screens

- [ ] **UI-01**: Splash screen displays "Hurdle's Mom Inc. Intl." title, "Presents:", and scrolls through all 25 original credits lines at 1500 ms cadence
- [ ] **UI-02**: Splash screen alternates between two character sprites (Goblin/Superman) at 750 ms cadence
- [ ] **UI-03**: Splash screen shows game controls text (Superman: arrows/Shift/Ctrl/Enter; Goblin: ESDF/R/Space/W)
- [ ] **UI-04**: Any key press or click dismisses the splash screen and starts a new game
- [ ] **UI-05**: P or Escape pauses the game — all timers/movement freeze; overlay indicates "PAUSED"
- [ ] **UI-06**: GAME_OVER screen displays final scores for all three players and prompts "F2 or Enter to restart"
- [ ] **UI-07**: F2 starts a new game from any state; Delete/Escape quits

### Packaging

- [ ] **PKG-01**: PyInstaller `--onedir --windowed` produces a Windows `.exe` with all assets bundled

---

## v2 Requirements (Deferred)

- Sprite sheet format (individual PNGs are fine for v1 at this sprite count)
- Configurable win score via command-line or in-game setting
- Sound effects stereo-panned by character position
- Fullscreen toggle
- Key rebinding

---

## Out of Scope

- Online/network multiplayer — local 2-player only
- AI/CPU opponent
- Settings UI screen — constants in `settings.py` are sufficient
- New gameplay mechanics or characters
- Persistent high scores / leaderboard
- macOS / Linux packaging (Windows focus for v1)

---

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| ENG-01 | Phase 1 | Pending |
| ENG-02 | Phase 1 | Pending |
| ENG-03 | Phase 1 | Pending |
| ENG-04 | Phase 1 | Pending |
| ENG-05 | Phase 1 | Pending |
| MOV-01 | Phase 2 | Pending |
| MOV-02 | Phase 2 | Pending |
| MOV-03 | Phase 2 | Pending |
| MOV-04 | Phase 2 | Pending |
| MOV-05 | Phase 2 | Pending |
| MOV-06 | Phase 2 | Pending |
| MOV-07 | Phase 2 | Pending |
| MOV-08 | Phase 2 | Pending |
| MOV-09 | Phase 2 | Pending |
| MOV-10 | Phase 2 | Pending |
| CMB-01 | Phase 3 | Pending |
| CMB-02 | Phase 3 | Pending |
| CMB-03 | Phase 3 | Pending |
| CMB-04 | Phase 3 | Pending |
| CMB-05 | Phase 3 | Pending |
| CMB-06 | Phase 3 | Pending |
| CMB-07 | Phase 3 | Pending |
| CMB-08 | Phase 3 | Pending |
| DTH-01 | Phase 4 | Pending |
| DTH-02 | Phase 4 | Pending |
| DTH-03 | Phase 4 | Pending |
| DTH-04 | Phase 4 | Pending |
| DTH-05 | Phase 4 | Pending |
| DTH-06 | Phase 4 | Pending |
| DTH-07 | Phase 4 | Pending |
| SCR-01 | Phase 4 | Pending |
| SCR-02 | Phase 4 | Pending |
| SCR-03 | Phase 4 | Pending |
| SCR-04 | Phase 4 | Pending |
| SCR-05 | Phase 4 | Pending |
| SCR-06 | Phase 4 | Pending |
| AUD-01 | Phase 5 | Pending |
| AUD-02 | Phase 5 | Pending |
| AUD-03 | Phase 5 | Pending |
| AUD-04 | Phase 5 | Pending |
| AUD-05 | Phase 5 | Pending |
| AUD-06 | Phase 5 | Pending |
| UI-01 | Phase 6 | Pending |
| UI-02 | Phase 6 | Pending |
| UI-03 | Phase 6 | Pending |
| UI-04 | Phase 6 | Pending |
| UI-05 | Phase 6 | Pending |
| UI-06 | Phase 6 | Pending |
| UI-07 | Phase 6 | Pending |
| PKG-01 | Phase 6 | Pending |
