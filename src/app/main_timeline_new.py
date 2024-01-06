from core.positions.position_factory import create_geo_positions
from events.extremes.extreme_event_factory import create_extreme_events
from events.zodiacal.positional_event_factory import create_positional_events
from tools.timeline.timeline_config_parser import parse_json_to_timeline_configs
from tools.timeline.timeline_factory import create_timeline
from tools.timeline.timeline_printer import TimelinePrinter
from util.common import measure


def timeline():
    json_data = """
{
  "configurations": [
    {
      "coordinateSystem": "geo",
      "startDate": "2024-01-01",
      "endDate": "2024-01-06",
      "intervalMinutes": 1,
      "points": ["sun", "moon", "mercury", "north node"],
      "nodeCalc": "mean",
      "events": [
        "TropicalSignChange",
        "VedicSignChange",
        "TermChange",
        "NakshatraChange",
        "DecanChange",
        "DirectionChange"
      ]
    }
  ]
}
"""

    cfg = parse_json_to_timeline_configs(json_data)[0]
    cfg.validate()

    timeline = create_timeline(
        cfg, create_geo_positions, create_positional_events, create_extreme_events
    )

    printer = TimelinePrinter(timeline)
    printer.print_to_console()


if __name__ == "__main__":
    measure(timeline)
