from typing import List

import astrotoolz.core.ephemeris.swisseph_api as swe_api
import astrotoolz.core.zodiac.division as zodiac
from astrotoolz.core.enums import Zodiac
from astrotoolz.core.events.aspect import Aspect
from astrotoolz.core.events.astro_event import (
    AstroEvent,
    PositionalEvent,
    PositionChangeEvent,
)
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.units.degree import Degree
from astrotoolz.core.units.degree_converter import degree_from_decimal
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.core.zodiac.tropical_attributes import TropicalAttributes
from astrotoolz.core.zodiac.vedic_attributes import VedicAttributes
from astrotoolz.util.logger_base import LoggerBase


class PositionMapper(LoggerBase):

    def __init__(self, ayanamsa: str = "LAHIRI"):
        super().__init__()
        self._ayanamsa = ayanamsa

    def map_events(self, events: List[AstroEvent], zodiacs: List[Zodiac]):
        self._logger.info("Mapping astrological data...")
        for e in events:
            if isinstance(e, PositionalEvent):
                e.current = self.map_position(e.current, zodiacs)
            if isinstance(e, PositionChangeEvent):
                e.current = self.map_position(e.current, zodiacs)
                e.previous = self.map_position(e.previous, zodiacs)

    def map_aspects(self, aspects: List[Aspect], zodiacs: List[Zodiac]):
        self._logger.info("Mapping astrological data...")
        for e in aspects:
            e.angle.source = self.map_position(e.angle.source, zodiacs)
            e.angle.target = self.map_position(e.angle.target, zodiacs)

    def map_positions(
        self, positions: List[BasePosition], zodiacs: [List[Zodiac]]
    ) -> List[BasePosition]:
        self._logger.info("Mapping astrological data...")
        return [self.map_position(position, zodiacs) for position in positions]

    def map_position(
        self, position: BasePosition, zodiacs: List[Zodiac], cusps: List[float] = None
    ) -> MappedPosition:

        tropical_attributes = (
            self.map_tropical_attributes(position, cusps)
            if Zodiac.TROPICAL in zodiacs
            else None
        )

        vedic_attributes = (
            self.map_vedic_attributes(position, cusps)
            if Zodiac.SIDEREAL in zodiacs
            else None
        )

        return MappedPosition(position, tropical_attributes, vedic_attributes)

    def map_tropical_attributes(
        self, position: BasePosition, cusps: List[float] = None
    ) -> TropicalAttributes:

        lon = position.lon
        zodiacal_position = zodiac.degree_to_zodiacal(lon)
        sign = zodiac.map_sign(lon.decimal)
        sign_ruler = sign.classic_ruler
        decan = zodiac.map_decan(lon.decimal)
        term = zodiac.map_term(lon.decimal)
        house = self._house(lon, sign, cusps)

        return TropicalAttributes(
            lon, zodiacal_position, sign, sign_ruler, decan, term, house
        )

    def map_vedic_attributes(
        self, position: BasePosition, cusps: List[float] = None
    ) -> VedicAttributes:
        lon = self._calculate_sidereal_lon(position)
        zodiacal_position = zodiac.degree_to_zodiacal(lon)
        sign = zodiac.map_sign(lon.decimal)
        sign_ruler = sign.classic_ruler
        nakshatra = zodiac.map_nakshatra(lon.decimal)
        nakshatra_ruler = nakshatra.ruler
        house = self._house(lon, sign, cusps)

        return VedicAttributes(
            lon, zodiacal_position, sign, sign_ruler, nakshatra, nakshatra_ruler, house
        )

    # TODO Lahiri hardcoded
    def _calculate_sidereal_lon(self, position: BasePosition) -> Degree:
        ayanamsa = swe_api.get_ayanamsha(
            position.dt.year, position.dt.month, self._ayanamsa
        )
        subtracted = position.lon.decimal - ayanamsa
        if subtracted < 0:
            subtracted = 360 + subtracted
        return degree_from_decimal(subtracted)

    def _house(self, lon: Degree, sign: zodiac.Sign, cusps: List[float] = None) -> int:
        if cusps is None or not cusps:
            return sign.id

        return zodiac.calculate_house(lon.decimal, cusps)
