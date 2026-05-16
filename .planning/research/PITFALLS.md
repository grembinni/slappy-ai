# Domain Pitfalls

**Domain:** VB6 → Python/pygame 2-player local multiplayer arcade brawler port
**Project:** Goblin vs. Superman
**Researched:** 2026-05-16
**Confidence:** HIGH — derived from direct reading of VB6 source (`frmSuperman.frm`) and pygame internals knowledge

---

## Critical Pitfalls

Mistakes that cause rewrites or major correctness failures.

---

### Pitfall 1: Replicating the VB6 `Or 4` Collision Bug (or Introducing a Worse One)

**What goes wrong:**
The VB6 `SHit` and `GHit` subroutines contain this code:

```vb
ElseIf .bytDir = 3 Or 4 Then
```

In VB6, `Or` is a bitwise operator when used in a non-boolean context. `3 Or 4 = 7`, which is truthy, so this branch is **always entered regardless of direction**. The result: every laser beam performs a horizontal-direction hit check even when travelling vertically. The intent was `ElseIf .bytDir = 3 Or .bytDir = 4 Then`.

The same pattern appears in `GHit` at line 1338.

**Why it happens:**
The original developer knew VB6's `Or` was misused (the comments say "they aren't bugs, they're features"), but in Python the expression `direction == 3 or 4` is also a bug — it evaluates as `(direction == 3) or 4`, which is always truthy because `4` is truthy. Python silently preserves the VB6 bug.

**Consequences:**
- In Python, `if beam.direction == 3 or 4:` replicates the exact VB6 bug. The bug gets ported even when you intended to fix it.
- Collision detection fires for every beam regardless of travel direction.

**Prevention:**
Write the condition as `if beam.direction in (3, 4):` or `if beam.direction == 3 or beam.direction == 4:`. Never use `or <integer literal>` in a boolean chain. Add a unit test that shoots a beam going Up (direction=1) and asserts it does NOT trigger the left/right collision branch.

**Warning signs:**
- "All shots feel laggy to dodge" — they hit from any angle.
- If you paste the VB6 logic verbatim and only change syntax, the bug survives.

**Phase:** Collision detection implementation (core gameplay phase).

---

### Pitfall 2: Frame-Rate-Dependent Movement (the Timer-to-Clock Translation)

**What goes wrong:**
The VB6 game uses separate timers: `tmrSMove.Interval = 30` ms for Superman, an unlisted interval for Goblin (interval was not set in visible code — defaults to 0/disabled), and `tmrAttack.Interval = 5` ms for beam updates. Movement is `intSpeed = 500` twips applied each tick, so speed is implicitly `500 twips / timer_interval`.

In pygame, the naive port calls `clock.tick(60)` and moves entities by a fixed pixel count per frame. If the machine runs faster or slower than expected, characters move at different speeds. On modern hardware `clock.tick(60)` is accurate enough for this simple game, but if vsync or system load causes frame time variance, movement becomes inconsistent.

More critically: the VB6 timers fired independently, meaning Superman and Goblin could theoretically get different update rates. A pygame single-loop processes both in one frame — this is actually better, but developers sometimes compensate by adding artificial delays that reintroduce the problem.

**Why it happens:**
Developers copy `speed = 5` pixel literals from VB6 twip values without converting, then add `clock.tick(60)` without applying `dt = clock.get_time() / 1000.0` to scale movement.

**Consequences:**
- Characters fly 2x fast on a 120Hz monitor if movement is not dt-scaled.
- Characters stutter if the machine drops below 60fps.

**Prevention:**
Use `dt = clock.tick(60) / 1000.0` and multiply all position increments by `dt`. Target pixel-per-second speeds, not pixel-per-frame.

```python
# VB6: intSpeed = 500 twips/tick at ~30ms interval
# 1 twip = 1/1440 inch; at 96dpi: 500 twips ≈ 33 pixels
# At 30ms tick: 33px / 0.03s ≈ 1100 px/s at 96dpi
# pygame: target ~180 px/s at modern resolution for similar feel
SPEED_PX_PER_SEC = 180
# In loop:
x += direction_x * SPEED_PX_PER_SEC * dt
```

**Warning signs:**
- Movement "feels wrong" at different frame rates.
- Testing exclusively at 60fps and not noticing 120fps issues.

**Phase:** Core movement / game loop setup (first gameplay milestone).

---

