from datetime import datetime

import pytest

from astrotoolz.core.enums import CoordinateSystem, NodeCalc
from astrotoolz.core.events.astro_event import DirectionChange
from astrotoolz.timeline.aspect_config import AspectsConfig
from astrotoolz.timeline.timeline_config import TimelineConfig


class TestTimelineConfig:
    def test_validate_start_date_after_end_date(self):
        with pytest.raises(ValueError):
            config = TimelineConfig(
                CoordinateSystem.GEO,
                datetime(2022, 1, 1),
                datetime(2021, 1, 1),
                1,
                ["sun"],
            )
            config.validate()

    def test_validate_interval_less_than_1(self):
        with pytest.raises(ValueError):
            config = TimelineConfig(
                CoordinateSystem.GEO,
                datetime(2021, 1, 1),
                datetime(2022, 1, 1),
                0,
                ["sun"],
            )
            config.validate()

    def test_validate_invalid_source_points(self):
        with pytest.raises(ValueError):
            config = TimelineConfig(
                CoordinateSystem.GEO,
                datetime(2021, 1, 1),
                datetime(2022, 1, 1),
                1,
                ["invalid_point"],
            )
            config.validate()

    def test_validate_no_valid_points(self):
        with pytest.raises(ValueError):
            config = TimelineConfig(
                CoordinateSystem.GEO,
                datetime(2021, 1, 1),
                datetime(2022, 1, 1),
                1,
                [],
            )
            config.validate()

    def test_validate_helio_point_is_in_SUN_MOON_NN_SN(self):
        with pytest.raises(ValueError):
            config = TimelineConfig(
                CoordinateSystem.HELIO,
                datetime(2021, 1, 1),
                datetime(2022, 1, 1),
                1,
                ["sun"],
                NodeCalc.MEAN,
                None,
                None,
            )
            config.validate_helio()

    def test_validate_helio_DirectionChange_is_in_events(self):
        with pytest.raises(ValueError):
            config = TimelineConfig(
                CoordinateSystem.HELIO,
                datetime(2021, 1, 1),
                datetime(2022, 1, 1),
                1,
                ["earth"],
                NodeCalc.MEAN,
                [DirectionChange],
            )
            config.validate_helio()

    def test_validate_geo_MOON_is_in_points_but_node_calc_is_None(self):
        with pytest.raises(ValueError):
            config = TimelineConfig(
                CoordinateSystem.GEO,
                datetime(2021, 1, 1),
                datetime(2022, 1, 1),
                1,
                ["moon"],
                None,
            )
            config.validate_geo()

    def test_validate_helio_invalid_angle_targets(self):
        with pytest.raises(ValueError):
            config = TimelineConfig(
                CoordinateSystem.HELIO,
                datetime(2021, 1, 1),
                datetime(2022, 1, 1),
                1,
                ["mercury"],
                aspects=[AspectsConfig(30, True, 0.1, ["sun"])],
            )
            config.validate_helio()
