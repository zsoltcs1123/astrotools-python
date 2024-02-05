from events.astro_event import (
    DecanChange,
    DeclinationExtreme,
    SpeedExtreme,
    TropicalSignChange,
)

from astrotoolz.core.enums import CoordinateSystem, NodeCalc
from astrotoolz.tools.timeline.timeline_config_parser import (
    parse_json_to_timeline_configs,
)


def test_parse_json_to_timeline_configs():
    json_data = """
    {
      "configurations": [
        {
          "coordinateSystem": "geo",
          "startDate": "2024-01-01",
          "endDate": "2024-12-31",
          "intervalMinutes": 1,
          "points": ["sun", "moon", "mercury", "north node"],
          "nodeCalc": "mean",
          "events": [
            "TropicalSignChange",
            "DecanChange",
            "DeclinationExtreme",
            "SpeedExtreme"
          ],
          "aspects": {
            "angle": 30,
            "family": true
          }
        }
      ]
    }
    """
    timeline_configs = parse_json_to_timeline_configs(json_data)
    assert isinstance(timeline_configs, list)
    for config in timeline_configs:
        assert config.coordinate_system == CoordinateSystem.GEO
        assert config.start_date.year == 2024
        assert config.end_date.year == 2024
        assert config.interval_minutes == 1
        assert config.points == ["sun", "moon", "mercury", "north node"]
        assert config.node_calc == NodeCalc.MEAN
        assert config.events == [
            TropicalSignChange,
            DecanChange,
            DeclinationExtreme,
            SpeedExtreme,
        ]
        assert config.aspects.angle == 30
        assert config.aspects.family == True
