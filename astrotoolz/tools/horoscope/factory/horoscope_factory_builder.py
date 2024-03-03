from astrotoolz.core.angles.angle_factory import AngleFactory
from astrotoolz.core.angles.angle_target_calculator import AngleTargetCalculator
from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.events.factory.aspect_factory import AspectFactory
from astrotoolz.core.positions.factory.geo_factory import GeoFactory
from astrotoolz.core.positions.factory.helio_factory import HelioFactory
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper
from astrotoolz.tools.horoscope.factory.horoscope_factory import HoroscopeFactory
from astrotoolz.tools.horoscope.factory.horoscope_factory_config import (
    HoroscopeFactoryConfig,
)


def build_horoscope_factory(config: HoroscopeFactoryConfig) -> HoroscopeFactory:

    position_factory = (
        GeoFactory(config.node_calc)
        if config.coord_system == CoordinateSystem.GEO
        else HelioFactory()
    )

    position_mapper = PositionMapper()

    angle_target_calculator = (
        AngleTargetCalculator(config.coord_system) if config.include_aspects else None
    )

    angle_factory = (
        AngleFactory(position_factory, position_mapper)
        if config.include_aspects
        else None
    )

    aspect_factory = (
        AspectFactory(config.coord_system) if config.include_aspects else None
    )

    return HoroscopeFactory(
        config.coord_system,
        position_factory,
        position_mapper,
        angle_target_calculator,
        angle_factory,
        aspect_factory,
    )
