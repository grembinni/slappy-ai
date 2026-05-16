# Phase 1: Foundation - Research

**Researched:** 2026-05-16
**Domain:** pygame-ce game bootstrap, Pillow ICO→PNG conversion, FluidSynth MIDI→WAV pipeline, Python project scaffolding
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Source files in `raw_assets/` (committed to repo). Do NOT reference `D:\dev\repo\best-game-ever\_old\`.
- **D-02:** Only game-relevant files in `raw_assets/` — exclude unused originals (LITENING.ICO, PLANE.ICO, ROCKET.ICO, tree.bmp, bit.bmp, e.bmp, HobGoblin.cur, Cloud*.ico, unused WAVs: APPLAUSE.WAV, BOILGUY2.WAV, CLAP.WAV, etc.).
- **D-03:** `convert_assets.py` reads `raw_assets/` → writes `assets/`. The `assets/` folder is gitignored (generated output); `raw_assets/` is committed (source of truth).
- **D-04:** Bundle `TimGM6mb.sf2` at `tools/TimGM6mb.sf2` — committed to the repo.
- **D-05:** `convert_assets.py` accepts `--soundfont` CLI arg defaulting to `tools/TimGM6mb.sf2`. Fail clearly if FluidSynth not installed — no silent skipping.
- **D-06:** Phase 1 creates ONLY 5 files: `main.py`, `game.py`, `assets.py`, `settings.py`, `convert_assets.py`. No stubs for `player.py`, `beam.py`, `sound.py`, `hud.py`.

### Claude's Discretion

- Zone dimensions (GROUND_Y, CEILING_H, colors): researcher should check `frmSuperman.frm` for original VB6 proportions and translate to pixel values for the 1280×800 canvas.
- Background image vs. solid color: pre-render a `background_surface` once at startup using `pygame.draw.rect()` for ground and ceiling bands over a filled sky color.
- ICO conversion upscaling: Use Pillow `Image.NEAREST` resampling when scaling 32×32 ICO to 128×128 PNG.

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within Phase 1 scope.

</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ENG-01 | Game runs at fixed 60 FPS loop using `pygame.time.Clock` with `dt = clock.tick(60) / 1000.0` | Game loop skeleton section; verified `clock.tick(60)` returns ms integer in pygame-ce 2.5.7 |
| ENG-02 | `GameState` enum: SPLASH, PLAYING, PAUSED, GAME_OVER | Standard Python `enum.Enum` pattern; Phase 1 skeleton only needs PLAYING state active |
| ENG-03 | All game assets (PNG sprites, WAV sounds) loaded once at startup via `assets.py` into a keyed cache | Asset loading pattern section; key naming convention fully specified |
| ENG-04 | `settings.py` defines all geometry constants: SCREEN_W=1280, SCREEN_H=800, SPRITE_SIZE=128, WIN_SCORE=50, BEAM_SPEED, FPS=60 | VB6 analysis provides all zone constants; full constants list provided |
| ENG-05 | Dev-time conversion script converts .ico sprites to .png (128×128, nearest-neighbor) and .mid music to .wav via FluidSynth | Pillow ICO→PNG verified working; FluidSynth CLI approach documented; full raw_assets manifest derived |

</phase_requirements>

---

## Summary

Phase 1 establishes the five files that every subsequent phase imports from. The work divides into three parallel streams: (1) the asset conversion pipeline (`convert_assets.py` + `raw_assets/`), (2) the constants foundation (`settings.py`), and (3) the game loop skeleton (`main.py` + `game.py` + `assets.py`). All three are independent until the game loop calls `assets.py`, which requires the conversion pipeline to have already run.

The VB6 source has been read directly and all zone proportions, colors, and sprite sets are fully enumerated below. The VB6 background color is cyan (`&H00FFFF00&` = RGB(0, 255, 255)) — not blue as commonly assumed. Ground and ceiling bands are both solid color rectangles: white ceiling, green ground. The pre-baked `background_surface` approach is confirmed by the PITFALLS.md analysis and is non-negotiable for correct beam rendering in later phases.

All five packages (`pygame-ce`, `Pillow`, `pyfluidsynth`, `pyinstaller`, `pytest`) verified clean via slopcheck [OK] against PyPI. Actual current versions: pygame-ce 2.5.7, Pillow 12.2.0, pyfluidsynth 1.3.4, pytest 9.0.3, pyinstaller 6.20.0. FluidSynth (the system CLI) is **not installed** in this environment — the plan must include an install step or note that the developer must install it manually before running `convert_assets.py`.

**Primary recommendation:** Implement in wave order — constants first (settings.py), then asset pipeline (convert_assets.py + raw_assets/ directory), then game skeleton (main.py + game.py + assets.py). All five files must be in place before the Phase 1 success criteria can be verified.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Game loop / clock | Game process (`game.py`) | — | Single `Clock.tick(60)` loop owns all timing |
| Constants / settings | Module (`settings.py`) | — | All geometry/color/speed values imported here by every other module |
| Asset loading / caching | Module (`assets.py`) | — | Load once at startup; surfaces and sounds cached by key |
| Asset conversion pipeline | Dev script (`convert_assets.py`) | — | One-time build step, not runtime |
| Background rendering | Game process (`game.py`) | Pre-baked surface at startup | background_surface blit each frame; ground/ceiling drawn at init time |
| Event dispatch / quit handling | Game process (`game.py`) | — | pygame.QUIT and K_DELETE caught in event loop |
| Window creation | `main.py` (bootstrap) | — | pygame.display.set_mode() called once in main |

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pygame-ce | 2.5.7 | Game window, display, event loop, clock | [VERIFIED: PyPI] Active community fork of pygame; identical API; includes SDL 2.32.10 |
| Pillow | 12.2.0 | ICO→PNG conversion at build time | [VERIFIED: PyPI] Only pure-Python tool that handles ICO AND masks correctly; tested on these specific ICO files |
| Python | 3.11.x | Runtime | [ASSUMED] 3.11 is sweet spot for pygame-ce + PyInstaller support; see STACK.md |

### Supporting (dev-time only)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pyfluidsynth | 1.3.4 | Python bindings for FluidSynth MIDI→WAV | [VERIFIED: PyPI] Used by `convert_assets.py` as alternative to CLI subprocess; see note below |
| pytest | 9.0.3 | Unit tests | [VERIFIED: PyPI] Tests for settings constants, asset loading, convert_assets dry-run |
| pyinstaller | 6.20.0 | Windows .exe packaging | [VERIFIED: PyPI] Phase 6 only; listed here for requirements.txt completeness |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pyfluidsynth Python binding | `subprocess` calling `fluidsynth` CLI | CLI is simpler and has no Python binding dependency; pyfluidsynth is redundant if CLI is available |
| Pillow for ICO→PNG | ImageMagick CLI | Pillow keeps pipeline pure-Python and was verified to work correctly on all ICO files in this repo |
| `clock.tick(60) / 1000.0` | `clock.tick_busy_loop(60) / 1000.0` | `tick_busy_loop` is more precise but uses 100% CPU; not needed for a 60 FPS game |

**Installation (dev machine):**
```bash
pip install pygame-ce==2.5.7
pip install Pillow==12.2.0
pip install pyfluidsynth==1.3.4
pip install pytest==9.0.3
```

**requirements.txt structure:**
```
# requirements.txt — runtime
pygame-ce==2.5.7

