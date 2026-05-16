# Roadmap — Goblin vs. Superman (Python Port)

## Overview

6 phases | 50 requirements | Vertical MVP

Each phase delivers a playable or demonstrable increment. Phase 1 gets the window open with
real assets on screen. By Phase 4 a full match plays to completion. Phases 5–6 add audio
polish and make the game shippable.

---

## Phases

- [x] **Phase 1: Foundation** — Asset pipeline, settings, game loop skeleton, background renders in window
- [x] **Phase 2: Two Characters Move** — Both characters appear, move with keyboard, wrap, respect ground/ceiling
- [ ] **Phase 3: Combat** — Beams fire, travel, wrap, and hit detection triggers CRASHING state
- [ ] **Phase 4: Death, Respawn & Scoring** — Crash animation, DEAD state, respawn keys, HUD scores, win condition
- [ ] **Phase 5: Audio** — All WAVs play on correct events, background music loops, M mutes
- [ ] **Phase 6: Screens & Packaging** — Splash/credits, pause, GAME_OVER screen, mouse-click mechanic, PyInstaller .exe

---

## Phase Details

### Phase 1: Foundation
**Goal:** The window opens at 1280x800, displays the background, loads all assets without error, and closes cleanly.
**Mode:** mvp
**Depends on:** Nothing
**Requirements:** ENG-01, ENG-02, ENG-03, ENG-04, ENG-05
**Success Criteria:**
1. Running `python main.py` opens a 1280x800 window titled "Goblin vs. Superman" without crashing
2. The green ground zone and white ceiling zone are visible against the background
3. All PNG sprites and WAV files exist in the `assets/` folder (conversion script ran without errors)
4. Closing the window (X button or Delete key) exits cleanly with no traceback
5. `settings.py` constants (`SCREEN_W`, `SCREEN_H`, `SPRITE_SIZE`, `WIN_SCORE`, `BEAM_SPEED`, `FPS`) are importable and correct
**Plans:** 5 plans

Plans:
**Wave 1** (parallel):
- [x] 01-01-PLAN.md — Project scaffold: settings.py constants, requirements.txt, .gitignore, pytest.ini
- [x] 01-02-PLAN.md — Test scaffold: conftest.py, test_settings.py, test_convert.py
- [x] 01-03-PLAN.md — raw_assets/ population: create directory structure and human copies 46 source files

**Wave 2** *(blocked on Wave 1 completion — FluidSynth install checkpoint required)*:
- [x] 01-04-PLAN.md — convert_assets.py: ICO→PNG + MIDI→WAV pipeline with --dry-run, --skip-midi, --soundfont

**Wave 3** *(blocked on Wave 2 completion)*:
- [x] 01-05-PLAN.md — Walking skeleton: main.py, game.py, assets.py, test_assets.py

**Cross-cutting constraints:** All geometry/color constants flow only through settings.py; assets/ directory is gitignored (generated output); `dt = clock.tick(FPS) / 1000.0` established in game.py in Wave 3.

### Phase 2: Two Characters Move
**Goal:** Two players can simultaneously control their characters on the same keyboard, moving freely within boundaries.
**Mode:** mvp
**Depends on:** Phase 1
**Requirements:** MOV-01, MOV-02, MOV-03, MOV-04, MOV-05, MOV-06, MOV-07, MOV-08, MOV-09, MOV-10
**Success Criteria:**
1. Superman moves smoothly in all four directions using arrow keys while Goblin moves simultaneously using ESDF — no input blocking between the two
2. Both characters animate with direction-appropriate sprite frames that alternate each game tick
3. Either character exiting the left edge reappears on the right edge (and vice versa) in the same frame
4. Neither character can move below the green ground zone or above the white ceiling zone
5. The `CharState` enum is active per player and each character starts in `ALIVE` state
**Plans:** 4 plans

Plans:
**Wave 1:**
- [x] 02-01-PLAN.md — settings.py: add PLAYER_SPEED_UP, PLAYER_SPEED_H, PLAYER_SPEED_DOWN, ANIM_INTERVAL

**Wave 2** *(blocked on Wave 1)*:
- [x] 02-02-PLAN.md — player.py: CharState enum + Player class (movement, animation, wrap, boundaries)

**Wave 3** *(parallel, blocked on Wave 2)*:
- [x] 02-03-PLAN.md — game.py: wire two Player instances into update/draw
- [x] 02-04-PLAN.md — test_player.py: unit tests for all MOV-01 through MOV-10

