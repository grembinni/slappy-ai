---
plan: 04-05
phase: 04-death-respawn-scoring
status: complete
---

# Plan 04-05: tests/test_death.py — Phase 4 test suite

## What was built

`tests/test_death.py` with 16 tests (planned 15; DTH-07 source inspection adds one for fuller coverage):

| Test | Requirement |
|------|-------------|
| test_start_crash_sets_crashing | DTH-01 |
| test_crashing_falls_dt_scaled | DTH-02 |
| test_spin_frame_advances_at_interval | DTH-03 |
| test_spin_frame_wraps | DTH-03 |
| test_crashing_transitions_to_dead_at_ground | DTH-04 |
| test_dead_sprite_key | DTH-04 |
| test_crashing_sprite_key | DTH-03 |
| test_respawn_returns_to_alive | DTH-05/06 |
| test_respawn_position_bounds | DTH-06 (20 iterations) |
| test_respawn_clears_beams | DTH-06 |
| test_mouse_click_crash_logic_present | DTH-07 (source inspection) |
| test_score_formula | SCR-01 |
| test_pose_accumulates_idle_airborne | SCR-02 |
| test_beam_hit_awards_hit_bonus | SCR-03 |
| test_hud_renders_and_osg_hidden | SCR-05 |
| test_win_condition_triggers_game_over | SCR-06 |

## Verification

- `py -3.11 -m pytest tests/test_death.py -v` — 16/16 passed
- `py -3.11 -m pytest tests/ -v` — 66/66 passed (50 prior + 16 new, no regressions)

## Requirements covered

DTH-01–07 (crash animation, death, respawn), SCR-01–06 (scoring, HUD, win condition)
