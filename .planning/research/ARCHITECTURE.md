# Architecture Patterns

**Project:** Goblin vs. Superman (Python/pygame port)
**Researched:** 2026-05-16
**Source analyzed:** `frmSuperman.frm` (VB6 main game form), `Form1.frm` (VB6 intro form)

---

## VB6 Original: What It Actually Does

Before prescribing an architecture, it is worth being precise about what the original does, because the pygame port maps directly to it.

The VB6 game has two forms:

**Form1** (intro / credits screen)
- `Timer1` (1500 ms): scrolls `strarrCredits[]` through a Label
- `Timer2` (750 ms): randomly picks a sprite icon and shows it in `Image1`
- Click anywhere or click the image to dismiss and launch the game form

**frmForm** (gameplay)
- `tmrIntro` (150 ms): alternates between two character images while the intro instructions panel is visible
- `tmrSMove` (75 ms): moves Superman — updates position, wraps, tracks score, calls `SPose()` for sprite selection
- `tmrGMove` (75 ms): same for Goblin — independent timer, same logic
- `tmrSCrash` (100 ms): drives Superman's spinning fall-to-ground death animation
- `tmrGCrash` (100 ms): same for Goblin
- `tmrAttack` (5 ms): calls `DrawSLines()` and `DrawGLines()` every 5 ms — this is the laser beam draw loop

Movement state is a single byte (`bytSDir`, `bytGDir`) storing the last-pressed direction (1=up, 2=down, 3=left, 4=right, 5=pose, 6=idle). Velocity (`intSXInc`, `intSYInc`) is recomputed each timer tick from that state.

Beams are a fixed-size ring buffer of 10 entries (`arrSLine`, `arrGLine`). Each entry stores a line segment's start/end/increment. Every `tmrAttack` tick: erase old position (draw in background color), advance by increment, draw at new position, check hit, check wrap. The "draw with background color to erase" pattern is the VB6 sprite erasure technique — pygame replaces it with `screen.fill()` + redraw each frame.

Sound: two Windows Media Player controls — one for one-shot effects (laser, death, explosion), one for looping background MIDI. In pygame these become `pygame.mixer.Sound` for effects and `pygame.mixer.music` for background.

The known VB6 bug: `ElseIf .bytDir = 3 Or 4 Then` evaluates as `ElseIf (.bytDir = 3) Or (4) Then`, which is always `True` because `4` is a non-zero integer. This means the horizontal-beam hit check runs for every beam regardless of direction. The fix is `ElseIf .bytDir = 3 Or .bytDir = 4 Then`.

---

## Recommended Architecture

### One Sentence

A single-file-per-concern flat module layout driven by a `pygame.time.Clock`-based game loop, with a `GameState` enum controlling which subsystem is active each frame.

### File Layout

```
slappy-ai/
    main.py                  # Entry point: init pygame, create Game, run loop
    game.py                  # Game class: loop, state machine, event dispatch
    states.py                # GameState enum (INTRO, PLAYING, PAUSED)
    player.py                # Player class: position, velocity, direction, sprite selection, crash physics
    beam.py                  # Beam class: position, velocity, wrap logic, hit detection
    sound.py                 # SoundManager: load and play effects + background music
    assets.py                # AssetLoader: load and cache all images and sounds at startup
    hud.py                   # HUD: update window caption with score
    settings.py              # Constants: resolution, speeds, colors, key bindings
    assets/
        sprites/
            superman/        # superman_up1.png, superman_up2.png, ... (PNG exports from ICO)
            goblin/          # goblin_up1.png, goblin_up2.png, ...
            intro/           # tree.png, goblin_intro.png, superman_intro.png
        sounds/
            laser.wav
            deathcry.wav
            explode.wav
            canyon.wav       # converted from canyon.mid
            passport.wav     # converted from passport.mid
```

Seven source files is the right size for this game. Do not add a `scenes/` layer, a `components/` abstraction, or a plugin system. The original was one form and ~1,400 lines of spaghetti; the port should be ~700 lines of clean Python.

---

## Component Boundaries

