import pathlib
import subprocess
import pytest

CONVERT_PATH = pathlib.Path(__file__).parent.parent / "convert_assets.py"
pytestmark = pytest.mark.skipif(
    not CONVERT_PATH.exists(),
    reason="convert_assets.py not yet created (Plan 04)",
)

_PROJECT_ROOT = str(pathlib.Path(__file__).parent.parent)


def test_dry_run():
    result = subprocess.run(
        ["python", "convert_assets.py", "--dry-run"],
        capture_output=True,
        text=True,
        cwd=_PROJECT_ROOT,
    )
    assert result.returncode == 0


def test_dry_run_output():
    result = subprocess.run(
        ["python", "convert_assets.py", "--dry-run"],
        capture_output=True,
        text=True,
        cwd=_PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert "gevil" in result.stdout.lower() or "GEvil" in result.stdout


def test_skip_midi_flag():
    result = subprocess.run(
        ["python", "convert_assets.py", "--skip-midi", "--dry-run"],
        capture_output=True,
        text=True,
        cwd=_PROJECT_ROOT,
    )
    assert result.returncode == 0
    combined = result.stdout + result.stderr
    assert "SKIPPING MIDI" in combined or "skip" in combined.lower()
