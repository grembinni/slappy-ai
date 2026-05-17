# Phase 6: Screens & Packaging - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 6-Screens-Packaging
**Areas discussed:** Escape key conflict, Splash credits content, Restart mechanic, GAME_OVER screen look, Win score input

---

## Escape Key Conflict

Requirements conflict: UI-05 said "P or Escape pauses", UI-07 said "Delete/Escape quits."

| Option | Description | Selected |
|--------|-------------|----------|
| Escape pauses (P or Esc) | During PLAYING: Escape and P both toggle pause. Delete remains the only hard quit. | ✓ |
| Escape quits (like Delete) | Escape and Delete both quit immediately. P alone toggles pause. | |

**User's choice:** Escape pauses (P or Esc)
**Notes:** Escape ONLY pauses during PLAYING state. No effect from SPLASH or GAME_OVER.

| Option | Description | Selected |
|--------|-------------|----------|
| PLAYING only | P/Escape only toggles pause when in PLAYING state. | ✓ |
| Any game state | P/Escape can pause from SPLASH or GAME_OVER too. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Pause audio | Music and SFX pause when PAUSED; resume on unpause. | ✓ |
| Audio keeps playing | Music continues looping during pause. | |

---

## Splash Credits Content

| Option | Description | Selected |
|--------|-------------|----------|
| Grep the VB6 source | Extract exact credits from D:\dev\repo\best-game-ever\_old\.frm files. | ✓ |
| Hardcode from memory | User tells Claude the text. | |

VB6 Form1.frm was read and 25 credits lines extracted. Timer1=1500ms (credits), Timer2=750ms (sprites).

| Option | Description | Selected |
|--------|-------------|----------|
| Random from sprite pool (VB6 faithful) | Pick randomly from all available character sprites every 750ms. | ✓ |
| Alternate Goblin/Superman only (REQUIREMENTS) | Two sprites, alternating at 750ms. | |

**Notes:** VB6 Timer2 picked randomly from a pool of 17 sprites — the requirement saying "two characters" was an approximation.

| Option | Description | Selected |
|--------|-------------|----------|
| Keep all 25 lines verbatim | Preserve all original credits exactly, including entries 22–23. | ✓ |
| You decide (Claude discretion) | Flag lines 22–23 as potentially sensitive with a comment. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Dark navy/dark red (VB6 original) | VB6 BackColor &H00400000 = RGB(0, 0, 64) dark navy blue. | ✓ |
| Black | Pure black. | |
| Same sky/background as game | Cyan sky. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Bottom of screen below credits | Fixed position at very bottom of screen. | ✓ |
| You decide | Claude places controls text. | |

---

## Restart Mechanic

| Option | Description | Selected |
|--------|-------------|----------|
| Full Game reinit (Recommended) | main.py creates new Game object. Cleanest approach. | ✓ |
| In-place state reset | game.py resets scores/players in place. Risk of missed resets. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Back to SPLASH | Full restart plays splash screen and intro music again. | ✓ |
| Straight to PLAYING | Skip splash on restart — faster for replaying. | |

| Option | Description | Selected |
|--------|-------------|----------|
| GAME_OVER only | F2/Enter only works on the GAME_OVER screen. | ✓ |
| Any state (matches UI-07) | F2 restarts from SPLASH, PLAYING, PAUSED, or GAME_OVER. | |

**Notes:** User narrowed from UI-07's "any state" to GAME_OVER only to avoid accidental mid-match restart.

---

## GAME_OVER Screen Look

| Option | Description | Selected |
|--------|-------------|----------|
| Black (Recommended) | Simple black background — draws attention to score text. | ✓ |
| Frozen game background | Blit last-rendered game frame, overlay text on top. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Scores + restart prompt (Recommended) | Final scores for all 3 players + "F2 or Enter to restart". Matches UI-06. | ✓ |
| Winner callout + scores + prompt | Also show which player won ("Superman Wins!"). | |

---

## Win Score Input (New — folded from v2 backlog)

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, fold into Phase 6 | Add win score selector to splash screen. | ✓ |
| Keep it v2 | Leave WIN_SCORE = 50 as constant. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Up/Down arrow keys to increment (Recommended) | Show "Win Score: 50", Up/Down to change, any other key starts. | ✓ |
| Number keys to type directly | Player types a number directly. | |

| Option | Description | Selected |
|--------|-------------|----------|
| 10 to 500 in steps of 10 (Recommended) | Min 10, max 500, step 10, default 50. | ✓ |
| You decide | Claude picks a sensible range. | |

---

## Claude's Discretion

- PAUSED overlay: semi-transparent dark rect or "PAUSED" text centered in large font — keep it simple
- Splash font sizes: title ~48–72, credits 28 (same as HUD), controls text ~20
- Splash sprite pool: random-pick from AssetCache.sprites.values() every 750ms
- GAME_OVER rendering stays in game.py draw() — no new module needed for a few text blits
- SoundManager.pause_game() / resume_game() — new methods that freeze audio without touching _muted flag

## Deferred Ideas

- GAME_OVER fanfare / jingle — v1 out of scope (Phase 5 deferred this)
- Winner callout ("Superman Wins!") on GAME_OVER — user chose scores-only
- Fullscreen toggle — v2 backlog
- Key rebinding — v2 backlog
- macOS/Linux packaging — out of scope
