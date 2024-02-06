from typing import List

from astrotoolz.tools.timeline.timeline import Timeline


def aggregate_timelines(timelines: List[Timeline]) -> Timeline:
    events = []
    for timeline in timelines:
        events += timeline.events
    return Timeline(events)
