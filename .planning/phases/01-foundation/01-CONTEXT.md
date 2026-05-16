# Phase 1: Foundation - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Bootstrap the project: asset conversion pipeline, constants, game loop skeleton, background renders in window. No gameplay — just: window opens, background (sky + ceiling band + ground band) displays, all PNG sprites and WAV files exist in `assets/`, window closes cleanly.

**Requirements in scope:** ENG-01, ENG-02, ENG-03, ENG-04, ENG-05
**Out of scope:** Any player movement, input handling, beams, scoring, audio playback (those are Phases 2–5)

</domain>

<decisions>
## Implementation Decisions

### Asset Source — raw_assets/ folder
- **D-01:** Original source files (ICO sprites, MIDI music) are committed to the repo in a `raw_assets/` folder. Do NOT reference the external `D:\dev\repo\best-game-ever\_old\` path — that path is local-only and not portable.
- **D-02:** Only game-relevant files go in `raw_assets/` — exclude unused originals (LITENING.ICO, PLANE.ICO, ROCKET.ICO, tree.bmp, bit.bmp, e.bmp, HobGoblin.cur, Cloud*.ico, and unused WAVs like APPLAUSE.WAV, BOILGUY2.WAV, CLAP.WAV, etc.). The researcher must derive the exact manifest from REQUIREMENTS.md sprite/sound lists (MOV-09, MOV-10, CMB-01–04, AUD-01–05) and PITFALLS.md.
- **D-03:** `convert_assets.py` reads from `raw_assets/` and writes converted files to `assets/`. The `assets/` folder is gitignored (generated output); `raw_assets/` is committed (source of truth).

### FluidSynth Soundfont
- **D-04:** Bundle a free public-domain soundfont (`TimGM6mb.sf2`, ~6 MB) at `tools/TimGM6mb.sf2` — committed to the repo.
- **D-05:** `convert_assets.py` accepts a `--soundfont` CLI arg that defaults to `tools/TimGM6mb.sf2`. If FluidSynth is not installed, fail clearly with an installation hint rather than silently skipping.

### Module Scaffolding
- **D-06:** Phase 1 creates only the five files needed to hit success criteria: `main.py`, `game.py`, `assets.py`, `settings.py`, `convert_assets.py`. Do NOT create stubs for `player.py`, `beam.py`, `sound.py`, or `hud.py` — those are added in their respective phases.

### Claude's Discretion
- **Zone dimensions (GROUND_Y, CEILING_H, colors):** Not specified by the user — researcher should check `frmSuperman.frm` for the original VB6 proportions and translate to pixel values for the 1280×800 canvas. Reasonable starting point: `CEILING_H = 50`, `GROUND_Y = 750` (leaving 800px total with 50px bands at top and bottom). Colors: white ceiling, green ground, blue sky — check VB6 source for exact RGB values. All must be defined in `settings.py`, never hardcoded elsewhere.
- **Background image vs. solid color:** The original used solid colored bands (no background image). Pre-render a `background_surface` once at startup using `pygame.draw.rect()` for ground and ceiling bands over a filled sky color. See PITFALLS.md Pitfall 10.
- **ICO conversion upscaling:** Use Pillow `Image.NEAREST` resampling when scaling from 32×32 ICO to 128×128 PNG. Already decided in STATE.md.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` §Core Engine — ENG-01 through ENG-05 define Phase 1 deliverables exactly
- `.planning/ROADMAP.md` §Phase 1 — success criteria are the acceptance test; all 5 must pass

### Project Constraints
- `CLAUDE.md` — ALL key constraints: geometry constants in settings.py only, no hardcoded pixels, dt-scaling, `pygame.key.get_pressed()` for movement, beam collision syntax, no pygame.sprite.Sprite. **Non-negotiable.**
- `.planning/PROJECT.md` §Constraints — stack, asset source, faithfulness rules

### Pitfalls (read before writing any Phase 1 code)
- `.planning/research/PITFALLS.md` §Pitfall 5 — Twip-to-pixel mismatch: do NOT copy VB6 twip values as pixels. Define canonical pixel constants fresh.
- `.planning/research/PITFALLS.md` §Pitfall 6 — ICO alpha channel: load via Pillow `.convert("RGBA")`, not pygame's ICO loader directly.
- `.planning/research/PITFALLS.md` §Pitfall 10 — AutoRedraw → clear-then-draw: pre-bake background_surface, blit it first every frame.
- `.planning/research/PITFALLS.md` §Pitfall 2 — dt-scaling: apply from day one in the game loop.

### VB6 Source (for reference proportions/colors only)
- `D:\dev\repo\best-game-ever\_old\frmSuperman.frm` — original VB6 form; read for zone proportions and color values
- `D:\dev\repo\best-game-ever\_old\Form1.frm` — secondary VB6 form

### Asset Manifest Derivation
- `.planning/REQUIREMENTS.md` §Player Movement (MOV-09, MOV-10) — Superman and Goblin sprite sets
- `.planning/REQUIREMENTS.md` §Audio (AUD-01–05) — required WAV and MIDI files
- `D:\dev\repo\best-game-ever\_old\Icons\` — source ICO files (copy relevant ones to raw_assets/)
- `D:\dev\repo\best-game-ever\_old\Sounds\` — source WAV/MIDI files (copy relevant ones to raw_assets/)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None — this is a greenfield project. No existing code to reuse.

### Established Patterns
- None yet — Phase 1 establishes all foundational patterns that later phases follow.

### Integration Points
- `settings.py` is the single source of truth for all constants. Every subsequent phase imports from it. Get this right in Phase 1.
- `assets.py` asset cache (keyed dict of surfaces/sounds) is consumed by every gameplay phase. The key naming convention established here must be consistent with what player.py and beam.py expect in later phases.

</code_context>

<specifics>
## Specific Ideas

- `raw_assets/` folder structure: `raw_assets/icons/` for ICOs, `raw_assets/sounds/` for WAVs and MIDIs — mirrors the original `_old/Icons/` and `_old/Sounds/` layout.
- `tools/TimGM6mb.sf2` — the soundfont lives in `tools/`, separate from game assets. The `tools/` directory holds dev-time utilities only.
- The `convert_assets.py` script should be idempotent: re-running it when `assets/` already exists should be safe (overwrite or skip unchanged files).

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within Phase 1 scope.

</deferred>

---

*Phase: 1-Foundation*
*Context gathered: 2026-05-16*
