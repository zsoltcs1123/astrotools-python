from collections import defaultdict
from datetime import datetime as dt
from typing import List, Type
from events.astro_event import AstroEvent


class Timeline:
    events: List[Type[AstroEvent]]
    grouped_events: defaultdict[dt, List[Type[AstroEvent]]]

    def __init__(self, events: List[Type[AstroEvent]]):
        self.events = sorted(events, key=lambda x: x.dt)
        self.grouped_events = self._group_events_by_date()

    def _group_events_by_date(self):
        grouped_events = defaultdict(list)
        for event in self.events:
            grouped_events[event.dt.date()].append(event)
        return grouped_events
