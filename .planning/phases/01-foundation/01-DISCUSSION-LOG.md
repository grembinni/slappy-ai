# Phase 1: Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 1-Foundation
**Areas discussed:** Asset source path, FluidSynth soundfont, Module scaffolding scope

---

## Asset source path

| Option | Description | Selected |
|--------|-------------|----------|
| Hardcode D:\dev\repo\best-game-ever\_old\ | Simple, works on developer's machine only | |
| CLI arg with hardcoded default | convert_assets.py --src with default path baked in | |
| Copy files to raw_assets/ first | User copies originals into raw_assets/ folder | ✓ |

**User's choice:** "copy the sound file into this project" → commit raw source files to `raw_assets/`

**Notes:** User then clarified: committed to repo (not gitignored local staging). Only game-relevant files (not unused ICOs like LITENING, PLANE, ROCKET, unused WAVs). Researcher derives exact manifest from REQUIREMENTS.md sprite/sound lists.

---

## FluidSynth soundfont

| Option | Description | Selected |
|--------|-------------|----------|
| Hardcode a default path | Baked-in path to user's local soundfont | |
| Env var (FLUIDSYNTH_SOUNDFONT) | Portable, no path in code | |
| Skip for Phase 1 | Add placeholder arg, fail clearly if missing | |
| Bundle TimGM6mb.sf2 | ~6MB free soundfont committed to tools/ | ✓ |

**User's choice:** "that works" — confirmed bundling `tools/TimGM6mb.sf2` with `--soundfont` CLI arg defaulting to it.

**Notes:** User asked if the script could download a soundfont automatically. Claude explained bundling is simpler and more reliable. TimGM6mb.sf2 is public domain and small enough to commit.

---

## Module scaffolding scope

| Option | Description | Selected |
|--------|-------------|----------|
| All 9 stubs upfront | Create all modules now, establishes full layout from day 1 | |
| Only what Phase 1 needs | Create only main.py, game.py, assets.py, settings.py, convert_assets.py | ✓ |

**User's choice:** Only what Phase 1 needs.

**Notes:** player.py, beam.py, sound.py, hud.py will be created when those phases are implemented.

---

## Claude's Discretion

- **Zone dimensions (GROUND_Y, CEILING_H, colors):** User did not select this area for discussion. Claude to derive from VB6 source (`frmSuperman.frm`) during planning. Reasonable defaults: CEILING_H=50, GROUND_Y=750 for 1280×800 canvas.

## Deferred Ideas

None — discussion stayed within Phase 1 scope.
