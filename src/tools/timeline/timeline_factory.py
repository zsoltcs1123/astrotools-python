from typing import Callable, Dict, List, Type
from core.enums import CoordinateSystem
from core.positions.base_position import BasePosition as bp
from core.positions.position_factory_config import PositionFactoryConfig
from core.zodiac.positions.mapped_helio_position import MappedHelioPosition
from core.zodiac.positions.mapped_position import MappedPosition as mp
from events.astro_event import (
    AstroEvent,
    ExtremeEvent,
    PositionalEvent,
    TropicalProgression,
)
from core.objects.points import NN, SN, SUN
from tools.timeline.timeline import Timeline
from tools.timeline.timeline_config import (
    TimelineConfig,
)
from util.console_logger import ConsoleLogger
from core.zodiac.positions.mapped_geo_position import (
    MappedGeoPosition as MappedGeoPosition,
)


_logger = ConsoleLogger("TimelineFactory")


PositionFactory = Callable[[PositionFactoryConfig], List[bp]]
EventFactory = Callable[[List[mp], List[type]], List[AstroEvent]]


def create_timelines(
    configs: List[TimelineConfig],
    position_factory: PositionFactory,
    positional_event_factory: EventFactory,
    extreme_event_factory: EventFactory,
    aggregate: bool = True,
) -> List[Timeline]:
    timelines = [
        create_timeline(
            config,
            position_factory,
            positional_event_factory,
            extreme_event_factory,
        )
        for config in configs
    ]

    if aggregate:
        return [_aggregate_timelines(timelines)]
    else:
        return timelines


def create_timeline(
    config: TimelineConfig,
    position_factory: PositionFactory,
    positional_event_factory: EventFactory,
    extreme_event_factory: EventFactory,
) -> Timeline:
    mps = _generate_mapped_positions(config, position_factory)

    events = []

    positional_event_types = [
        e
        for e in config.events
        if issubclass(e, PositionalEvent) or e is TropicalProgression
    ]

    if positional_event_types:
        events += _generate_positional_events(
            config, mps, positional_event_types, positional_event_factory
        )

    extreme_event_types = [e for e in config.events if e == ExtremeEvent]

    if extreme_event_types:
        events += _generate_extreme_events(
            config, mps, extreme_event_types, extreme_event_factory
        )

    aspects = []

    # if config.aspects:
    #     aspect_finder = AspectFinder(config.orb_map, config.aspects)
    #     _logger.info(f"Generating angles")
    #     angles = generate_angles_list(mps, get_default_angle_targets)
    #     _logger.info(f"Calculating aspects...")
    #     aspects = aspect_finder.find_exact_aspects(angles)

    return Timeline(events + aspects)


def _generate_mapped_positions(
    tl_config: TimelineConfig,
    factory: PositionFactory,
) -> Dict[str, List[mp]]:
    mps = {}
    for point in tl_config.points:
        _logger.info(f"Generating {tl_config.coordinate_system} positions for {point}")
        factory_config = PositionFactoryConfig(
            tl_config.coordinate_system,
            point,
            tl_config.start_date,
            tl_config.end_date,
            tl_config.interval_minutes,
            tl_config.node_calc,
        )
        bps = factory(factory_config)
        mp_list = (
            [MappedGeoPosition(bp) for bp in bps]
            if tl_config.coordinate_system == CoordinateSystem.GEO
            else [MappedHelioPosition(bp) for bp in bps]
        )
        mps[point] = mp_list

    return mps


def _generate_positional_events(
    tl_config: TimelineConfig,
    mps: Dict[str, List[mp]],
    event_types: List[type],
    factory: EventFactory,
) -> List[Type[AstroEvent]]:
    events = []
    for p, mp_list in mps.items():
        _logger.info(
            f"Generating {tl_config.coordinate_system} positional events for {p}"
        )
        events += factory(mp_list, event_types)
    return events


def _generate_extreme_events(
    tl_config: TimelineConfig,
    mps: Dict[str, List[mp]],
    event_types: List[type],
    factory: EventFactory,
) -> List[AstroEvent]:
    events = []
    for p, mp_list in mps.items():
        if p == NN or p == SN or p == SUN:
            continue
        _logger.info(f"Generating {tl_config.coordinate_system} extreme events for {p}")
        events += factory(mp_list, event_types)
    return events


def _aggregate_timelines(timelines: List[Timeline]) -> Timeline:
    _logger.info("Aggregating timelines...")
    events = []
    for timeline in timelines:
        events += timeline.events
    return Timeline(events)
