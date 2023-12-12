from typing import Dict, List, Type
from core.angle_factory import generate_angles_list
from core.position_factory import create_geo_positions
from events.aspect_finder import AspectFinder
from events.astro_event import AstroEvent
from events.zodiacal_event_factory import ZodiacalEventFactory
from objects.points import get_default_angle_targets
from tools.timeline.timeline import Timeline
from tools.timeline.timeline_config import TimelineConfig
from util.console_logger import ConsoleLogger
from zodiac.mapped_geo_position import MappedGeoPosition as mp


_logger = ConsoleLogger("TimelineFactory")


def create_timeline(config: TimelineConfig):
    zodiacal_event_factory = (
        ZodiacalEventFactory(config.zodiacal_events)
        if len(config.zodiacal_events) > 0
        else None
    )

    aspect_finder = (
        AspectFinder(config.orb_map, config.aspects)
        if len(config.aspects) > 0
        else None
    )

    mps = _generate_positions(config)
    zodiacal_events = _generate_zodiacal_events(zodiacal_event_factory, mps)
    _logger.info(f"Generating angles")
    angles = generate_angles_list(mps, get_default_angle_targets)

    _logger.info(f"Calculating aspects...")
    aspects = aspect_finder.find_exact_aspects(angles)

    return Timeline(zodiacal_events + aspects)


def _generate_positions(config: TimelineConfig) -> Dict[str, List[mp]]:
    mps = {}
    for point in config.points:
        _logger.info(f"Generating positions for {point}")
        bps = create_geo_positions(
            point, config.start, config.end, config.interval_minutes
        )
        mp_list = [mp(bp) for bp in bps]
        mps[point] = mp_list

    return mps


def _generate_zodiacal_events(
    zodiacal_event_factory: ZodiacalEventFactory,
    mps: Dict[str, List[mp]],
) -> List[Type[AstroEvent]]:
    events = []
    for p, mp_list in mps.items():
        _logger.info(f"Generating zodiacal events for {p}")
        events += zodiacal_event_factory.create_events(mp_list)
    return events