### Pitfall 3: Using KEYDOWN Events for Continuous Movement (Two-Player Input)

**What goes wrong:**
The VB6 `Form_Keydown` handler sets a direction byte (`bytSDir`, `bytGDir`) on each key press, and timers move characters continuously in that direction. In pygame, developers often mirror this by listening only to `pygame.KEYDOWN` events to update direction. This works, but `pygame.KEYDOWN` fires once, then repeats only after the OS key-repeat delay (~500ms). Characters stutter on direction changes.

The correct approach is `pygame.key.get_pressed()` polled each frame, which maps directly to the VB6 pattern of "currently held direction key determines movement."

**Why it happens:**
The pygame event loop tutorial prominently features `KEYDOWN`/`KEYUP` for responsive controls, so beginners reach for it first. VB6's `KeyDown` event also fires continuously (Windows sends WM_KEYDOWN with repeat), masking the distinction.

**Consequences:**
- Holding Up Arrow for Superman causes it to lurch then pause, then repeat.
- With two players on one keyboard, KEYDOWN events may be missed when both players hold keys simultaneously (N-Key Rollover issues on cheap keyboards).

**Prevention:**
Use `pygame.key.get_pressed()` for all directional movement. Reserve `KEYDOWN` events only for one-shot actions (shoot, respawn, new game, quit):

```python
keys = pygame.key.get_pressed()

# Superman continuous movement
if keys[pygame.K_UP]:
    superman.dir = DIR_UP
elif keys[pygame.K_DOWN]:
    superman.dir = DIR_DOWN
elif keys[pygame.K_LEFT]:
    superman.dir = DIR_LEFT
elif keys[pygame.K_RIGHT]:
    superman.dir = DIR_RIGHT

# One-shot shoot — use KEYDOWN event, not get_pressed:
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RSHIFT and not superman.dead:
            superman.shoot()
        if event.key == pygame.K_r and not goblin.dead:
            goblin.shoot()
```

**Warning signs:**
- Direction changes feel "sticky" or delayed.
- Shoot action fires multiple times per keypress.

**Phase:** Input system (first gameplay milestone).

---

### Pitfall 4: N-Key Rollover / Ghost Keys on Shared Keyboard

**What goes wrong:**
The control scheme assigns keys from two different keyboard regions: Superman uses arrow cluster + Shift/Ctrl/Enter; Goblin uses ESDF + R/Space/W. These regions are physically separated and should not conflict electrically on most keyboards. However, modifier keys (Shift, Ctrl) interact with pygame's key scan — `pygame.K_LSHIFT` and `pygame.K_RSHIFT` are distinct from each other, and the VB6 code used `vbKeyShift` (generic shift). If the port binds only `K_LSHIFT`, right-shift does not shoot.

More critically: many laptop keyboards use a matrix that blocks certain three-key combinations. If Goblin holds S+F (left+right), and Superman presses Right Arrow, the third key may ghost.

**Why it happens:**
Developers bind keys by testing alone (one player). The three-key failure only manifests during actual two-player sessions.

**Consequences:**
- Superman cannot shoot while Goblin holds two movement keys.
- Players blame "lag" when the real issue is keyboard rollover.

**Prevention:**
- Bind both `K_LSHIFT` and `K_RSHIFT` for Superman's shoot action (use `keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]`).
- Test all control combinations with two humans before first playtest.
- Document that this is a hardware limitation on low-end keyboards — it is not fixable in software.
- The ESDF+R/Space/W layout was a good choice in the original; preserve it. Do not move Goblin to WASD, which conflicts with Windows system shortcuts and increases rollover risk.

**Warning signs:**
- Player 2 reports intermittent non-response during intense play.
- Keys work fine in solo testing but fail with two players.

**Phase:** Input system (first gameplay milestone, two-player test before shipping).

---

### Pitfall 5: Twip-to-Pixel Coordinate Mismatch

**What goes wrong:**
VB6 measures screen coordinates in twips (1/1440 inch). The VB6 form is:
- `ClientWidth = 4455` twips, `ClientHeight = 6330` twips
- `frmForm.Width = 9000` twips during gameplay, `Height = Screen.Height - 300`
- `intImgHeight = 850` twips, `intImgWidth = 850` twips
- `intShotLength = 350` twips
- `intSpeed = 500` twips

