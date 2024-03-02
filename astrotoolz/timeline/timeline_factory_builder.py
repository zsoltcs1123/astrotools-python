from astrotoolz.core.angles.angle_factory import AngleFactory
from astrotoolz.core.angles.angle_target_calculator import AngleTargetCalculator
from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.events.astro_event import (
    ExtremeEvent,
    PositionalEvent,
    TropicalProgression,
)
from astrotoolz.core.events.factory.aspect_factory import AspectFactory
from astrotoolz.core.events.factory.extreme_event_factory import ExtremeEventFactory
from astrotoolz.core.events.factory.positional_event_factory import (
    PositionalEventFactory,
)
from astrotoolz.core.positions.factory.geo_factory import GeoFactory
from astrotoolz.core.positions.factory.helio_factory import HelioFactory
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper
from astrotoolz.timeline.timeline_config import TimelineConfig
from astrotoolz.timeline.timeline_factory import TimelineFactory


def build_timeline_factory(config: TimelineConfig) -> TimelineFactory:

    config.validate()

    position_factory = (
        GeoFactory(config.node_calc)
        if config.coordinate_system == CoordinateSystem.GEO
        else HelioFactory()
    )

    position_mapper = PositionMapper()

    angle_target_calculator = AngleTargetCalculator(config.coordinate_system)

    angle_factory = AngleFactory(position_factory, position_mapper)

    positional_event_types = [
        e
        for e in config.events
        if issubclass(e, PositionalEvent) or e is TropicalProgression
    ]

    positional_event_factory = (
        PositionalEventFactory(positional_event_types, config.coordinate_system)
        if positional_event_types
        else None
    )

    extreme_event_types = [e for e in config.events if issubclass(e, ExtremeEvent)]

    extreme_event_factory = (
        ExtremeEventFactory(extreme_event_types, config.coordinate_system)
        if extreme_event_types
        else None
    )

    aspect_factory = AspectFactory(config.coordinate_system)

    return TimelineFactory(
        position_factory,
        position_mapper,
        angle_target_calculator,
        angle_factory,
        positional_event_factory,
        extreme_event_factory,
        aspect_factory,
    )
