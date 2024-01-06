from tools.timeline.timeline_config_parser import parse_json_to_timeline_configs
from tools.timeline.timeline_factory import create_timelines
from tools.timeline.timeline_printer import TimelinePrinter
from util.common import measure


single_cfg = """
{
  "configurations": [
    {
      "coordinateSystem": "geo",
      "startDate": "2024-01-01",
      "endDate": "2024-02-01",
      "intervalMinutes": 60,
      "points": ["mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"],
      "nodeCalc": "mean",
      "events": [
        "TropicalSignChange",
        "TermChange",
        "DecanChange",
        "DirectionChange"
      ],
      "aspects": [
          {
              "angle": 30,
              "family": true,
              "orb": 0.1
          }
      ]
    },
    {
      "coordinateSystem": "geo",
      "startDate": "2024-01-01",
      "endDate": "2024-01-31",
      "intervalMinutes": 1,
      "points": ["moon"],
      "nodeCalc": "mean",
      "aspects": [
          {
              "angle": 30,
              "family": true,
              "orb": 0.01,
              "targets": ["sun"]
          }
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

    timelines = create_timelines(cfgs)

    for tl in timelines:
        printer = TimelinePrinter(tl)
        printer.print_to_file("tropical_january.txt")


if __name__ == "__main__":
    measure(lambda: timeline(single_cfg))