| Component | Responsibility | What It Does NOT Do |
|-----------|---------------|---------------------|
| `main.py` | Bootstrap pygame, create Game, call `game.run()` | No game logic |
| `game.py` | Own the main loop, own `GameState`, dispatch events, call update/draw on active subsystem | Does not own player/beam state directly |
| `player.py` | Track position, velocity, direction, crash state, pose timer, sprite frame; expose `update(dt)` and `draw(screen)` | Does not read keyboard directly |
| `beam.py` | Track segment position and velocity; advance per frame; detect collision with a given target rect; handle wrap | Does not know about players — receives target rect |
| `sound.py` | Load all sounds at startup; expose `play_effect(name)` and `play_music(name, loop)` | Does not know about game state |
| `assets.py` | Load and cache `pygame.Surface` objects and `pygame.mixer.Sound` objects once at startup | Does not draw anything |
| `hud.py` | Update `pygame.display.set_caption()` with formatted score string | Does not own score data |
| `settings.py` | All magic numbers as named constants | No logic |

---

## Data Flow

```
Keyboard events (pygame.KEYDOWN / KEYUP)
    |
    v
game.py: handle_events()
    |-- if PLAYING: translate keycode to player action
    |       |-- direction keys -> player.set_direction(dir)
    |       |-- shoot key      -> game.spawn_beam(player)
    |       |-- pose key       -> player.set_direction(POSE)
    |       |-- respawn key    -> player.respawn() if player.dead
    |-- if F2: game.new_game()
    |-- if DELETE: quit
    |-- mouse click on player rect -> game.omnipotent_kill(player)
    v
game.py: update(dt)
    |-- INTRO state: advance intro animation timer, check for dismiss
    |-- PLAYING state:
    |       |-- player_s.update(dt)   # move, clamp, wrap, advance sprite frame
    |       |-- player_g.update(dt)
    |       |-- for beam in beams:
    |               beam.update(dt)   # advance, wrap, check hit
    |               if beam.hit(player_s.rect) or beam.hit(player_g.rect):
    |                   kill victim, add to attacker score
    |                   sound.play_effect('deathcry')
    |               if beam.expired: remove from list
    |-- hud.update(scores)            # set_caption
    v
game.py: draw(screen)
    |-- screen.fill(BG_COLOR)
    |-- draw ground bar (static surface, pre-rendered)
    |-- draw ceiling bar (static surface, pre-rendered)
    |-- for beam in beams: beam.draw(screen)    # pygame.draw.line
    |-- player_s.draw(screen)
    |-- player_g.draw(screen)
    |-- pygame.display.flip()
```

All state flows through `game.py`. Players and beams do not reference each other or the display. Sound is fire-and-forget via `sound.play_effect()`.

---

## Specific pygame APIs to Use

### Game Loop

Use `pygame.time.Clock` with a fixed target frame rate of **60 FPS**.

```python
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60)  # milliseconds since last frame, capped at 60 FPS
    handle_events()
    update(dt)
    draw()
```

Pass `dt` (delta time in ms) to all `update()` calls. Scale velocities as `pixels_per_ms * dt`. This replaces the VB6 timer model: `tmrSMove` at 75 ms / `tmrGMove` at 75 ms / `tmrAttack` at 5 ms are all collapsed into the single 60 Hz loop with dt-scaled movement.

**Do not** use `pygame.time.set_timer` for movement — it adds latency and complexity. The VB6 used separate timers because VB6 had no game loop concept. pygame does not need them.

### State Machine

```python
from enum import Enum, auto

class GameState(Enum):
    INTRO   = auto()
    PLAYING = auto()
```

`game.py` holds `self.state: GameState`. Each `update()` and `draw()` call branches on `self.state`. No third-party state machine library needed — an enum and an if/elif is sufficient for two states.

### Sprite Management

Do NOT use `pygame.sprite.Sprite` or `pygame.sprite.Group` for this game.

Rationale: The game has exactly two characters and a variable-length list of beams. The overhead of `Group.update()` and `Group.draw()` is irrelevant at this scale, and the `Group` abstraction requires `.rect` and `.image` to be set on sprites — which fights the manual frame-selection logic copied from VB6's `SPose()` / `GPose()` pattern. A plain `Player` class with `update(dt)` and `draw(screen)` is simpler and easier to debug.

Use a plain Python `list[Beam]` for active beams, with list comprehension cleanup:

```python
self.beams = [b for b in self.beams if not b.expired]
```

### Player Sprite Selection

