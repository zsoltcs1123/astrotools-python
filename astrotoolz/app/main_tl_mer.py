from datetime import datetime

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.tools.timeline.timeline_config import AspectsConfig, TimelineConfig
from astrotoolz.tools.timeline.timeline_factory_builder import build_timeline_factory
from astrotoolz.tools.timeline.timeline_printer import TimelinePrinter
from astrotoolz.util.common import measure


def timeline():

    cfg = TimelineConfig(
        CoordinateSystem.GEO,
        datetime(2024, 1, 1),
        datetime(2025, 1, 1),
        60,
        ["mercury"],
        "mean",
        [],
        [AspectsConfig(360, True, 0.1, ["sun"])],
    )

    factory = build_timeline_factory(cfg)

    timeline = factory.create_timeline(cfg)

    printer = TimelinePrinter(timeline)
    printer.print_to_file("tl_mer_sun.txt")


if __name__ == "__main__":
    measure(lambda: timeline())
