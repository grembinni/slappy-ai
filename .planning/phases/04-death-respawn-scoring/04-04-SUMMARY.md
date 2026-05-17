---
plan: 04-04
phase: 04-death-respawn-scoring
status: complete
---

# Plan 04-04: game.py — Phase 4 full wiring

## What was built

9 changes to `game.py` wiring all Phase 4 features into the game loop:

1. `from hud import draw_hud` — new import
2. `WIN_SCORE` and `DIR_IDLE` added to settings import
3. `self.osg_score = 0` and `self._hud_font = pygame.font.Font(None, 28)` in `__init__`
4. K_UP KEYDOWN: Superman respawn when `state == DEAD`
5. K_w KEYDOWN: Goblin respawn when `state == DEAD` (state-gated, no conflict with move-up)
6. `MOUSEBUTTONDOWN`: clicks on living player → `start_crash()` + `osg_score += 1`
7. Collision: upgraded from `player.state = CharState.CRASHING` to `player.start_crash()` + `self.players[1-i].hit_bonus += 10`
8. Pose accumulation: `raw_pose += 1` for ALIVE + DIR_IDLE + not on ground (each frame)
9. Win condition: `player.score >= WIN_SCORE` or `osg_score >= WIN_SCORE` → `GameState.GAME_OVER`
10. `draw_hud(self.screen, self.players, self.osg_score, self._hud_font)` before `pygame.display.flip()`

## Verification

- `game.py phase4 OK` — all assertions passed
- `py -3.11 -m pytest tests/ -v` — 50/50 passed (no regressions)

## Requirements covered

DTH-05 (respawn keys), DTH-06 (state-gated), DTH-07 (mouse crash), SCR-02 (pose score), SCR-03 (hit_bonus), SCR-04 (osg_score), SCR-05 (draw_hud), SCR-06 (win condition)