The VB6 uses `LoadPicture()` inside the timer callback to switch sprites — equivalent to loading a file from disk every frame. In pygame, load all sprites once at startup into a dict keyed by (character, direction, frame):

```python
# In AssetLoader
self.sprites = {
    ('superman', 'up', 0):    pygame.image.load(...).convert_alpha(),
    ('superman', 'up', 1):    pygame.image.load(...).convert_alpha(),
    ('superman', 'right', 0): pygame.image.load(...).convert_alpha(),
    # etc.
}
```

`Player.draw()` calls `screen.blit(assets.sprites[(self.character, self.direction, self.frame)], self.rect)`.

Animation frame (0/1 alternating) advances every N frames inside `player.update()`. Match VB6 cadence: `tmrSMove` was 75 ms, so flip the walking frame every ~75 ms.

Crash animation (spin): advance through frames SSpin1→SSpin4 cyclically every ~100 ms, matching `tmrSCrash`'s 100 ms interval.

### Laser Beam System

The VB6 beam is a moving line segment: `(intX, intY) -> (intNewX, intNewY)`, translated each tick by `(intIncX, intIncY)`. The beam is 350 VB6 twips long, oriented along one axis only (no diagonal beams).

**pygame equivalent:** Each `Beam` object stores:

```python
@dataclass
class Beam:
    x: float       # tail position
    y: float
    dx: float      # per-ms velocity
    dy: float
    length: int    # pixels (350 VB6 twips scaled to target resolution)
    color: tuple   # (255, 0, 0) for Superman, (0, 128, 0) for Goblin
    wrap_count: int = 0
    expired: bool = False
```

Each frame: advance `x += dx * dt`, `y += dy * dt`. Compute head position as `(x + dx_unit * length, y + dy_unit * length)`. Draw with `pygame.draw.line(screen, color, (x, y), (head_x, head_y), width=2)`.

No erase step. `screen.fill(BG_COLOR)` at the top of every draw call clears everything. This is the key architectural difference from VB6's draw-in-background-color-to-erase idiom.

**Wrap:** When the tail or head exits `[0, SCREEN_WIDTH]` horizontally, reposition to the opposite edge. Expire after `wrap_count >= 2`, matching VB6's `SWrapCheck` / `GWrapCheck`. Vertical beams stop at ceiling/ground (set `dy = 0`, mark expired).

**Collision:** Beam-to-player collision is a line-rect intersection. Given the beam is axis-aligned, this simplifies to:

- Horizontal beam: does the beam's Y fall within `player.rect.top..player.rect.bottom`, and does any X between tail and head overlap `player.rect.left..player.rect.right`?
- Vertical beam: symmetric check.

This is the correct logic the VB6 was trying to implement in `SHit` / `GHit` (and what the Or-bug broke for horizontal beams).

Ring buffer of 10 beams: the VB6 limits simultaneous beams to 10 per player (`intSCounter`, `intGCounter` mod 10). Preserve this: if `len(player_s_beams) >= 10`, drop the oldest before appending the new one.

### Input Handling

```python
# settings.py
SUPERMAN_KEYS = {
    pygame.K_UP:      'up',
    pygame.K_DOWN:    'down',
    pygame.K_LEFT:    'left',
    pygame.K_RIGHT:   'right',
    pygame.K_LSHIFT:  'shoot',
    pygame.K_RSHIFT:  'shoot',
    pygame.K_LCTRL:   'pose',
    pygame.K_RCTRL:   'pose',
    pygame.K_RETURN:  'respawn',
}
GOBLIN_KEYS = {
    pygame.K_e:     'up',
    pygame.K_d:     'down',
    pygame.K_s:     'left',
    pygame.K_f:     'right',
    pygame.K_r:     'shoot',
    pygame.K_SPACE: 'pose',
    pygame.K_w:     'respawn',
}
```

