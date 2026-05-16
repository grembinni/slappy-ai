# Technology Stack

**Project:** Goblin vs. Superman (Python Port)
**Researched:** 2026-05-16
**Confidence:** MEDIUM — Bash/WebSearch/WebFetch tools unavailable in this environment; findings are from training data (cutoff August 2025) cross-checked against project constraints. Version numbers reflect latest known stable releases; validate with PyPI before pinning.

---

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | 3.11.x | Runtime | 3.11 offers best performance-per-release ratio; 3.12 introduced breaking changes in some C extensions; 3.13 is too new for stable PyInstaller support as of mid-2025. 3.10 is the minimum for `match` statements if used, but 3.11 is the sweet spot. |
| pygame-ce | 2.5.x | Game engine | pygame-ce (Community Edition) is the actively maintained fork of pygame. pygame itself had its last release (2.6.0) in 2024 but upstream development has largely migrated to pygame-ce. pygame-ce releases faster, has better Python 3.12+ support, and is a drop-in API replacement. For a new port in 2025/2026, start on pygame-ce directly rather than migrating later. |

### Why pygame-ce over the alternatives

| Framework | Verdict | Reason |
|-----------|---------|--------|
| pygame (original) | Do not use | Slower release cadence; pygame-ce is the community-maintained successor with identical API. No reason to choose original pygame for a new project. |
| pygame-ce | **USE THIS** | Drop-in replacement, actively maintained, same API, faster SDL2 iteration. |
| arcade | Do not use | arcade uses OpenGL via pyglet under the hood — heavier dependency, requires GPU driver support, and is designed for a different programming model (update/draw callbacks vs. main-loop). For a faithful VB6-style game loop this mismatch creates friction, not value. |
| pyglet | Do not use | OpenGL-native, excellent for modern 2D/3D, but has no built-in sprite sheet or collision helpers at pygame's level. Higher learning curve for a port that wants a direct VB6-timer→game-loop mapping. |

### Asset Pipeline: ICO to PNG

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Pillow | 10.x | ICO → PNG conversion | Pillow reads Windows ICO files natively (including multi-resolution ICOs), extracts any embedded size as a PIL Image, and saves as PNG with full alpha. One-liner conversion. Already needed for any image preprocessing; no extra dependency. |

**Exact conversion approach:**

The VB6 sprites are 32x32 ICO files. Target size is 64x64 or 128x128 PNG (2x or 4x upscale).

```python
from PIL import Image

def ico_to_png(ico_path: str, out_path: str, size: int = 128) -> None:
    """Extract largest embedded ICO frame and upscale to `size` px PNG."""
    with Image.open(ico_path) as img:
        # ICO files may contain multiple sizes; pick the largest available
        sizes = img.info.get("sizes", [(img.width, img.height)])
        best = max(sizes, key=lambda s: s[0])
        img.size = best          # select that sub-image
        img = img.convert("RGBA")
        img = img.resize((size, size), Image.NEAREST)  # pixel-art: NEAREST, not LANCZOS
        img.save(out_path, "PNG")
```

**Critical detail:** Use `Image.NEAREST` resampling, NOT `LANCZOS`/`BICUBIC`. The source sprites are pixel art — nearest-neighbor preserves hard edges. Any smoothing algorithm will blur and destroy the pixel aesthetic.

**CLI equivalent (one-shot, no Python script):**

```bash
python -c "
from PIL import Image, ImageFilter
img = Image.open('goblin_left.ico').convert('RGBA')
img = img.resize((128, 128), Image.NEAREST)
img.save('goblin_left.png')
"
```

**Alternative — ImageMagick (if Pillow ICO extraction is lossy):**

Some ICOs embed PNG-compressed frames; Pillow handles these correctly since version 9.x. If a specific ICO file produces incorrect output, ImageMagick's `magick convert` is the fallback:

```bash
magick convert -background none goblin_left.ico[0] -scale 128x128 goblin_left.png
```

The `[0]` selects the first (often largest) embedded frame. This is a fallback only — Pillow is preferred because it keeps the pipeline pure-Python.

