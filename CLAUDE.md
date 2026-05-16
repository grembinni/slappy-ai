# Goblin vs. Superman — Project Guide

## Project

A Python/pygame-ce port of a VB6 2-player arcade brawler. Two players share a keyboard, fly around, shoot laser beams, and score points. See `.planning/PROJECT.md` for full context.

## Tech Stack

- Python 3.11 + pygame-ce 2.5.x
- Pillow (dev-time: ICO→PNG conversion)
- FluidSynth (dev-time: MIDI→WAV conversion)
- PyInstaller 6.x (packaging)
- pytest 7.x (testing)

## Key Constraints

- All geometry constants in `settings.py` — never hardcode pixel values
- Use `pygame.key.get_pressed()` for movement, `KEYDOWN` only for one-shot actions
- Beam collision must use `if beam.direction in (LEFT, RIGHT):` — never `or RIGHT` (VB6 Or-bug fix)
- All position increments must be multiplied by `dt` (delta-time) for frame-rate independence
- Do not use `pygame.sprite.Sprite`/`Group` — plain classes with `update(dt)` / `draw(screen)`

## GSD Workflow

This project uses the GSD (Get Shit Done) planning workflow.

### Current State

See `.planning/STATE.md` for current phase and status.

### Planning Files

| File | Purpose |
|------|---------|
| `.planning/PROJECT.md` | Project context and requirements |
| `.planning/REQUIREMENTS.md` | All v1 requirements with REQ-IDs |
| `.planning/ROADMAP.md` | 6-phase roadmap |
| `.planning/STATE.md` | Current phase and progress |
| `.planning/config.json` | Workflow preferences |
| `.planning/research/` | Domain research (stack, features, architecture, pitfalls) |

### Commands

```
/gsd:discuss-phase 1    # Gather context before planning Phase 1
/gsd:plan-phase 1       # Create PLAN.md for Phase 1
/gsd:execute-phase 1    # Execute Phase 1 plans
/gsd:verify-work        # Verify phase goals were achieved
/gsd:progress           # Check current status
```

### Workflow per Phase

1. `/gsd:discuss-phase N` — clarify approach
2. `/gsd:plan-phase N` — create detailed PLAN.md
3. `/gsd:execute-phase N` — implement
4. `/gsd:verify-work` — confirm requirements met
5. Move to next phase

## File Layout (Target)

```
slappy-ai/
  main.py          # bootstrap only
  game.py          # main loop, GameState enum, event dispatch
  player.py        # Player class, CharState enum, sprite selection
  beam.py          # Beam class, travel, wrap, collision
  sound.py         # SoundManager
  assets.py        # load and cache all surfaces/sounds at startup
  hud.py           # in-game score overlay
  settings.py      # all constants — edit here, never elsewhere
  convert_assets.py  # dev-time ICO→PNG + MIDI→WAV conversion script
  assets/          # converted PNGs and WAVs (gitignored source ICOs)
  .planning/       # GSD planning artifacts
```