At 96dpi (standard Windows): 1 twip = 96/1440 = 0.0667px, so:
- Play area: 9000 twips ≈ 600px wide
- Sprite: 850 twips ≈ 57px (close to the 32x32 ICO at screen scaling)
- Shot length: 350 twips ≈ 23px
- Speed: 500 twips/tick at 30ms ≈ 1,110 px/s at 96dpi

However, VB6's `Screen.TwipsPerPixelX` varies by system DPI setting, so the original game's dimensions were DPI-dependent. At 120dpi it ran differently than at 96dpi.

Naively copying numeric values without conversion produces a game that is either too cramped (if using twip values as pixels: 850-pixel sprites) or too small (if the conversion arithmetic is wrong).

**Why it happens:**
Developers see `intImgHeight = 850` and write `SPRITE_HEIGHT = 850` in pixels.

**Consequences:**
- At 850px, sprites are enormous and fill the screen.
- At 32px (raw ICO size), sprites are invisible on modern displays.
- `intShotLength = 350` pixels makes beams span half the screen (too long) or at 23px they are invisible (too short).

**Prevention:**
Define a canonical internal resolution (e.g., 800x600) and derive all gameplay values from it. Work in pixels from the start; do not import twip numbers. Use the original game's *feel* as the target, not its numeric values. A good starting point:
- Play area: 800x540px (leaving 60px for ground/ceiling bands)
- Sprites: 64x64px (2x upscale from 32x32 ICO)
- Shot segment length: 80px
- Character speed: ~180px/s

**Warning signs:**
- Characters are comically large or tiny relative to the screen.
- Shot beams are nearly invisible or span the entire width.

**Phase:** Layout / coordinate system setup (very first phase — establish before drawing anything).

---

## Moderate Pitfalls

---

### Pitfall 6: ICO File Loading — Alpha Channel and Palette Issues

**What goes wrong:**
pygame's `pygame.image.load()` can load Windows ICO files on most platforms, but ICO files contain multiple embedded image sizes (16x16, 32x32, 48x48, 256x256) and pygame picks one unpredictably. The 32x32 images in the original repo use a 1-bit mask for transparency (AND mask + XOR mask), not an 8-bit alpha channel. pygame may load these with a black background instead of transparency.

Additionally, ICO files use indexed colour (palette mode). When converted to a pygame surface, the transparent colour index may not be interpreted as transparent — you get a surface with a solid colour background.

**Why it happens:**
ICO transparency is not PNG-style alpha. pygame's ICO loader behaviour on Windows differs from Linux. A file that loads correctly on the developer's Windows machine may show black boxes on another OS.

**Consequences:**
- Goblin and Superman sprites appear with black or white rectangles around them.
- Transparency works in dev but breaks on other machines.

**Prevention:**
Convert all ICO files to PNG with transparency before importing into pygame. Use Python's Pillow library for the conversion:

```python
from PIL import Image
img = Image.open("GEvil.ico")
img = img.convert("RGBA")  # handles AND mask → alpha channel
img.save("GEvil.png")
```

Then load PNGs in pygame with `pygame.image.load("GEvil.png").convert_alpha()`. Do this conversion once as a build step, not at runtime. Commit the PNGs, not the ICOs, to the game's asset directory.

**Warning signs:**
- Sprites load fine on Windows but show black backgrounds on macOS/Linux.
- `convert_alpha()` has no effect on ICO-loaded surfaces.

**Phase:** Asset conversion (first phase, before any rendering work).

---

### Pitfall 7: Laser Beam Collision as Line Segment vs. Rectangle

**What goes wrong:**
The VB6 collision detection checks whether a beam's endpoints or control points fall inside the target sprite's bounding rectangle. The beam is a line segment with two endpoints: `(intX, intY)` to `(intNewX, intNewY)`. In the VB6 code, only the endpoints are tested — the beam can pass through a corner of the target without detecting a hit if the beam is long enough to span the character entirely (head endpoint past, tail endpoint past).

In pygame, the common mistake is to use `pygame.Rect.colliderect()` between a 1-pixel-wide beam rect and the character rect. If the beam moves fast enough, it tunnels through the character between frames.

**Why it happens:**
Developers model the beam as a pygame.Rect with width=1 and check colliderect. At the beam speed of ~180px/s, the beam moves ~3px per frame at 60fps — unlikely to tunnel. But if the dt-based speed is miscalibrated higher, tunneling occurs.

