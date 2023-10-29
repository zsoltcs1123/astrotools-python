from datetime import datetime as dt
from typing import List, Type
from core.angle import get_all_angles_in_date_range
from core.enums import CoordinateSystem
from core.position import Position as pp
from events.aspect import get_all_aspects
from events.astro_event import AstroEvent, get_astro_events
from util.console_logger import ConsoleLogger
from zodiac.mapped_position import MappedPosition as mp
from itertools import groupby


class Timeline:
    events: List[Type[AstroEvent]]
    grouped_events: List[List[Type[AstroEvent]]]
    
    def __init__(self, start: dt, end: dt, interval_minutes: int, planets: List[str], coordinate_system=CoordinateSystem.GEO):
        self.logger = ConsoleLogger(Timeline.__name__)
        self.start = start
        self.end = end
        self.interval_minutes = interval_minutes
        self.planets = planets
        self.coordinate_system = coordinate_system
        
        self.events = self._generate()
        self.events = sorted(self.events, key=lambda x: x.time)
        
        self.grouped_events = []
        for k, g in groupby(self.events, key=lambda x: x.time.date()):
            self.grouped_events.append(list(g))
        

    def _generate_geo(self):
        events = []
        for i, planet in enumerate(self.planets):
            self.logger.info(f'Calculating {planet}')
            pos = pp.from_datetime_range(planet, self.start, self.end, self.interval_minutes)
            mapped = mp.from_planetary_positions(pos)
            events += get_astro_events(mapped)
            angles = get_all_angles_in_date_range(planet, self.start, self.end, 1)
            aspects = get_all_aspects(angles)
            events += aspects
        return events

    def _generate_helio(self):
        pass

    def _generate(self):
        if (self.coordinate_system == CoordinateSystem.GEO):
            return self._generate_geo()
        else:
            return self._generate_helio()
