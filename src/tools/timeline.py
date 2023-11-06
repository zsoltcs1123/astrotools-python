from collections import defaultdict
from datetime import datetime as dt
from typing import List, Type
from core.angle_factory import AngleFactory
from core.enums import CoordinateSystem
from events.astro_event import AstroEvent, get_astro_events
from objects.points import get_default_angle_targets
from tools.timeline_config import TimelineConfig
from util.console_logger import ConsoleLogger
from zodiac.mapped_position import MappedPosition as mp


class Timeline:
    events: List[Type[AstroEvent]]
    grouped_events: defaultdict[dt, List[Type[AstroEvent]]]

    def __init__(self, config: TimelineConfig):
        self.logger = ConsoleLogger(Timeline.__name__)
        self.config = config
        self.events = sorted(self._generate(), key=lambda x: x.time)
        self.grouped_events = self._group_events_by_date()

    def _generate(self):
        if self.config.coordinate_system == CoordinateSystem.GEO:
            return self._generate_geo()
        else:
            return self._generate_helio()
        
    def _generate_helio(self):
        pass

    def _generate_geo(self):
        events = self._calculate_zodiacal_events() + self._find_all_aspects()
        return [event for sublist in events for event in sublist]

    def _calculate_zodiacal_events(self):
        return [self._calculate_event(point) for point in self.config.points]

    def _calculate_event(self, point):
        self.logger.info(f"Calculating zodiacal events for {point}")
        pos = self.config.position_factory.create_positions(
            point, self.config.start, self.config.end, self.config.interval_minutes
        )
        mapped = mp.from_planetary_positions(pos)
        return get_astro_events(mapped)

    def _find_all_aspects(self):
        if self.config.aspect_finder is None:
            return []

        angle_factory = AngleFactory(self.config.position_factory)
        return [self._find_aspects(point, angle_factory) for point in self.config.points]

    def _find_aspects(self, point, angle_factory):
        self.logger.info(f"Calculating aspects for {point}")
        targets = get_default_angle_targets(point)
        angles = angle_factory.get_multiple_angles_in_range(
            point,
            targets,
            self.config.start,
            self.config.end,
            self.config.interval_minutes,
        )
        return self.config.aspect_finder.find_exact_aspects(angles)


    def _group_events_by_date(self):
        grouped_events = defaultdict(list)
        for event in self.events:
            grouped_events[event.time.date()].append(event)
        return grouped_events
