from datetime import datetime
from core.base_position import BasePosition
from core.position_factory import PositionFactory
from events.astro_event import NakshatraChange, TropicalSignChange
from objects.points import MEAN_NODE
from out.file import to_text_file
from tools.timeline.timeline_printer import TimelinePrinter
from out.tv import generate_pivot_times
from tools.timeline.timeline import Timeline
from tools.timeline.timeline_config import (
    DEFAULT_ASPECTS,
    DEFAULT_ZODIACAL_EVENTS,
    TimelineConfig,
)
from util.common import measure
from zodiac.mapped_position import MappedPosition


def timeline():
    start = datetime(2023, 11, 22)
    end = datetime(2023, 11, 23)

    timeline_config = TimelineConfig.default_no_moon(start, end)
    timeline = Timeline(timeline_config)
    timeline_printer = TimelinePrinter(timeline)

    timeline_printer.print_to_console()


def timeline_tv_script():
    start = datetime(2023, 11, 20)
    end = datetime(2023, 11, 27)

    zodiacal_events = [
        event for event in DEFAULT_ZODIACAL_EVENTS if event != TropicalSignChange
    ]
    timeline_config = TimelineConfig.default_no_moon(
        start, end, DEFAULT_ASPECTS, zodiacal_events
    )
    timeline = Timeline(timeline_config)

    # Filter events where event.time is the same
    unique_events = []
    seen_times = set()
    for event in timeline.events:
        if event.dt not in seen_times:
            unique_events.append(event)
            seen_times.add(event.dt)

    tv_timestamps = ", ".join([event.tv_timestamp() for event in unique_events])
    script = generate_pivot_times("Pivot Times nov 20 - nov 27", tv_timestamps)
    to_text_file("PT nov 20-nov 27.txt", script)


def mars():
    factory = PositionFactory(MEAN_NODE)
    mars = factory.create_position(
        "mars",
        datetime.now(),
    )

    mars_mapped = MappedPosition(mars)

    print(mars_mapped)


def timeline_sun():
    start = datetime(2023, 8, 1)
    end = datetime(2023, 11, 21)

    tcfg = TimelineConfig.default(start, end, ["sun"], zodiacal_events=[])
    timeline = Timeline(tcfg)

    timeline_printer = TimelinePrinter(timeline)

    timeline_printer.print_to_console()


if __name__ == "__main__":
    measure(timeline_sun)
