from typing import Dict, List, Type
from core.angles.angle_factory import generate_angles_list
from core.positions.root_position_factory import create_geo_positions
from events.aspects.aspect_finder import AspectFinder
from events.zodiacal.astro_event import AstroEvent
from events.zodiacal.zodiacal_event_factory import ZodiacalEventFactory
from events.extremes.extreme_event_factory import create_extreme_events
from core.objects.points import get_default_angle_targets
from tools.timeline.timeline import Timeline
from tools.timeline.timeline_config import (
    EXTREME_EVENTS,
    ZODIACAL_EVENTS,
    TimelineConfig,
)
from util.console_logger import ConsoleLogger
from core.zodiac.positions.mapped_geo_position import (
    MappedGeoPosition as MappedGeoPosition,
)


_logger = ConsoleLogger("TimelineFactory")


def create_timeline(config: TimelineConfig):
    mps = _generate_positions(config)

    zodiacal_events = []

    if set(config.astro_events) & set(ZODIACAL_EVENTS):
        zodiacal_event_factory = ZodiacalEventFactory(config.astro_events)
        zodiacal_events = _generate_zodiacal_events(zodiacal_event_factory, mps)

    aspects = []
    if config.aspects:
        aspect_finder = AspectFinder(config.orb_map, config.aspects)
        _logger.info(f"Generating angles")
        angles = generate_angles_list(mps, get_default_angle_targets)
        _logger.info(f"Calculating aspects...")
        aspects = aspect_finder.find_exact_aspects(angles)

    extreme_events = []
    if set(config.astro_events) & set(EXTREME_EVENTS):
        extreme_events = _generate_extreme_events(mps, config)

    return Timeline(zodiacal_events + aspects + extreme_events)


def _generate_positions(config: TimelineConfig) -> Dict[str, List[MappedGeoPosition]]:
    mps = {}
    for point in config.points:
        _logger.info(f"Generating positions for {point}")
        bps = create_geo_positions(
            point, config.start, config.end, config.interval_minutes
        )
        mp_list = [MappedGeoPosition(bp) for bp in bps]
        mps[point] = mp_list

    return mps


def _generate_zodiacal_events(
    zodiacal_event_factory: ZodiacalEventFactory,
    mps: Dict[str, List[MappedGeoPosition]],
) -> List[Type[AstroEvent]]:
    events = []
    for p, mp_list in mps.items():
        _logger.info(f"Generating zodiacal events for {p}")
        events += zodiacal_event_factory.create_events(mp_list)
    return events


def _generate_extreme_events(
    mps: Dict[str, List[MappedGeoPosition]], config: TimelineConfig
) -> List[AstroEvent]:
    events = []
    for p, mp_list in mps.items():
        _logger.info(f"Generating extreme events for {p}")
        events += create_extreme_events(mp_list, config.astro_events)
    return events