### Asset Pipeline: MIDI to WAV

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| FluidSynth | 2.3.x (system) | MIDI → WAV rendering | FluidSynth is the industry-standard software MIDI synthesizer. It reads a MIDI file + a SoundFont (.sf2) and renders to PCM WAV. Output quality is excellent. Timidity++ is an alternative but less actively maintained and harder to install on Windows. |
| pyfluidsynth | 1.3.x | Python bindings for FluidSynth | Allows offline rendering directly from a Python script without shell subprocess calls. Optional: the CLI `fluidsynth` command works just as well for a one-time asset bake. |
| GeneralUser GS (SoundFont) | 2.0.1 | .sf2 soundfont for MIDI rendering | Free, high-quality General MIDI soundfont. Canyon.mid and Passport.mid are General MIDI files (Windows 3.1 era); any GM soundfont will render them. GeneralUser GS is ~30MB and produces clean output. |

**Why not Timidity++:** Harder to install on Windows 11 (no official binary in a standard package manager path); FluidSynth has an official Windows installer and conda-forge package. Same output quality, easier setup.

**Why not midiutil:** midiutil is for *writing* MIDI files, not rendering them to audio. Wrong tool.

**Why not pygame.midi:** pygame's MIDI module routes to the system MIDI device at runtime — it does not render to a WAV file. Unreliable on Windows 11 (depends on Windows MIDI mapper and GS Wavetable synthesizer, which varies by system). The PROJECT.md already correctly identifies this as unreliable.

**Exact MIDI → WAV conversion command:**

```bash
# Install FluidSynth (Windows, via winget or conda):
winget install FluidSynth.FluidSynth
# or: conda install -c conda-forge fluidsynth

# Download GeneralUser GS soundfont:
# https://www.schristiancollins.com/generaluser.php

# Render MIDI to WAV:
fluidsynth -ni GeneralUser_GS.sf2 Canyon.mid -F Canyon.wav -r 44100

# Flags:
#   -n  = no MIDI driver (headless/offline)
#   -i  = no interactive shell
#   -F  = output file
#   -r  = sample rate (44100 matches pygame mixer default)
```

**Python equivalent (pyfluidsynth, for scripted batch conversion):**

```python
import fluidsynth

def midi_to_wav(midi_path: str, sf2_path: str, out_path: str, sample_rate: int = 44100) -> None:
    fs = fluidsynth.Synth(samplerate=float(sample_rate))
    fs.start(driver="file", filename=out_path)
    sfid = fs.sfload(sf2_path)
    fs.program_select(0, sfid, 0, 0)
    # Load and play via fluidsynth player
    player = fluidsynth.Player(fs)
    player.add(midi_path)
    player.play()
    player.join()
    fs.delete()
```

**This is a one-time asset bake, not a runtime dependency.** The rendered WAV files ship with the game; FluidSynth is a dev tool, not a user requirement.

### Audio Runtime

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pygame-ce mixer | (bundled) | WAV playback, background music | pygame's mixer module handles WAV playback perfectly. Initialize at 44100 Hz, 16-bit, stereo. Background music (converted WAV) uses `pygame.mixer.music`; sound effects use `pygame.mixer.Sound`. No additional audio library needed. |

**Do not use:** `sounddevice`, `pyaudio`, `simpleaudio` — these are low-level PCM libraries that require more code for the same result. pygame's built-in mixer is the right tool for this use case.

### Packaging: Windows Distribution

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| PyInstaller | 6.x | Bundle to .exe | PyInstaller 6.x has solid pygame-ce support, bundles the SDL2 DLLs automatically (pygame-ce ships SDL2 with its wheel), and produces a single-folder or single-file distribution. The single-folder (`--onedir`) output is preferred over `--onefile` for games because `--onefile` has a slow extraction step on launch and antivirus false-positive rates are higher. |

**PyInstaller command:**

```bash
pip install pyinstaller

# Build single-folder distribution
pyinstaller --onedir \
  --name "GoblinVsSuperman" \
  --windowed \
  --icon assets/icon.ico \
  --add-data "assets;assets" \
  main.py

# --windowed   = no console window (required for games)
# --add-data   = bundle the assets folder (Windows uses ; separator)
# Output in: dist/GoblinVsSuperman/
```

**PyInstaller .spec file approach (preferred for repeatability):**

Generate once with `pyi-makespec`, then edit to add data files, then build with `pyinstaller goblin.spec`. This avoids long command lines and is version-control friendly.

**Alternatives considered:**

