from datetime import datetime
from core.positions.root_position_factory import create_geo_position
from events.zodiacal.astro_event import (
    DeclinationExtreme,
    LatitudeExtreme,
    NakshatraChange,
    PhaseExtreme,
    SpeedExtreme,
    TermChange,
)
from out.file import to_text_file
from tools.timeline.timeline_factory import create_timeline
from tools.timeline.timeline_printer import TimelinePrinter
from out.tv import generate_astro_events_script
from tools.timeline.timeline_config import (
    DEFAULT_ASTRO_EVENTS,
    TimelineConfig,
)
from util.common import measure
from core.zodiac.positions.mapped_geo_position import MappedGeoPosition as mgp


def timeline():
    start = datetime(2023, 12, 24)
    end = datetime(2024, 1, 10)

    timeline_config = TimelineConfig.default_no_moon(start, end)
    timeline = create_timeline(timeline_config)
    timeline_printer = TimelinePrinter(timeline)

    timeline_printer.print_to_file("timeline dec 24 - jan 10.txt")


def timeline_tv_script():
    start = datetime(2023, 11, 28)
    end = datetime(2023, 12, 1)

    zodiacal_events = [
        e for e in DEFAULT_ASTRO_EVENTS if e not in [TermChange, NakshatraChange]
    ]

    timeline_config = TimelineConfig.default_no_moon(start, end, zodiacal_events)
    timeline = create_timeline(timeline_config)

    script = generate_astro_events_script(
        timeline.events, "./src/app/resources/tv_template.txt"
    )
    to_text_file("PT nov 27 - dec 5.txt", script)


def mars():
    mars = create_geo_position(
        "mars",
        datetime.now(),
    )

    mars_mapped = mgp(mars)

    print(mars_mapped)


def timeline_moon():
    start = datetime(2023, 12, 1)
    end = datetime(2023, 12, 31)

    tcfg = TimelineConfig.default(
        start,
        end,
        60,
        ["mercury"],
        [DeclinationExtreme, LatitudeExtreme, SpeedExtreme],
        [],
    )
    timeline = create_timeline(tcfg)

    timeline_printer = TimelinePrinter(timeline)

    timeline_printer.print_to_console()


def timeline_sun():
    start = datetime(2023, 11, 18)
    end = datetime(2023, 11, 21)

    tcfg = TimelineConfig.default(
        start,
        end,
        ["sun"],
    )
    timeline = create_timeline(tcfg)

    timeline_printer = TimelinePrinter(timeline)

    timeline_printer.print_to_console()


if __name__ == "__main__":
    measure(timeline)
