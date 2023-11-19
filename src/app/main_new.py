from datetime import datetime
from events.astro_event import SignChange
from out.file import to_text_file
from out.timeline_printer import TimelinePrinter
from out.tv import generate_pivot_times
from tools.timeline import Timeline
from tools.timeline_config import DEFAULT_ASPECTS, DEFAULT_ZODIACAL_EVENTS, TimelineConfig


def timeline():
    start = datetime(2023, 11, 13)
    end = datetime(2023, 12, 2)

    timeline_config = TimelineConfig.default_no_moon(start, end)
    timeline = Timeline(timeline_config)
    timeline_printer = TimelinePrinter(timeline)

    timeline_printer.print_to_file("timeline_nov_13_dec_2_no_moon")
    

def timeline_tv_script():
    start = datetime(2023, 11, 13)
    end = datetime(2023, 11, 20)

    zodiacal_events = [event for event in DEFAULT_ZODIACAL_EVENTS if event != SignChange] 
    timeline_config = TimelineConfig.default_no_moon(start, end, DEFAULT_ASPECTS, zodiacal_events)
    timeline = Timeline(timeline_config)
    
    # Filter events where event.time is the same
    unique_events = []
    seen_times = set()
    for event in timeline.events:
        if event.time not in seen_times:
            unique_events.append(event)
            seen_times.add(event.time)
            
    tv_timestamps = ", ".join([event.tv_timestamp() for event in unique_events])
    script = generate_pivot_times('Pivot Times nov 13 - nov 20', tv_timestamps)
    to_text_file('PT nov 13-nov 20.txt', script)


if __name__ == "__main__":
    timeline_tv_script()
