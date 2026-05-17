# Phase 5: Audio - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 5-Audio
**Areas discussed:** SoundManager design, Music backend, Mute behavior, AUD-05 scope

---

## SoundManager Design

### Q1: Where should sound triggers live for Player-originated events?

| Option | Description | Selected |
|--------|-------------|----------|
| game.py only | game.py detects all events (fire, collision, landing) and calls snd methods. Player stays pure. | ✓ |
| Pass SoundManager to Player | Player.fire() calls snd.play_laser() internally. Couples audio to player model. | |
| Callback on Player | Player stores callables set by game.py. Indirect and adds complexity. | |

**User's choice:** game.py only (recommended)
**Notes:** game.py already owns collision detection and the KEYDOWN block — adding sound calls there is zero-friction.

### Q2: What should SoundManager own?

| Option | Description | Selected |
|--------|-------------|----------|
| SFX + music + mute | SoundManager is the single audio authority — all pygame.mixer calls go through it. | ✓ |
| SFX only, music in game.py | Splits audio logic; game.py handles pygame.mixer.music directly. | |
| Just a thin dict wrapper | SoundManager is essentially AssetCache.sounds + muted flag; no named methods. | |

**User's choice:** SFX + music + mute (recommended)

### Q3: Where is SoundManager instantiated?

| Option | Description | Selected |
|--------|-------------|----------|
| Built inside Game.__init__ | self.snd = SoundManager(assets.sounds). Same pattern as self._hud_font. | ✓ |
| Passed into Game.__init__ | main.py builds SoundManager and passes it alongside assets. | |

**User's choice:** Built inside Game.__init__ (recommended)

---

## Music Backend

### Q1: How should background/intro music be played?

| Option | Description | Selected |
|--------|-------------|----------|
| pygame.mixer.music | Streaming, seamless looping, no channel consumed. Standard choice for long tracks. | You decide |
| pygame.mixer.Sound(loops=-1) | Reuses AssetCache Sound objects. In-memory, consumes a channel, possible loop gap. | |

**User's choice:** You decide (deferred to Claude)
**Notes:** Claude selected pygame.mixer.music — purpose-built for background music, seamless looping via play(-1), frees all mixer channels for SFX.

### Q2: Named vs generic music API?

| Option | Description | Selected |
|--------|-------------|----------|
| Named: play_playing_music() / play_splash_music() | Explicit per-state methods. Intent is clear, no string keys to typo. | ✓ |
| Generic: play_music('passport') | Flexible but shifts string key burden to callers. | |

**User's choice:** Named methods (recommended)

---

## Mute Behavior

### Q1: What happens to mid-play SFX when M is pressed?

| Option | Description | Selected |
|--------|-------------|----------|
| Pause them mid-play | pygame.mixer.pause() freezes active channels. Unmute resumes them. | ✓ |
| Let them finish, block new ones | Active SFX play through; mute flag prevents new triggers. Inconsistent behavior. | |

**User's choice:** Pause mid-play (recommended)

### Q2: What should music do on unmute?

| Option | Description | Selected |
|--------|-------------|----------|
| Resume from where it paused | pygame.mixer.music.unpause(). Music feels continuous. | ✓ |
| Restart track from beginning | pygame.mixer.music.play(-1). Disorienting if mid-loop. | |

**User's choice:** Resume from paused position (recommended)

---

## AUD-05 Scope

### Q1: What should Phase 5 do with canyon.wav?

| Option | Description | Selected |
|--------|-------------|----------|
| Wire the trigger now, SPLASH can't fire yet | play_splash_music() implemented; game.py maps SPLASH→canyon. Harmless until Phase 6 uses SPLASH state. | ✓ |
| Defer canyon.wav to Phase 6 | Phase 5 only wires passport.wav. Phase 6 adds play_splash_music() and the trigger. | |

**User's choice:** Wire the trigger now (recommended)
**Notes:** Phase 6 needs zero audio code for AUD-05 — it just needs to set initial game state to SPLASH.

---

## Claude's Discretion

- **Music backend selection:** User chose "You decide." Claude selected `pygame.mixer.music` based on: streaming for large converted-MIDI tracks, seamless looping, no channel consumption, and standard pygame best practice.
- **SFX key mapping:** `assets.sounds` keys are lowercase WAV stems — `laser`, `deathcry`, `explode`. Claude maps these directly without adding constants.
- **intro.wav:** File exists in assets/sounds/ but has no AUD requirement. Claude marked it unused in Phase 5 and noted it as deferred.
- **stop_music() on GAME_OVER:** Claude added this integration point; not explicitly discussed but implied by a clean state-driven audio design.

## Deferred Ideas

- Stereo panning by character position (v2 backlog in REQUIREMENTS.md)
- GAME_OVER fanfare — Phase 6 scope
- intro.wav — exists but no requirement; defer post-v1
- Per-channel volume control / sliders — out of scope for v1