**Consequences:**
- Beams pass through characters at high speeds or on slow machines.
- At normal speeds, collision works fine — the bug only appears under load.

**Prevention:**
Model each beam as a line segment stored as `(x1, y1, x2, y2)` matching the VB6 approach. Use `pygame.Rect.clipline()` (available since pygame 2.0) for line-segment-to-rectangle intersection:

```python
char_rect = pygame.Rect(char.x, char.y, SPRITE_W, SPRITE_H)
hit = char_rect.clipline(beam.x1, beam.y1, beam.x2, beam.y2)
if hit:
    # beam intersects character
```

This exactly matches the VB6 logic and avoids tunneling entirely. Do not use pixel-perfect collision — the original uses AABB (bounding box) only.

**Warning signs:**
- Players report beams passing through characters, especially from vertical shots.
- Collision tests pass in unit tests but fail during fast gameplay.

**Phase:** Collision detection implementation.

---

### Pitfall 8: Music Looping Gap with pygame.mixer

**What goes wrong:**
`pygame.mixer.music.play(-1)` loops music, but with WAV files converted from MIDI there is often a silent gap at the end of the loop point. MIDI files like `Passport.mid` and `Canyon.mid` typically end with a trailing silence or a note-off delay. When converted to WAV with timidity or fluidsynth at default settings, the output includes 1-3 seconds of silence before the loop.

Additionally, `pygame.mixer.music.play(-1)` restarts from the beginning of the file on each loop, including any intro section. If the MIDI had a non-repeating intro, the loop repeats it on every cycle.

