---
plan: 01-01
status: complete
completed: 2026-05-16
---

# Plan 01-01 Summary — Project Scaffold

## What was built
- `settings.py` — all 14 Phase 1 constants verified importable and correct
- `requirements.txt` — pinned to `pygame-ce==2.5.7` (runtime only)
- `requirements-dev.txt` — extends requirements.txt with Pillow, pyfluidsynth, pytest, pyinstaller at exact versions
- `.gitignore` — excludes `assets/`, `dist/`, `build/`, `__pycache__/`, etc.; does NOT exclude `raw_assets/` or `tools/`
- `pytest.ini` — configures `testpaths = tests` with `-x -q` addopts

## Verification
All assertions in plan passed: `settings.py OK`, `Scaffold OK`

## Key decisions
- SKY_COLOR = (0, 255, 255) — VB6 OLE BGR decoding of &H00FFFF00& = cyan
- CEILING_H = 50, GROUND_Y = 750 — 50px bands at top and bottom of 800px canvas
- SPRITE_SIZE = 128 — 4x upscale from 32x32 ICO source
