from datetime import datetime
from out.timeline_printer import TimelinePrinter
from tools.timeline import Timeline
from tools.timeline_config import TimelineConfig


def timeline():
    start = datetime(2023, 11, 13)
    end = datetime(2023, 12, 2)

    timeline_config = TimelineConfig.default_no_moon(start, end)
    timeline = Timeline(timeline_config)
    timeline_printer = TimelinePrinter(timeline)

    timeline_printer.print_to_file("timeline_nov_13_dec_2_no_moon")


if __name__ == "__main__":
    timeline()
