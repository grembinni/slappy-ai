import pathlib
import pytest


@pytest.fixture
def assets_dir():
    return pathlib.Path(__file__).parent.parent / "assets"


@pytest.fixture
def raw_assets_dir():
    return pathlib.Path(__file__).parent.parent / "raw_assets"


@pytest.fixture
def sprites_dir(assets_dir):
    return assets_dir / "sprites"


@pytest.fixture
def sounds_dir(assets_dir):
    return assets_dir / "sounds"
