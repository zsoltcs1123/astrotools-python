from dataclasses import dataclass
from typing import List
from core.degree import Degree
from core.geo_position import GeoPosition
import zodiac.division as zd


@dataclass
class TropicalAttributes:
    _base_position: GeoPosition
    lon: Degree
    position: str
    sign: zd.Sign
    sign_ruler: str
    decan: zd.Decan
    term: zd.Term

    def __init__(self, base_position: GeoPosition):
        self._base_position = base_position
        self.lon = base_position.lon
        self.position = zd.degree_to_zodiacal(base_position.lon)
        self.sign = zd.map_sign(base_position.lon.decimal)
        self.sign_ruler = self.sign.modern_ruler
        self.decan = zd.map_decan(base_position.lon.decimal)
        self.term = zd.map_term(base_position.lon.decimal)

    def house(self, cusps: List[float] = None) -> int:
        if cusps is None:
            return self.sign.id

        return zd.calculate_house(self.lon.decimal, cusps)