**Why it happens:**
WAV converters don't trim trailing silence. pygame's music looping has no loop-point parameter (unlike SDL_mixer's native `Mix_FadeInMusicPos`).

**Consequences:**
- Music loops with a jarring pause every cycle.
- The intro section plays repeatedly instead of once.

**Prevention:**
During MIDI-to-WAV conversion, trim trailing silence. With fluidsynth:
```
fluidsynth -ni -F output.wav soundfont.sf2 input.mid
```
Then use ffmpeg to strip trailing silence:
```
ffmpeg -i output.wav -af silenceremove=stop_periods=-1:stop_duration=0.1:stop_threshold=-50dB trimmed.wav
```
Alternatively, use OGG Vorbis format (which supports loop-point metadata) and load with `pygame.mixer.music.load("canyon.ogg")`. OGG is preferred over WAV for music because `pygame.mixer.music` streams it rather than loading the whole file into memory.

**Warning signs:**
- Music has a noticeable 1-2 second silence before restarting.
- Converted WAV file is larger than expected (extra silence frames).

**Phase:** Audio / music conversion (can be done before or after gameplay; audio is separable).

---

### Pitfall 9: Game State Managed with Boolean Flags Instead of a State Machine

**What goes wrong:**
The VB6 code manages state with boolean flags (`blnSCrash`, `blnGCrash`, `blnIntro`) and by enabling/disabling timers. The pygame port's temptation is to replicate this: `is_dead`, `is_crashing`, `is_posing`, `in_intro` booleans. With two characters each having 4+ states and a global intro/gameplay state, you end up with 8+ flags and complex nested if-trees to determine what is valid in each combination.

The specific danger in this game: `blnSCrash = True` is set at line 890 (inside `tmrSCrash_Timer`) and also at line 1335 (inside `GHit`) before the crash timer is even enabled. In the VB6 code, crash detection (`blnGCrash` check in `SHit`) runs while the crash is already in progress. The flag order matters. Boolean flags make this kind of ordering dependency invisible.

**Why it happens:**
Porting line-by-line preserves the flag structure. Booleans feel simpler than an enum.

**Consequences:**
- You can be simultaneously "posing" and "dead" because there is no single authority for the current state.
- The respawn logic (Enter/W keys) fires during the crash animation (before the character lands) because `blnSCrash` is set early but the crash animation is incomplete.

**Prevention:**
Use an enum state machine per character. Python's `enum.Enum` is zero-overhead:

```python
from enum import Enum, auto

class CharState(Enum):
    ALIVE = auto()
    CRASHING = auto()   # spinning/falling
    DEAD = auto()       # lying on ground, awaiting respawn key
    POSING = auto()     # scoring pose (still alive)
    RESPAWNING = auto() # brief invincibility after respawn

class Character:
    def __init__(self):
        self.state = CharState.ALIVE
```

Valid transitions: `ALIVE → POSING → ALIVE`, `ALIVE → CRASHING → DEAD → ALIVE`. Respawn key is only processed in `DEAD` state. This eliminates the entire class of "crashed but still accepting input" bugs.

**Warning signs:**
- You find yourself writing `if not dead and not crashing and not in_intro:` guards.
- Respawn fires during the death animation.
- Score increments during a character's crash sequence.

**Phase:** Character architecture (establish before implementing movement or state transitions).

---

### Pitfall 10: VB6 AutoRedraw → pygame Dirty Rect / Full Redraw Confusion

**What goes wrong:**
The VB6 form uses `AutoRedraw = True`, which means VB6 maintains an off-screen buffer and redraws automatically. Laser beams are drawn with `Line` commands directly onto the form's canvas, and "erased" by drawing the background colour over them each tick. The draw order is: erase old beam, move beam, draw new beam.

In pygame, beginners replicate this with `pygame.draw.line()` on the main surface and never call `screen.fill()` or blit a background. The result: beam trails persist on screen because the old positions are never cleared.

Alternatively, some developers call `screen.fill(background_colour)` every frame, which wipes the background. This is correct, but they then fail to redraw the ground/ceiling bands after filling, creating a plain-colour screen with no ground.

**Why it happens:**
VB6's "draw then erase" pattern doesn't translate to pygame's "clear then draw" pattern. They look identical in code structure but have opposite timing requirements.

**Consequences:**
- Beam trails streak across the screen.
- Ground and ceiling bands disappear after the first frame.

**Prevention:**
Every frame: `screen.blit(background_surface, (0, 0))` first, then draw all sprites and beams on top. Pre-render the background (including green ground band and white ceiling band) once into a `background_surface` at startup. Never draw beams directly to the screen and rely on erasing them.

```python
# Startup:
background = pygame.Surface((SCREEN_W, SCREEN_H))
background.fill(SKY_COLOUR)
pygame.draw.rect(background, GREEN, (0, GROUND_Y, SCREEN_W, CEILING_H))
pygame.draw.rect(background, WHITE, (0, 0, SCREEN_W, CEILING_H))

# Each frame:
screen.blit(background, (0, 0))
for beam in active_beams:
    pygame.draw.line(screen, beam.colour, beam.start, beam.end, 2)
for char in characters:
    screen.blit(char.current_sprite, char.rect)
pygame.display.flip()
```

**Warning signs:**
- Beam trails visible on screen.
- Background colour visible through the ground band.

**Phase:** Rendering setup (first phase, before drawing anything gameplay-related).

---

## Minor Pitfalls

---

### Pitfall 11: Window Title Score Update Performance

**What goes wrong:**
The VB6 code updates `frmForm.Caption` (window title) on every score event and every pose tick. In pygame, `pygame.display.set_caption()` is a system call. Calling it inside the pose-scoring loop (which fires every timer tick while posing) causes minor but measurable overhead. Not a crash, but noticeable on slower machines.

**Prevention:**
Cache the last title string. Only call `pygame.display.set_caption()` when the string changes.

```python
new_title = f"Goblin {goblin_score} Superman {superman_score} OmnipotentShootingGuy {guy_score}"
if new_title != current_title:
    pygame.display.set_caption(new_title)
    current_title = new_title
```

**Phase:** Scoring implementation.

---

### Pitfall 12: Horizontal Wrap Boundary Off-by-One

**What goes wrong:**
The VB6 wrap logic for characters is:
```vb
If intSX <= intFormLeft Then intSX = intFormRight
ElseIf intSX >= intFormRight Then intSX = intFormLeft
```
where `intFormLeft = 0 - intImgWidth / 2` (negative value) and `intFormRight = frmForm.Width - intImgWidth / 2`.

Characters wrap when their left edge goes off-screen, not when they fully exit. This means half the character is visible at the edge before wrapping. If the pygame port uses `if x < 0: x = SCREEN_W` without accounting for sprite width, characters warp to the right edge before they finish exiting the left edge.

**Prevention:**
Use `if char.rect.right < 0: char.rect.left = SCREEN_W` for wrap, matching the "fully off left side" semantics. Adjust wrap threshold to match the original feel.

**Phase:** Movement / wrap implementation.

---

### Pitfall 13: Sound Effect Overlap with pygame.mixer.Sound

**What goes wrong:**
The VB6 code plays sound effects through `MediaPlayer1`, which can only play one sound at a time. Playing a new effect interrupts the current one. This is actually the intended behavior — death cry cuts off the laser sound. In pygame, `pygame.mixer.Sound.play()` mixes multiple sounds simultaneously. If the death cry fires while the laser is playing, both sounds play concurrently, which can sound cluttered.

Additionally, if you allocate only 1 mixer channel (`pygame.mixer.set_num_channels(1)`), sounds will cut each other off — matching VB6 behaviour — but this also cuts off background music, which uses a separate `pygame.mixer.music` system.

**Prevention:**
Use 2 dedicated channels: channel 0 for sound effects (one at a time, new sound stops old), channel 1 reserved. Music uses `pygame.mixer.music` (separate from the channel system). Play effects with `channel.play(sound)`, which stops any currently playing effect on that channel.

```python
sfx_channel = pygame.mixer.Channel(0)
sfx_channel.play(laser_sound)   # automatically stops previous SFX
```

**Phase:** Audio implementation.

---

### Pitfall 14: GAttack Uses Wrong Sprite Width for Beam Origin

**What goes wrong:**
In the VB6 source, `GAttack` calculates the beam origin as:
```vb
.intX = imgG.Left + imgS.Width / 2   ' BUG: uses imgS.Width, not imgG.Width
.intY = imgG.Top + imgS.Height / 2   ' BUG: uses imgS.Height, not imgG.Height
```
The Goblin's beam originates from a point offset by Superman's sprite dimensions, not the Goblin's own. If the two sprites are the same size (they are: both 850 twips), this produces the same result. But if you ever give them different sprite sizes during the upscaling process, Goblin's beam will originate from a wrong position.

**Prevention:**
Use `goblin.rect.centerx, goblin.rect.centery` as the beam origin in the Python port. Do not replicate the `imgG + imgS.Width` cross-reference.

**Phase:** Laser / attack implementation.

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Project setup / first render | Twip-to-pixel mismatch (Pitfall 5) | Define canonical resolution (800x600) in constants before writing any position code |
| Asset pipeline | ICO transparency failure (Pitfall 6) | Run Pillow ICO→PNG conversion as first task; verify all sprites show transparency |
| Game loop | Frame-rate-dependent movement (Pitfall 2) | Use `dt = clock.tick(60) / 1000.0`, multiply all movement by `dt` from day one |
| Input system | KEYDOWN vs get_pressed (Pitfall 3), N-Key Rollover (Pitfall 4) | Use `get_pressed()` for movement, `KEYDOWN` for one-shot actions; test with two people |
| Character architecture | Boolean flag state explosion (Pitfall 9) | Define `CharState` enum before writing any movement or death code |
| Rendering | AutoRedraw → clear-then-draw confusion (Pitfall 10) | Pre-bake background surface; blit it first every frame |
| Collision detection | VB6 `Or 4` bug survival (Pitfall 1), line tunneling (Pitfall 7) | Use `in (3, 4)` syntax; use `Rect.clipline()` for beam-character intersection |
| Attack / beams | GAttack wrong origin (Pitfall 14) | Use `goblin.rect.center` not `goblin.pos + superman.size / 2` |
| Audio | Music loop gap (Pitfall 8), SFX overlap (Pitfall 13) | Trim WAV silence post-conversion; use dedicated SFX channel |
| Scoring | Window title overhead (Pitfall 11) | Cache title string, only set_caption on change |
| Horizontal wrap | Off-by-one (Pitfall 12) | Wrap on `rect.right < 0` / `rect.left > SCREEN_W`, not on center crossing |

---

## Sources

- VB6 source: `D:/dev/repo/best-game-ever/_old/frmSuperman.frm` (read directly — line references above are authoritative)
- VB6 source: `D:/dev/repo/best-game-ever/_old/Form1.frm` (read directly)
- pygame documentation knowledge: `pygame.time.Clock`, `pygame.key.get_pressed()`, `pygame.Rect.clipline()`, `pygame.mixer` — HIGH confidence from training knowledge cross-checked against known pygame 2.x API
- Twip conversion: standard formula (1 twip = 1/1440 inch; at 96dpi = 1/15 px) — HIGH confidence
- `pygame.Rect.clipline()`: added in pygame 2.0.0 (released 2020) — verify target pygame version supports this before using
