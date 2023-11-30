from typing import Dict, List, Type
from core.angle import Angle
from core.position_factory import PositionFactory
from events.aspect_finder import AspectFinder
from events.astro_event import AstroEvent
from events.zodiacal_event_factory import ZodiacalEventFactory
from objects.points import get_default_angle_targets
from tools.timeline.timeline import Timeline
from tools.timeline.timeline_config import TimelineConfig
from util.console_logger import ConsoleLogger
from zodiac.mapped_position import MappedPosition as mp


_logger = ConsoleLogger("TimelineFactory")


def create_timeline(config: TimelineConfig):
    position_factory = PositionFactory(config.node_calc)

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

    mps = _generate_positions(position_factory, config)
    zodiacal_events = _generate_zodiacal_events(zodiacal_event_factory, mps)
    angles = _generate_angles(position_factory, mps)
    aspects = aspect_finder.find_exact_aspects(angles)

    return Timeline(zodiacal_events + aspects)


def _generate_positions(
    position_factory: PositionFactory, config: TimelineConfig
) -> Dict[str, List[mp]]:
    mps = {}
    for point in config.points:
        bps = position_factory.create_positions(
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


def _generate_angles(
    position_factory: PositionFactory, mps: Dict[str, List[mp]]
) -> List[Angle]:
    angles = []
    for p, mp_list in mps.items():
        targets = get_default_angle_targets(p)

        for source_mp in mp_list:
            for t in targets:
                target_bp = position_factory.create_position(t, source_mp.dt)
                target_mp = mp(target_bp)
                angle = Angle(source_mp, target_mp)
                angles.append(angle)

    return angles