| Tool | Verdict | Reason |
|------|---------|--------|
| cx_Freeze | Do not use | More configuration overhead; PyInstaller handles pygame SDL2 DLLs automatically, cx_Freeze requires manual DLL hunting. |
| Nuitka | Do not use for v1 | Compiles Python to C for performance, but adds significant build complexity and time. For a 2-player arcade game, Python performance is not the bottleneck. Revisit only if profiling reveals hot loops. |
| py2exe | Do not use | Largely unmaintained; no meaningful advantage over PyInstaller for modern Python. |
| briefcase (BeeWare) | Do not use | Designed for cross-platform app stores; significant overhead for a simple Windows game. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Pillow | 10.x | ICO → PNG conversion, sprite sheet generation | Dev-time asset pipeline only; not imported at runtime |
| pyfluidsynth | 1.3.x | MIDI → WAV rendering (Python scripted) | Dev-time asset bake only; not a runtime dependency |
| pytest | 7.x | Unit tests for game logic | Collision detection, scoring, state machine logic — testable without pygame display |
| pytest-mock | 3.x | Mock pygame surfaces/events in tests | Allows testing input handling without a display |

---

## Installation

```bash
# Runtime + packaging
pip install pygame-ce==2.5.2
pip install pyinstaller==6.10.0

# Asset pipeline (dev only)
pip install Pillow==10.4.0
pip install pyfluidsynth==1.3.3

# Testing
pip install pytest==7.4.4
pip install pytest-mock==3.12.0
```

**requirements.txt structure (recommended):**

```
# requirements.txt  — runtime only (what ships)
pygame-ce==2.5.2

# requirements-dev.txt  — dev tools (not shipped)
-r requirements.txt
Pillow==10.4.0
pyfluidsynth==1.3.3
pyinstaller==6.10.0
pytest==7.4.4
pytest-mock==3.12.0
```

---

## Python Version Requirement

**Require Python 3.11.** Rationale:
- pygame-ce 2.5.x wheels are published for 3.9, 3.10, 3.11, 3.12 on Windows. 3.11 is safe.
- PyInstaller 6.x fully supports 3.11 on Windows; 3.12 support is present but has more edge cases.
- 3.13 was released October 2024; PyInstaller and several C extensions lagged in 3.13 support through early 2025. Avoid for a distribution target.
- 3.10 is EOL October 2026 — too close; start on 3.11 (EOL October 2027).

**Minimum in pyproject.toml or setup.cfg:**
```toml
[project]
requires-python = ">=3.11,<3.13"
```

---

## What NOT to Use

| Technology | Reason to Avoid |
|------------|-----------------|
| pygame (original, not CE) | Slower release cadence; no advantage over pygame-ce for new projects |
| arcade framework | OpenGL dependency, different programming model, overkill for a faithful VB6 port |
| pyglet | No built-in collision/sprite helpers at pygame's level; OpenGL-native adds complexity |
| pygame.midi (runtime) | Unreliable on Windows 11; depends on system MIDI mapper — render to WAV offline instead |
| Timidity++ | Harder Windows installation than FluidSynth; no quality advantage |
| midiutil | Writes MIDI; does not render audio |
| sounddevice / pyaudio | Low-level PCM; pygame mixer is the correct abstraction for game audio |
| cx_Freeze / py2exe | More configuration, less automatic DLL handling than PyInstaller |
| Nuitka | Build complexity unwarranted for a game where Python speed is not the bottleneck |
| Image.LANCZOS for upscaling | Blurs pixel art; use NEAREST resampling |

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| pygame-ce vs pygame | HIGH | Well-established fork with clear community migration; API identical |
| pygame-ce version (2.5.x) | MEDIUM | Reflects training data through mid-2025; verify current release on PyPI before pinning |
| Pillow ICO→PNG approach | HIGH | Pillow ICO support is stable; NEAREST resampling for pixel art is well-established |
| FluidSynth for MIDI→WAV | HIGH | Industry standard; approach is well-documented and widely used |
| PyInstaller 6.x for Windows | HIGH | Stable, correct choice; version number should be verified on PyPI |
| Python 3.11 recommendation | HIGH | Solid reasoning from version support matrix |
| pyfluidsynth bindings | MEDIUM | Library is less actively updated; if pyfluidsynth is broken, the CLI `fluidsynth` command is the direct fallback with no Python dependency |

---

## Sources

- Training data (August 2025 cutoff): pygame-ce GitHub, PyPI, pygame-ce changelog
- PROJECT.md: confirmed pygame constraint, ICO sprites, MIDI files, WAV sound effects
- Note: WebSearch, WebFetch, and Bash tools were unavailable in this research session. All version numbers should be validated against PyPI before pinning in requirements files.