# requirements-dev.txt — dev tools
-r requirements.txt
Pillow==12.2.0
pyfluidsynth==1.3.4
pytest==9.0.3
pyinstaller==6.20.0
```

---

## Package Legitimacy Audit

> slopcheck 0.6.1 was installed and run against all five packages.

| Package | Registry | slopcheck | Disposition |
|---------|----------|-----------|-------------|
| pygame-ce | PyPI | [OK] | Approved |
| Pillow | PyPI | [OK] | Approved |
| pyfluidsynth | PyPI | [OK] | Approved |
| pytest | PyPI | [OK] | Approved |
| pyinstaller | PyPI | [OK] | Approved |

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as [SUS]:** none

*Note: These are Python packages; npm postinstall script checks do not apply.*

---

## Architecture Patterns

### System Architecture Diagram

```
[Developer runs convert_assets.py]
  raw_assets/icons/*.ico ─────────────────────────────┐
  raw_assets/sounds/*.wav ──────────────────────────┐  │
  raw_assets/sounds/*.mid ──────────────────────────┤  │
  tools/TimGM6mb.sf2  ──── FluidSynth CLI ──────────┤  │
                                                     ▼  ▼
                                                 assets/sprites/*.png
                                                 assets/sounds/*.wav
                                                     │
                                                     ▼
[User runs python main.py]
  main.py: pygame.init() ──► display.set_mode(1280, 800)
              │
              ▼
  assets.py: load all PNGs → surfaces dict
             load all WAVs → sounds dict
              │
              ▼
  game.py: Game.__init__()
    ├─ pre-bake background_surface (sky fill + ceiling rect + ground rect)
    ├─ state = GameState.PLAYING
    └─ game.run():
         while True:
           dt = clock.tick(60) / 1000.0
           ─── event loop ───
           │  pygame.QUIT → quit
           │  K_DELETE    → quit
           ─── update(dt) ───
           │  (Phase 1: no entities yet)
           ─── draw() ───
              screen.blit(background_surface, (0, 0))
              pygame.display.flip()
```

### Recommended Project Structure

```
slappy-ai/
  main.py               # bootstrap: pygame.init(), create Game, run()
  game.py               # Game class: loop, GameState enum, event dispatch, draw
  assets.py             # AssetCache: load all surfaces and sounds at startup
  settings.py           # ALL constants — edit here only
  convert_assets.py     # dev-time: raw_assets/ → assets/
  raw_assets/
    icons/              # source .ico files (committed)
    sounds/             # source .wav and .mid files (committed)
  tools/
    TimGM6mb.sf2        # bundled soundfont (committed)
  assets/               # gitignored — generated by convert_assets.py
  tests/
    test_settings.py    # constants importable and correct values
    test_assets.py      # asset cache loads without error
    conftest.py         # shared fixtures
  requirements.txt
  requirements-dev.txt
  .gitignore
```

### Pattern 1: Game Loop with dt

```python
# game.py — verified against pygame-ce 2.5.7
# clock.tick(60) returns int milliseconds; divide by 1000.0 for seconds
import pygame
from enum import Enum, auto

class GameState(Enum):
    SPLASH = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

class Game:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.clock = pygame.time.Clock()
        self.state = GameState.PLAYING
        self.background = self._bake_background()

    def _bake_background(self):
        from settings import SCREEN_W, SCREEN_H, CEILING_H, GROUND_Y, SKY_COLOR, CEILING_COLOR, GROUND_COLOR
        surf = pygame.Surface((SCREEN_W, SCREEN_H))
        surf.fill(SKY_COLOR)
        pygame.draw.rect(surf, CEILING_COLOR, (0, 0, SCREEN_W, CEILING_H))
        pygame.draw.rect(surf, GROUND_COLOR, (0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y))
        return surf

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  # seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        running = False
            # Phase 1: no update logic yet
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()
```

### Pattern 2: Pillow ICO→PNG Conversion

```python
# convert_assets.py — verified against Pillow 12.2.0 on actual ICO files
# All ICO files in this repo are 32x32 RGBA; tested: GEvil.ico, SUp1.ico, SDeath.ico, etc.
from PIL import Image
import pathlib

def convert_ico(src: pathlib.Path, dst: pathlib.Path, size: int = 128) -> None:
    """Convert ICO to PNG at target size using NEAREST resampling (pixel art)."""
    with Image.open(src) as img:
        img = img.convert("RGBA")          # handles ICO AND-mask transparency
        img = img.resize((size, size), Image.NEAREST)  # pixel art: no smoothing
        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst, "PNG")
```

**Verified:** All 8 test ICO files open as RGBA (32×32) and resize to (128×128) without error. The `convert("RGBA")` step correctly interprets the ICO AND-mask as alpha channel. [VERIFIED: direct test on actual repo ICO files]

### Pattern 3: Asset Cache

```python
# assets.py — key naming convention for all phases
import pygame
import pathlib
from settings import SPRITE_SIZE

ASSETS_DIR = pathlib.Path(__file__).parent / "assets"

class AssetCache:
    def __init__(self):
        self.sprites: dict[str, pygame.Surface] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self._load_sprites()
        self._load_sounds()

    def _load_sprites(self):
        sprites_dir = ASSETS_DIR / "sprites"
        # Key convention: filename stem, lowercased
        # e.g. "gevil" -> GEvil.png, "sup1" -> SUp1.png
        for png in sprites_dir.glob("*.png"):
            key = png.stem.lower()
            self.sprites[key] = pygame.image.load(str(png)).convert_alpha()

    def _load_sounds(self):
        sounds_dir = ASSETS_DIR / "sounds"
        for wav in sounds_dir.glob("*.wav"):
            key = wav.stem.lower()
            self.sounds[key] = pygame.mixer.Sound(str(wav))
```

**Key naming convention** (lowercase stem of filename):
- `"gevil"`, `"gevil1"`, `"gevil2"`, `"gevil3"` — Goblin air sprites
- `"gup1"`, `"gup2"`, `"gdown1"`, `"gdown2"`, `"gleft1"`, `"gleft2"`, `"gright1"`, `"gright2"` — Goblin directional
- `"gppose"`, `"gppose2"`, `"gdeath"` — Goblin special
- `"gspin1"`, `"gspin2"`, `"gspin3"`, `"gspin4"` — Goblin crash
- `"gevil1"`, `"gevil2"`, `"gevil3"` — GEvil ground walking variants
- `"sup1"`, `"sup2"`, `"sdown1"`, `"sdown2"`, `"sleft1"`, `"sleft2"`, `"sright1"`, `"sright2"` — Superman directional
- `"spose"`, `"sdeath"` — Superman special
- `"sspin1"`, `"sspin2"`, `"sspin3"`, `"sspin4"` — Superman crash
- `"ckent"`, `"ckent1"`, `"ckent2"`, `"ckent3"`, `"ckentintro"` — Superman ground (Clark Kent)
- `"superman"` — Superman idle/intro
- `"laser"`, `"deathcry"`, `"explode"`, `"intro"` — sound effects
- `"passport"`, `"canyon"` — music (WAV converted from MIDI)

### Pattern 4: settings.py Constants

```python
# settings.py — complete Phase 1 constants
# VB6 source: frmSuperman.frm — zone values translated to pixel equivalents

# Display
SCREEN_W = 1280
SCREEN_H = 800
FPS = 60

# Sprites
SPRITE_SIZE = 128   # 4x upscale from 32x32 ICO source

# Background zones
# VB6: intCeiling = 300 twips = ~20px at 96dpi; scaled proportionally to 128px sprites
CEILING_H = 50      # white band: y=0 to y=50
GROUND_Y = 750      # green band: y=750 to y=800 (50px tall)

# Colors — from VB6 source (BackColor = &H00FFFF00& = BBGGRR = cyan)
SKY_COLOR     = (0, 255, 255)   # VB6 BackColor &H00FFFF00& = cyan [VERIFIED: VB6 source]
CEILING_COLOR = (255, 255, 255) # vbWhite
GROUND_COLOR  = (0, 128, 0)     # vbGreen

# Gameplay (Phase 1: define now, used in later phases)
WIN_SCORE  = 50
BEAM_SPEED = 400    # pixels per second [ASSUMED — tunable in Phase 3]

# Direction constants (for later phases — define now for consistency)
DIR_UP    = 1
DIR_DOWN  = 2
DIR_LEFT  = 3
DIR_RIGHT = 4
DIR_POSE  = 5
DIR_IDLE  = 6
```

**VB6 sky color derivation:** `frmSuperman.frm` line 4: `BackColor = &H00FFFF00&`. VB6 OLE color format is `0x00BBGGRR`. Therefore: BB=0xFF, GG=0xFF, RR=0x00 → RGB(0, 255, 255) = cyan. [VERIFIED: VB6 source + Python hex arithmetic]

### Pattern 5: FluidSynth MIDI→WAV via subprocess

**Preferred approach for `convert_assets.py`:** Use `subprocess` to call the FluidSynth CLI rather than the `pyfluidsynth` Python binding. This is simpler, avoids binding version issues, and FluidSynth is explicitly a dev-tool dependency (not runtime).

```python
# In convert_assets.py
import subprocess
import sys
import shutil

def convert_midi_to_wav(midi_path, out_path, soundfont_path):
    """Convert MIDI to WAV using FluidSynth CLI. Fails loudly if not installed."""
    if shutil.which("fluidsynth") is None:
        print("ERROR: FluidSynth is not installed or not on PATH.")
        print("Install: winget install FluidSynth.FluidSynth")
        print("         or: conda install -c conda-forge fluidsynth")
        sys.exit(1)
    subprocess.run([
        "fluidsynth", "-ni",
        str(soundfont_path),
        str(midi_path),
        "-F", str(out_path),
        "-r", "44100"
    ], check=True)
```

**D-05 compliance:** The script accepts `--soundfont` via `argparse`, defaults to `tools/TimGM6mb.sf2`, and calls `sys.exit(1)` with an install hint if `shutil.which("fluidsynth")` returns None.

### Anti-Patterns to Avoid

- **Loading images each frame:** VB6 called `LoadPicture()` in timers. In pygame-ce, `pygame.image.load()` reads from disk; call it only in `AssetCache.__init__()`.
- **Relying on pygame's ICO loader:** pygame's built-in ICO loader is unreliable for transparency. Always use Pillow for ICO→PNG conversion first.
- **Using pygame.SCALED without testing:** pygame-ce 2.5.7 supports `pygame.SCALED` display flag for integer scaling. Do NOT use it in Phase 1 — fixed 1280×800 is simpler and the target monitor is assumed to support this resolution.
- **Drawing beams directly to screen (VB6 pattern):** The VB6 `DrawSLines()` pattern draws with background color to erase. In pygame, use `screen.blit(background_surface, (0,0))` every frame instead.
- **Hardcoding pixel values:** Every numeric value must flow through `settings.py`. The planner should reject any task that writes literal pixel/color values in `.py` files other than `settings.py`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| ICO transparency handling | Custom AND-mask parser | `Image.convert("RGBA")` | ICO format has 1-bit AND mask; Pillow handles it correctly |
| MIDI rendering | Python MIDI parser + waveform synthesis | FluidSynth CLI | MIDI synthesis is a solved problem; hand-rolling is thousands of lines |
| Delta time | Custom frame time accumulator | `clock.tick(60) / 1000.0` | pygame-ce `Clock.tick()` returns ms directly; one line |
| Asset file discovery | Custom directory walker | `pathlib.glob("*.png")` | glob handles all the edge cases |
| PNG loading with alpha | Manual palette parsing | `.convert_alpha()` on loaded Surface | pygame-ce handles pre-multiplied alpha correctly with this call |

**Key insight:** The three hardest parts of Phase 1 (ICO transparency, MIDI synthesis, dt-based timing) are all one-liners using the standard stack. Do not diverge from these patterns.

---

## Raw Assets Manifest

This is the complete list of files required in `raw_assets/` derived from the VB6 source (`frmSuperman.frm`) and Requirements (MOV-09, MOV-10, AUD-01–05). [VERIFIED: VB6 source direct read + Icons/ directory listing]

### raw_assets/icons/ (ICO files — all 32×32)

**Superman sprites** (from `SPose()`, `SCrash()` in frmSuperman.frm):

| File | Used for |
|------|----------|
| SUp1.ico | Superman flying up, frame 1 |
| SUp2.ico | Superman flying up, frame 2 |
| SDown1.ico | Superman flying down, frame 1 |
| SDown2.ico | Superman flying down, frame 2 |
| SLeft1.ICO | Superman flying left, frame 1 |
| SLeft2.ico | Superman flying left, frame 2 |
| SRight1.ico | Superman flying right, frame 1 |
| SRight2.ico | Superman flying right, frame 2 |
| SPose.ico | Superman idle/pose (air) |
| SDeath.ico | Superman death sprite |
| SSpin1.ico | Superman crash spin, frame 1 |
| SSpin2.ico | Superman crash spin, frame 2 |
| SSpin3.ico | Superman crash spin, frame 3 |
| SSpin4.ico | Superman crash spin, frame 4 |
| CKent.ico | Clark Kent pose (ground) |
| CKent1.ico | Clark Kent idle (ground) |
| CKent2.ico | Clark Kent walking, frame 1 |
| CKent3.ico | Clark Kent walking, frame 2 |
| CKentIntro.ico | Clark Kent intro screen |
| Superman.ico | Superman intro sprite |

**Goblin sprites** (from `GPose()`, `GCrash()` in frmSuperman.frm):

| File | Used for |
|------|----------|
| GUp1.ico | Goblin flying up, frame 1 |
| GUp2.ico | Goblin flying up, frame 2 |
| GDown1.ico | Goblin flying down, frame 1 |
| GDown2.ico | Goblin flying down, frame 2 |
| GLeft1.ico | Goblin flying left, frame 1 |
| GLeft2.ico | Goblin flying left, frame 2 |
| GRight1.ico | Goblin flying right, frame 1 |
| GRight2.ico | Goblin flying right, frame 2 |
| GEvil.ico | Goblin idle/pose (air) |
| GEvil1.ico | Goblin idle 2 (ground/intro) |
| GEvil2.ico | GEvil ground walking, frame 1 |
| GEvil3.ico | GEvil ground walking, frame 2 |
| GEvilIntro.ico | Goblin intro screen |
| GDeath.ico | Goblin death sprite |
| GPose.ico | Goblin idle/stand (air, dir=6) |
| GPose2.ico | Goblin pose (air, dir=5) |
| GSpin1.ico | Goblin crash spin, frame 1 |
| GSpin2.ico | Goblin crash spin, frame 2 |
| GSpin3.ico | Goblin crash spin, frame 3 |
| GSpin4.ico | Goblin crash spin, frame 4 |

**Files deliberately excluded** (D-02): LITENING.ICO, PLANE.ICO, ROCKET.ICO, tree.bmp, bit.bmp, e.bmp, HobGoblin.cur, Cloud.ico, Cloud2.ico, Cloud3.ico, Hobgoblin.ico, Hobgoblin2.ico, tree.ico, SDown.ico (duplicate), SRight.ico (duplicate), SDown3.ico (unused), SDownBack.ico (unused), SDownFront.ico (unused), SLDown3.ico (unused), SUp.ico (duplicate)

### raw_assets/sounds/ (WAV/MIDI files)

| File | AUD-REQ | Used for |
|------|---------|---------|
| LASER.WAV | AUD-01 | Laser fire sound effect |
| DeathCry.WAV | AUD-02 | Player hit sound effect |
| EXPLODE.WAV | AUD-03 | Crash landing sound effect |
| passport.mid | AUD-04 | Background music (PLAYING state) → converts to passport.wav |
| canyon.mid | AUD-05 | Intro music (SPLASH state) → converts to canyon.wav |
| Intro.wav | (frmSuperman SoundEffect case 1) | Form load sound — include for completeness |

**Files deliberately excluded** (D-02): APPLAUSE.WAV, BOILGUY2.WAV, CLAP.WAV, DEADGUY4.WAV, FF_BATL.WAV, FF_MSG.WAV, GUNSHOT.WAV, WHOOSH.WAV

**Total raw_assets manifest:** 40 ICO files + 6 sound files = 46 source files

---

## VB6 Zone Analysis

> This section documents the VB6 original values and their pixel translations for `settings.py`. [VERIFIED: VB6 source direct read]

**From `frmSuperman.frm` `New_Game()` subroutine (lines 420–437):**

```vb
intGround = 300        ' twips — height of ground band
intCeiling = 300       ' twips — height of ceiling band
frmForm.Width = 9000   ' twips — form width during gameplay
frmForm.Height = Screen.Height - intGround  ' dynamic
intBaseGroundY = Me.ScaleHeight - intGround - intImgHeight
```

**VB6 backdrop rendering (line 436–437):**
```vb
Line (0, frmForm.ScaleHeight - intGround)-Step(Me.ScaleWidth, Me.ScaleHeight), vbGreen, BF
Line (0, 0)-Step(Me.ScaleWidth, intCeiling), vbWhite, BF
```

**Color translations:**
- `BackColor = &H00FFFF00&` → OLE BGR format → RGB(0, 255, 255) = **cyan sky**
- `vbGreen` = VB6 constant → RGB(0, 128, 0) = **standard green**
- `vbWhite` = VB6 constant → RGB(255, 255, 255) = **white**

**Proportional zone translation to 1280×800:**
- VB6 at 96dpi: 300 twips = 20px; form height ~748px → band proportion ≈ 2.7%
- Our sprites are 128px (vs ~57px original) → scale factor ≈ 2.24x
- Scaled band height: 20px × 2.24 ≈ 45px → round to **50px**
- `CEILING_H = 50` (white band: y=0 to y=50)
- `GROUND_Y = 750` (green band: y=750 to y=800, 50px tall)
- Play area: y=50 to y=750 = **700px tall**, 1280px wide

**`intBaseGroundY` equivalent** (the y at which a sprite "sits on the ground"):
- VB6: `ScaleHeight - intGround - intImgHeight` = form_height - 300 - 850 twips
- Pygame equivalent: `GROUND_Y - SPRITE_SIZE = 750 - 128 = 622` (sprite top when on ground)

---

## Common Pitfalls

### Pitfall 1: pygame.image.load() on ICO files directly

**What goes wrong:** `pygame.image.load("GEvil.ico")` may produce a surface with a black background instead of transparency on Windows, and will break on macOS/Linux.
**Why it happens:** ICO transparency uses AND-mask format, not PNG-style alpha. pygame's ICO loader handles it inconsistently.
**How to avoid:** Always use Pillow ICO→PNG conversion (D-03). Load `.png` files in `assets.py`. Never call `pygame.image.load()` on an `.ico` file.
**Warning signs:** Sprites appear with black or colored rectangles around them.

### Pitfall 2: background_surface not baked at startup

**What goes wrong:** Calling `pygame.draw.rect()` for ground/ceiling bands every frame instead of once at startup, then blitting the result.
**Why it happens:** The VB6 redrew zones when beams erased them; developers replicate this.
**How to avoid:** Pre-bake `background_surface` in `Game.__init__()`. Every frame: `screen.blit(self.background, (0,0))` first.
**Warning signs:** Ground/ceiling redraw overhead noticeable in profiler; or ground band disappears after first blit-without-background.

### Pitfall 3: SKY_COLOR assumed to be blue

**What goes wrong:** Assuming the sky is blue and hardcoding `(135, 206, 235)` or similar.
**Why it happens:** "Sky = blue" is intuitive.
**How to avoid:** Use `SKY_COLOR = (0, 255, 255)` — the VB6 BackColor was cyan. If the user wants to change it, it must change only in `settings.py`.
**Warning signs:** Visual mismatch from the VB6 original.

### Pitfall 4: Twip values copied as pixels

**What goes wrong:** Using VB6's `intGround = 300` or `intImgHeight = 850` directly as pixel values.
**Why it happens:** Easy to miss the twip/pixel distinction.
**How to avoid:** All pixel constants are derived fresh in `settings.py` using the proportional translation documented above.
**Warning signs:** Ground band is 300px tall (takes up 37.5% of screen) or sprites are 850px tall.

### Pitfall 5: FluidSynth failure is silent

**What goes wrong:** `convert_assets.py` silently skips MIDI→WAV conversion if FluidSynth is not installed, producing an incomplete `assets/sounds/` directory. Phase 1 success criterion 3 ("all WAV files exist") fails but only at runtime, not at conversion time.
**Why it happens:** Developers catch the subprocess error and continue.
**How to avoid:** D-05 mandates `sys.exit(1)` with a clear install hint if `shutil.which("fluidsynth")` is None. Do not use a try/except that swallows the error.
**Warning signs:** `assets/sounds/` missing `passport.wav` and `canyon.wav`; game plays silently with no error.

### Pitfall 6: dt used incorrectly (Phase 1 seed)

**What goes wrong:** `dt = clock.tick(60)` without `/ 1000.0`. dt is then in milliseconds, not seconds. Movement in later phases is 1000x too fast.
**Why it happens:** Forgetting the division; the VB6 code used timer intervals in ms too.
**How to avoid:** Always `dt = clock.tick(60) / 1000.0`. Establish this in Phase 1's game loop skeleton and never change it.
**Warning signs:** Characters fly off-screen instantly in Phase 2.

---

## Code Examples

### Verified: clock.tick() returns integer ms

```python
# Verified against pygame-ce 2.5.7:
# clock.tick(60) returns int (e.g., 17 for ~60Hz)
# Divide by 1000.0 to get seconds as float
dt = clock.tick(60) / 1000.0  # seconds per frame
```

### Verified: Rect.clipline() API

```python
# Verified against pygame-ce 2.5.7:
# r.clipline(x1, y1, x2, y2) returns:
#   ((cx1,cy1),(cx2,cy2)) if line intersects rect
#   () (empty tuple) if no intersection
r = pygame.Rect(100, 100, 50, 50)
r.clipline(0, 125, 200, 125)   # → ((100, 125), (149, 125))
r.clipline(0, 0, 10, 10)       # → ()
```

### Verified: ICO→PNG pipeline

```python
# Verified against Pillow 12.2.0 on all repo ICO files:
# All ICO files are 32x32 RGBA — no size selection needed
from PIL import Image
img = Image.open("GEvil.ico")      # opens as RGBA (32, 32) automatically
img = img.convert("RGBA")          # ensures alpha channel present
img = img.resize((128, 128), Image.NEAREST)  # pixel art upscaling
img.save("GEvil.png", "PNG")
# Result: (128, 128) RGBA PNG — pygame.image.load().convert_alpha() compatible
```

### convert_assets.py CLI structure

```python
# argparse skeleton for D-05 compliance
import argparse
import pathlib

def main():
    parser = argparse.ArgumentParser(description="Convert raw_assets/ to assets/")
    parser.add_argument(
        "--soundfont",
        type=pathlib.Path,
        default=pathlib.Path("tools/TimGM6mb.sf2"),
        help="Path to .sf2 soundfont (default: tools/TimGM6mb.sf2)"
    )
    args = parser.parse_args()
    # ... conversion logic
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `pygame.image.load("sprite.ico")` | Pillow ICO→PNG + `pygame.image.load("sprite.png")` | pygame 2.x era | Reliable transparency on all platforms |
| VB6 per-beam erase via background-color draw | `screen.blit(background_surface, (0,0))` each frame | pygame paradigm shift | Simpler, correct, no artifacts |
| Separate timers per subsystem (VB6) | Single `Clock.tick(60)` loop with dt | pygame idiom | Frame-rate-independent, deterministic |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `BEAM_SPEED = 400` pixels/sec | Pattern 4 (settings.py) | Phase 3 may need tuning; value is a placeholder — the actual feel is only verifiable in Phase 3 |
| A2 | Python 3.11 is the target runtime | Standard Stack | If developer uses 3.12/3.13/3.14, pip install of pygame-ce works but PyInstaller 6.x may have edge cases |
| A3 | `Intro.wav` should be included in raw_assets/ | Raw Assets Manifest | It is referenced in frmSuperman SoundEffect case 1 but not in REQUIREMENTS.md AUD-01–05; Phase 5 may not use it |
| A4 | `vbGreen` = RGB(0, 128, 0) | VB6 Zone Analysis | VB6's vbGreen is defined as 0x008000 = (0,128,0); this is a standard VB6 constant, not configurable |

**If this table is empty:** It is not — four assumptions are listed above for planner confirmation.

---

## Open Questions

1. **Python version for the project**
   - What we know: The developer's default Python is 3.14.5; `pip install` runs on Python 3.11 (found at `C:\Users\jerem\AppData\Local\Programs\Python\Python311\`).
   - What's unclear: Should the project target Python 3.11 explicitly, or is 3.14 acceptable? pygame-ce 2.5.7 was installed for Python 3.11 in this session.
   - Recommendation: Create a virtual environment pinned to Python 3.11 and document this in README or .python-version file. The Phase 1 plan should include `python -m venv` using the 3.11 executable explicitly.

2. **FluidSynth installation**
   - What we know: FluidSynth is NOT installed in this environment (`shutil.which("fluidsynth")` returns None).
   - What's unclear: Is this a gap the developer needs to fill before Phase 1 is complete, or should `convert_assets.py` have a `--skip-midi` flag for iterative development?
   - Recommendation: The plan must include a FluidSynth install step as a prerequisite task (Wave 0 or task 0). `convert_assets.py` should have a `--skip-midi` flag that skips WAV conversion but warns clearly, so developers can test the ICO pipeline independently.

3. **Goblin green beam color**
   - What we know: VB6 uses `&H80FF&` for Goblin beams (line 1239: `Line (...), &H80FF&`). In OLE color: `0x000080FF` = RGB(255, 128, 0) = **orange**, not green.
   - What's unclear: Was this intentional? REQUIREMENTS.md CMB-04 says "Goblin beams render as green lines."
   - Recommendation: Use green `(0, 200, 0)` per REQUIREMENTS.md (CMB-04). The VB6 `&H80FF&` may have been a debugging artifact or error. This is Phase 3 work but the color constant should be defined in `settings.py` in Phase 1. [ASSUMED]

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.11 | All code | Yes (at Python311 path) | 3.11.2 | Use 3.11 venv explicitly |
| pygame-ce | game loop, display | Yes (installed) | 2.5.7 | — |
| Pillow | convert_assets.py ICO→PNG | Yes (installed) | 12.2.0 | — |
| pyfluidsynth | convert_assets.py (optional) | Yes (installed) | 1.3.4 | Use CLI subprocess instead |
| FluidSynth CLI | convert_assets.py MIDI→WAV | **NO** | — | `winget install FluidSynth.FluidSynth` or `conda install -c conda-forge fluidsynth` |
| pytest | test suite | Yes (installed) | 9.0.3 | — |
| ffmpeg | optional MIDI WAV trimming | Unknown | — | Skip silence trimming; acceptable for Phase 1 |

**Missing dependencies with no fallback:**
- FluidSynth CLI: required to convert `passport.mid` and `canyon.mid` to WAV. Without it, Phase 1 success criterion 3 ("all WAV files exist in assets/") cannot pass. The plan must include a FluidSynth install task.

**Missing dependencies with fallback:**
- ffmpeg: only needed for trailing silence trimming of converted WAVs (Pitfall 8 in PITFALLS.md). Acceptable to skip in Phase 1; address in Phase 5 if looping artifacts appear.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3 |
| Config file | `pytest.ini` or `pyproject.toml [tool.pytest]` — Wave 0 creates this |
| Quick run command | `python -m pytest tests/ -x -q` |
| Full suite command | `python -m pytest tests/ -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ENG-01 | `clock.tick(60)` returns ms; `dt = result / 1000.0` is float in range | unit | `pytest tests/test_settings.py::test_fps_constant -x` | No — Wave 0 |
| ENG-02 | `GameState` enum has SPLASH, PLAYING, PAUSED, GAME_OVER members | unit | `pytest tests/test_settings.py::test_gamestate_enum -x` | No — Wave 0 |
| ENG-03 | `AssetCache` loads without error when `assets/` is populated | integration | `pytest tests/test_assets.py::test_asset_cache_loads -x` | No — Wave 0 |
| ENG-04 | All six constants importable with correct values | unit | `pytest tests/test_settings.py::test_constants -x` | No — Wave 0 |
| ENG-05 | `convert_assets.py --dry-run` lists expected files without writing | unit | `pytest tests/test_convert.py::test_dry_run -x` | No — Wave 0 |

**Note on ENG-03:** Testing `AssetCache` requires `assets/` to already exist (i.e., `convert_assets.py` must have run successfully). This is an integration test, not a pure unit test. The test should be skipped with `pytest.mark.skipif` if `assets/sprites/` does not exist.

### Sampling Rate

- **Per task commit:** `python -m pytest tests/test_settings.py -x -q`
- **Per wave merge:** `python -m pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_settings.py` — covers ENG-01, ENG-02, ENG-04
- [ ] `tests/test_assets.py` — covers ENG-03 (with skipif guard)
- [ ] `tests/test_convert.py` — covers ENG-05 (dry-run mode)
- [ ] `tests/conftest.py` — shared fixtures (assets path, temp dir)
- [ ] `pytest.ini` or `pyproject.toml [tool.pytest.ini_options]`

---

## Security Domain

> Phase 1 is a local single-player dev bootstrap with no network, authentication, or user data. Security enforcement applies minimally.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | N/A — local game, no auth |
| V3 Session Management | No | N/A |
| V4 Access Control | No | N/A |
| V5 Input Validation | Minimal | argparse handles CLI arg validation for `--soundfont` path |
| V6 Cryptography | No | N/A |

### Known Threat Patterns for This Phase

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Path traversal via `--soundfont` | Tampering | `pathlib.Path.resolve()` and `exists()` check before passing to FluidSynth |
| Malformed ICO file | Spoofing | Pillow raises `UnidentifiedImageError`; wrap in try/except with clear error message |

---

## Sources

### Primary (HIGH confidence)
- `d:/dev/repo/best-game-ever/_old/frmSuperman.frm` — VB6 source direct read: zone constants, sprite names, color values, sound file names (lines 312–1438)
- `d:/dev/repo/best-game-ever/_old/Icons/` — ICO file directory listing: full manifest of available files
- `d:/dev/repo/best-game-ever/_old/Sounds/` — WAV/MIDI file directory listing: full manifest
- `pip index versions pygame-ce` — confirmed 2.5.7 as latest [VERIFIED: PyPI registry]
- `pip index versions Pillow` — confirmed 12.2.0 as latest [VERIFIED: PyPI registry]
- `pip index versions pytest` — confirmed 9.0.3 as latest [VERIFIED: PyPI registry]
- `pip index versions pyfluidsynth` — confirmed 1.3.4 as latest [VERIFIED: PyPI registry]
- `pip index versions pyinstaller` — confirmed 6.20.0 as latest [VERIFIED: PyPI registry]
- `slopcheck install pygame-ce Pillow pyfluidsynth pyinstaller pytest` — all 5 packages rated [OK]
- pygame-ce 2.5.7 runtime verification: `clock.tick(60)` return type, `Rect.clipline()` API, `pygame.SCALED` flag
- Pillow 12.2.0 verification: ICO→RGBA→NEAREST resize on 8 actual repo ICO files

### Secondary (MEDIUM confidence)
- `.planning/research/STACK.md` — pygame-ce vs pygame rationale, FluidSynth approach
- `.planning/research/ARCHITECTURE.md` — VB6 component analysis, pygame patterns
- `.planning/research/PITFALLS.md` — ICO loading, background baking, dt scaling

### Tertiary (LOW confidence)
- [ASSUMED] `BEAM_SPEED = 400` — placeholder value, tunable in Phase 3
- [ASSUMED] Goblin beam color should be green per REQUIREMENTS.md CMB-04, not VB6's `&H80FF&` (orange)

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all versions verified against PyPI registry; packages slopcheck-cleared; tested on this machine
- Architecture: HIGH — patterns derived from VB6 source and verified against running pygame-ce 2.5.7 instance
- Pitfalls: HIGH — derived from direct VB6 source read and runtime verification
- Zone constants: HIGH — computed from VB6 source with verified color decoding and proportional scaling

**Research date:** 2026-05-16
**Valid until:** 2026-06-16 (30 days — stable stack)
