from core.positions.position_factory import create_positions
from events.extremes.extreme_event_factory import create_extreme_events
from events.zodiacal.positional_event_factory import create_positional_events
from tools.timeline.timeline_config_parser import parse_json_to_timeline_configs
from tools.timeline.timeline_factory import create_timelines
from tools.timeline.timeline_printer import TimelinePrinter


single_cfg = """
{
  "configurations": [
    {
      "coordinateSystem": "helio",
      "startDate": "2024-01-01",
      "endDate": "2024-01-31",
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

multi_cfg = """
{
  "configurations": [
    {
      "coordinateSystem": "geo",
      "startDate": "2024-01-01",
      "endDate": "2024-01-10",
      "intervalMinutes": 1,
      "points": ["sun", "moon", "mercury", "north node"],
      "nodeCalc": "mean",
      "events": [
        "TropicalSignChange",
        "SiderealSignChange",
        "TermChange",
        "NakshatraChange",
        "DecanChange",
        "DirectionChange"
      ]
    },
    {
      "coordinateSystem": "helio",
      "startDate": "2024-01-01",
      "endDate": "2024-01-10",
      "intervalMinutes": 1,
      "points": ["mercury"],
      "nodeCalc": "mean",
      "events": [
        "TropicalSignChange",
        "SiderealSignChange"
      ]
    }
  ]
}
"""


def timeline(json_data: str):
    cfgs = parse_json_to_timeline_configs(json_data)

    for cfg in cfgs:
        cfg.validate()

    timelines = create_timelines(
        cfgs, create_positions, create_positional_events, create_extreme_events
    )

    for tl in timelines:
        printer = TimelinePrinter(tl)
        printer.print_to_console()


if __name__ == "__main__":
    timeline(multi_cfg)
