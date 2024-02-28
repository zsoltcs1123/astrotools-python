from abc import ABC, abstractmethod
from typing import List

import astrotoolz.core.ephemeris.swisseph_api as swe_api
import astrotoolz.core.zodiac.division as zodiac
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.units.degree import Degree
from astrotoolz.core.units.degree_converter import degree_from_decimal
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.core.zodiac.tropical_attributes import TropicalAttributes
from astrotoolz.core.zodiac.vedic_attributes import VedicAttributes
from astrotoolz.util.logger_base import LoggerBase


class PositionMapper(LoggerBase, ABC):

    def __init__(self, ayanamsa: str = "LAHIRI"):
        super().__init__()
        self._ayanamsa = ayanamsa

    def map_positions(self, positions: List[BasePosition]) -> List[BasePosition]:
        self._logger.info("Mapping astrological data...")
        return [self.map_position(position) for position in positions]

    @abstractmethod
    def map_position(self, position: BasePosition) -> MappedPosition:
        pass

    def map_tropical_attributes(self, position: BasePosition) -> TropicalAttributes:

        lon = position.lon
        zodiacal_position = zodiac.degree_to_zodiacal(lon)
        sign = zodiac.map_sign(lon.decimal)
        sign_ruler = sign.modern_ruler
        decan = zodiac.map_decan(lon.decimal)
        term = zodiac.map_term(lon.decimal)
        house = self._house(lon, sign)

        return TropicalAttributes(
            lon, zodiacal_position, sign, sign_ruler, decan, term, house
        )

    def map_vedic_attributes(self, position: BasePosition) -> VedicAttributes:
        lon = self._calculate_sidereal_lon(position)
        zodiacal_position = zodiac.degree_to_zodiacal(lon)
        sign = zodiac.map_sign(lon.decimal)
        sign_ruler = sign.vedic_ruler
        nakshatra = zodiac.map_nakshatra(lon.decimal)
        nakshatra_ruler = nakshatra.ruler
        house = self._house(lon, sign)

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
        if cusps is None:
            return sign.id

        return zodiac.calculate_house(lon.decimal, cusps)
