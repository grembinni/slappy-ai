# Validation Strategy — Phase 1: Foundation

**Phase:** 1
**Slug:** foundation
**Date:** 2026-05-16

---

## Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3 |
| Config file | `pytest.ini` (or `pyproject.toml [tool.pytest.ini_options]`) |
| Quick run | `python -m pytest tests/ -x -q` |
| Full suite | `python -m pytest tests/ -v` |

---

## Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command |
|--------|----------|-----------|-------------------|
| ENG-01 | `clock.tick(60)` returns ms; `dt = result / 1000.0` is a float in valid range | unit | `pytest tests/test_settings.py::test_fps_constant -x` |
| ENG-02 | `GameState` enum has SPLASH, PLAYING, PAUSED, GAME_OVER members | unit | `pytest tests/test_settings.py::test_gamestate_enum -x` |
| ENG-03 | `AssetCache` loads without error when `assets/` is populated | integration | `pytest tests/test_assets.py::test_asset_cache_loads -x` |
| ENG-04 | All six constants importable from `settings.py` with correct values | unit | `pytest tests/test_settings.py::test_constants -x` |
| ENG-05 | `convert_assets.py --dry-run` lists expected files without writing | unit | `pytest tests/test_convert.py::test_dry_run -x` |

**Note on ENG-03:** `AssetCache` test requires `assets/` to already exist (convert_assets.py must have run). Use `pytest.mark.skipif` if `assets/sprites/` does not exist.

---

## Test Files Required

| File | Covers |
|------|--------|
| `tests/test_settings.py` | ENG-01, ENG-02, ENG-04 |
| `tests/test_assets.py` | ENG-03 (with skipif guard) |
| `tests/test_convert.py` | ENG-05 (dry-run mode) |
| `tests/conftest.py` | Shared fixtures (assets path, temp dir) |
| `pytest.ini` | Test discovery config |

---

## Sampling Rate

| Trigger | Command |
|---------|---------|
| Per task commit | `python -m pytest tests/test_settings.py -x -q` |
| Per wave merge | `python -m pytest tests/ -v` |
| Phase gate (before /gsd:verify-work) | Full suite green |

---

## Dimension 8: Validation Coverage

- [x] Test framework specified (pytest 9.0.3)
- [x] All 5 requirements have mapped test cases
- [x] Integration test guard for ENG-03 (skipif when assets/ absent)
- [x] Sampling rate defined (per-task, per-wave, phase gate)
- [ ] Tests implemented — Wave 1 of PLAN.md creates these files
