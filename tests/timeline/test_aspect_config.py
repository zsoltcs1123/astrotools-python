import pytest

from astrotoolz.timeline.aspect_config import AspectsConfig


def test_validate_with_valid_targets():
    config = AspectsConfig(90, True, 1.5, ["moon", "mars"])
    assert config.validate() is None


def test_validate_with_invalid_target():
    config = AspectsConfig(90, True, 1.5, ["moon", "invalid_target"])
    with pytest.raises(ValueError):
        config.validate()


def test_validate_with_invalid_orb():
    config = AspectsConfig(90, True, -1.5, ["moon", "mars"])
    with pytest.raises(ValueError):
        config.validate()