### Phase 3: Combat
**Goal:** Players can shoot laser beams that travel across the screen, wrap, and kill the opponent on contact.
**Mode:** mvp
**Depends on:** Phase 2
**Requirements:** CMB-01, CMB-02, CMB-03, CMB-04, CMB-05, CMB-06, CMB-07, CMB-08
**Success Criteria:**
1. Pressing Shift (Superman) or R (Goblin) fires a beam in the character's current facing direction — or last known direction if idle
2. Superman's beams render red; Goblin's beams render green; both travel at `BEAM_SPEED` per second
3. A beam that exits the right edge reappears on the left edge (and vice versa); beams expire after 2 full wraps
4. When a beam's line segment intersects the opponent's rect, the opponent immediately enters `CRASHING` state
5. The collision direction check uses `beam.direction in (LEFT, RIGHT)` — not `== LEFT or RIGHT` — confirming the VB6 Or-bug is fixed
**Plans:** TBD

### Phase 4: Death, Respawn & Scoring
**Goal:** A complete match plays from first shot to game-over — crash animation, death, respawn, scores accumulate, and the game ends at 50 points.
**Mode:** mvp
**Depends on:** Phase 3
**Requirements:** DTH-01, DTH-02, DTH-03, DTH-04, DTH-05, DTH-06, SCR-01, SCR-02, SCR-03, SCR-04, SCR-05, SCR-06, DTH-07
**Success Criteria:**
1. A hit player spins through their spin sprites while falling to the ground, then switches to the death sprite — input is locked throughout
2. After reaching the ground, pressing Enter (Superman) or W (Goblin) respawns that character at a random valid position above the ground
3. Holding Ctrl (Superman) or Space (Goblin) while alive accumulates pose score each tick; landing a beam hit adds +10 to the shooter's score
4. All three scores (Superman, Goblin, OmnipotentShootingGuy) are visible in the in-game HUD overlay during play
5. When any score reaches 50, the game transitions to `GAME_OVER` state and normal play stops
**Plans:** TBD

### Phase 5: Audio
**Goal:** The game sounds like the original — every action has its sound, background music loops, and M mutes everything.
**Mode:** mvp
**Depends on:** Phase 4
**Requirements:** AUD-01, AUD-02, AUD-03, AUD-04, AUD-05, AUD-06
**Success Criteria:**
1. Firing a beam plays `LASER.WAV`; being hit plays `DeathCry.WAV`; hitting the ground during a crash plays `EXPLODE.WAV`
2. Background music (converted `passport.mid` → WAV) loops continuously while in `PLAYING` state without audible gaps
3. Intro music (converted `canyon.mid` → WAV) plays during `SPLASH` state
4. Pressing M silences all audio channels immediately; pressing M again restores all audio at previous levels
**Plans:** TBD

### Phase 6: Screens & Packaging
**Goal:** The game is shippable — it has a splash/credits screen, pause, a proper game-over screen, the secret mouse mechanic, and a standalone Windows .exe.
**Mode:** mvp
**Depends on:** Phase 5
**Requirements:** UI-01, UI-02, UI-03, UI-04, UI-05, UI-06, UI-07, PKG-01
**Success Criteria:**
1. On launch, the splash screen scrolls all 25 original credits lines at 1500 ms cadence and alternates character sprites at 750 ms cadence — any key or click starts the game
2. Pressing P or Escape during play freezes all movement and displays a "PAUSED" overlay; pressing again resumes
3. The GAME_OVER screen shows final scores for all three players and the prompt "F2 or Enter to restart"; F2 starts a new game from any screen
4. Clicking on a living character kills them and increments the OmnipotentShootingGuy score
5. `pyinstaller --onedir --windowed` produces a `dist/` folder with a runnable `.exe` that bundles all assets — game launches on a machine without Python installed
**Plans:** TBD
**UI hint**: yes

---

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 5/5 | Complete | 2026-05-16 |
| 2. Two Characters Move | 4/4 | Complete | 2026-05-16 |
| 3. Combat | 0/? | Not started | - |
| 4. Death, Respawn & Scoring | 0/? | Not started | - |
| 5. Audio | 0/? | Not started | - |
| 6. Screens & Packaging | 0/? | Not started | - |