Use `pygame.key.get_pressed()` inside `update()` for held-direction movement (continuous movement while key is held, matching the VB6 behavior where direction is stored and applied every timer tick). Use `KEYDOWN` events for shoot and respawn (one-shot actions, matching VB6's `Form_Keydown` handler).

The VB6 direction model (store last-pressed direction, apply continuously) maps naturally to:

```python
def update(self, dt):
    keys = pygame.key.get_pressed()
    if keys[K_UP]:   self.direction = 'up'
    elif keys[K_DOWN]: self.direction = 'down'
    # etc.
    self.x += VX[self.direction] * dt
    self.y += VY[self.direction] * dt
```

Two players on one keyboard work automatically — `get_pressed()` returns the state of all keys simultaneously.

**Mouse click kill (OmnipotentShootingGuy):** In the VB6, `imgG_MouseDown` / `imgS_MouseDown` fire when the mouse is clicked on the VB6 Image control that visually represents the character. In pygame: in the `MOUSEBUTTONDOWN` event handler, check `player.rect.collidepoint(event.pos)`.

### Sound System

```python
# sound.py
import pygame

class SoundManager:
    def __init__(self, asset_dir):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._effects = {
            'laser':    pygame.mixer.Sound(asset_dir / 'sounds/laser.wav'),
            'deathcry': pygame.mixer.Sound(asset_dir / 'sounds/deathcry.wav'),
            'explode':  pygame.mixer.Sound(asset_dir / 'sounds/explode.wav'),
        }

    def play_effect(self, name: str):
        self._effects[name].play()  # non-blocking, uses mixer channels automatically

    def play_music(self, filename: str):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops=-1)  # -1 = loop forever

    def stop_music(self):
        pygame.mixer.music.stop()
```

`pygame.mixer.Sound.play()` for effects — pygame allocates mixer channels automatically, so simultaneous laser + death sounds work without manual channel management for this game's scale.

`pygame.mixer.music` for background — only one track plays at a time, which matches the VB6's single `MediaPlayer2`. VB6 played Canyon.mid on the intro/credits screen and Passport.mid during gameplay; replicate with `play_music('canyon.wav')` on game launch and `play_music('passport.wav')` when `New_Game` starts.

MIDI conversion: use `timidity` or `fluidsynth` with a GM soundfont to produce `canyon.wav` and `passport.wav`. This is a build-time preprocessing step, not runtime.

### Score and HUD

The VB6 puts score in the window title: `"Goblin N Superman N OmnipotentShootingGuy N"`. Preserve this exactly.

```python
# hud.py
import pygame

def update_caption(goblin_score: int, superman_score: int, guy_score: int):
    pygame.display.set_caption(
        f"Goblin {goblin_score} Superman {superman_score} OmnipotentShootingGuy {guy_score}"
    )
```

Call `update_caption()` from `game.py` whenever any score changes. No in-game HUD overlay needed.

Score state lives in `game.py` as plain integers: `self.goblin_score`, `self.superman_score`, `self.guy_score`. The VB6's split between `intGScore` / `intGScoreMod` / `intGScoreFin` (pose ticks + hit bonus) should be simplified: accumulate directly in final score units.

---

## Intro Screen Architecture

The credits screen (Form1.frm) has:
- Scrolling credits label (one line every 1500 ms)
- Random character sprite alternating every 750 ms
- Background image (tree.bmp)
- Dismiss: click anywhere or press any key (in VB6 it was form click; generalise to any keypress)

In pygame this is the `INTRO` state in `game.py`:

```python
# In GameState.INTRO update():
self.credit_timer += dt
if self.credit_timer >= 1500:
    self.credit_timer = 0
    self.credit_index = (self.credit_index + 1) % len(CREDITS)

self.sprite_timer += dt
if self.sprite_timer >= 750:
    self.sprite_timer = 0
    self.intro_sprite = random.choice(INTRO_SPRITES)
```

Transition to `PLAYING` on `KEYDOWN` (any key) or `MOUSEBUTTONDOWN`. Call `new_game()` on transition.

The game form's own intro (instructions + alternating character images, `tmrIntro` at 150 ms, dismissed by starting a game) maps to the early `PLAYING` state before F2 is pressed. In the VB6, `Form_Load` for `frmForm` shows the instructions panel which is then hidden when `New_Game()` is called. The simplest pygame equivalent: the `INTRO` state shows credits; pressing any key moves to `PLAYING` and calls `new_game()` directly — no intermediate instructions-visible state is needed if the instructions are shown in the intro screen instead.

---

## Scalability Considerations

This game has a fixed scope. These are design limits to stay aware of, not things to engineer for:

| Concern | For This Game | Note |
|---------|--------------|------|
| Beam count | Max 20 active (10 per player) | Trivial; no pooling needed |
| Sprite count | 2 characters, ~50 frames total | Load all at startup, fits in RAM |
| Resolution | Fixed, match original aspect ratio | ~800x600 or 900x633 (matching VB6 `ClientWidth=4455` / `ScaleWidth=7350` twips) |
| Frame rate | 60 FPS cap | `Clock.tick(60)` |
| Sound channels | 8 default mixer channels | More than enough; don't touch |

---

## Build Order (Phase Dependencies)

The correct build sequence for roadmap phase planning follows these dependency edges:

```
1. settings.py + assets.py
       |
       v
2. game loop skeleton (main.py + game.py shell + GameState enum)
       |
       v
3. player.py (position, direction, wrap, basic blit with placeholder rect)
       |
       +-- 4a. beam.py (requires player position to spawn from)
       |
       +-- 4b. sound.py (independent; can be added any time after loop exists)
       |
       v
5. Collision detection (beam.py hits player.py rect)
       |
       v
6. Score + hud.py (requires collision to be meaningful)
       |
       v
7. Death/crash animation + respawn (requires score + collision)
       |
       v
8. Intro state + credits scroll (independent of gameplay; add last)
       |
       v
9. Mouse-click OmnipotentShootingGuy mechanic (requires player rects to be accurate)
       |
       v
10. Polish: sprite art upscale, sound conversion, caption formatting
```

Phases 4a and 4b are independent and can be worked in parallel. Everything before phase 5 can use colored rectangles instead of sprites — defer art until the mechanics are correct.

---

## Anti-Patterns to Avoid

### Pygame Sprite Groups for This Game
**What:** Using `pygame.sprite.Group` and inheriting from `pygame.sprite.Sprite`
**Why bad:** Imposes `.rect`/`.image` contract that fights the frame-selection logic; adds indirection for a two-character game where explicit `player_s.update()` / `player_g.update()` is clearer
**Instead:** Plain classes with `update(dt)` / `draw(screen)` methods called explicitly in the game loop

### Replicating the VB6 Timer Architecture
**What:** Using `pygame.time.set_timer` to fire separate events for movement, beam drawing, crash animation
**Why bad:** Reintroduces the VB6's fragmentation into a paradigm that does not need it; timing accuracy is worse than a 60 Hz loop with dt
**Instead:** Single `Clock.tick(60)` loop; dt-scaled movement; internal counters on Player/Beam for animation cadence

### Loading Images Every Frame
**What:** Calling `pygame.image.load()` inside `update()` or `draw()`
**Why bad:** VB6 did `LoadPicture()` in the timer because it had no other option; `pygame.image.load()` reads disk and is slow
**Instead:** Load all images in `AssetLoader.__init__()`, cache as dict, blit cached surfaces

### `pygame.display.update(rect_list)` with Dirty Rect Tracking
**What:** Tracking and passing only changed rects to `display.update()` to avoid full-screen redraws
**Why bad:** The background must be redrawn anyway to erase beams; dirty rect tracking adds complexity with no perceptible benefit at 60 FPS on modern hardware
**Instead:** `screen.fill(BG_COLOR)` + full redraw + `pygame.display.flip()` every frame

### Putting Game Logic in Event Handlers
**What:** Doing movement math inside the `KEYDOWN` event handler
**Why bad:** VB6's `Form_Keydown` called `SMove()` / `GMove()` directly, making movement frame-rate-dependent on key events; produces choppy movement in pygame where events are processed once per frame
**Instead:** Store direction from key events; compute movement in `update(dt)` using `get_pressed()` for held keys

---

## Sources

- VB6 source read directly: `D:\dev\repo\best-game-ever\_old\frmSuperman.frm`, `Form1.frm`
- pygame documentation: `pygame.time.Clock`, `pygame.mixer`, `pygame.draw.line`, `pygame.key.get_pressed()` — HIGH confidence (stable APIs, well-documented since pygame 1.x, unchanged in pygame 2.x)
- Beam erase-by-background-color pattern identified directly from VB6 `DrawSLines()` / `DrawGLines()`: `Line (.intX,.intY)-(.intNewX,.intNewY), frmForm.BackColor` followed by advance followed by `Line (...), vbRed`
- VB6 Or-bug identified at line 1142: `ElseIf .bytDir = 3 Or 4 Then` — documented in PROJECT.md and confirmed in source
