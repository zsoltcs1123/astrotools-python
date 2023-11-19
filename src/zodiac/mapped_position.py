from core.base_position import BasePosition
import core.swisseph_api as swe_api
from core.degree import Degree
from typing import List
from dataclasses import dataclass
import zodiac.division as zd


@dataclass
class MappedPosition:
    def __init__(self, base_position: BasePosition):
        self.base_position = base_position
        self.retrograde = self.base_position.speed.dec < 0
        self.stationary = self.base_position.speed.dec == 0
        self.direction = 'R' if self.retrograde else 'S' if self.stationary else 'D'
        self.sign = zd.map_sign(self.base_position.lon.dec)
        self.decan = zd.map_decan(self.base_position.lon.dec)
        self.term = zd.map_term(self.base_position.lon.dec)
        self.tropical_pos = MappedPosition.float_to_zodiacal(self.base_position.lon)
        self.sidereal_lon = self.calculate_sidereal_lon()
        self.sidereal_pos = MappedPosition.float_to_zodiacal(self.sidereal_lon)
        self.nakshatra = zd.map_nakshatra(self.sidereal_lon.dec)

    def calculate_sidereal_lon(self):
        ayanamsa = swe_api.get_ayanamsha(self.base_position.dt.year, self.base_position.dt.month, 'LAHIRI')
        subtracted = self.base_position.lon.dec - ayanamsa
        if (subtracted < 0):
            subtracted = 360 + subtracted
        return Degree.from_decimal(subtracted)
    
    @staticmethod
    def float_to_zodiacal(lon: Degree) -> str:
        sign_name = zd.map_sign(lon.dec).name
        sign_nr = (int)(lon.dec / 30)
        deg = (int)(lon.dec - sign_nr * 30)
        mins = lon.dms.minutes
        return f"{deg}{sign_name[:3]}{mins}"

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[BasePosition]):
        return [cls(position) for position in planetary_positions]

    def __repr__(self):
        return (
            f"{repr(self.base_position)}\n"
            f"Tropical position: {self.tropical_pos}\n"
            f"Sign: {self.sign.name}\n"
            f"Decan: {self.decan.name}\n"
            f"Term: {self.term.name}\n"
            f"Sidereal position: {self.sidereal_pos}\n"
            f"Nakshatra: {self.nakshatra.name}"
        )

    def house(self, cusps: List[float] = None):
        if cusps is None:
            return self.sign.id

        # Normalize values relative to the Ascendant (first cusp).
        normalized_cusps = [(cusp - cusps[0]) % 360 for cusp in cusps]
        normalized_longitude = (self.base_position.lon.dec - cusps[0]) % 360

        for i in range(0, 11):  # Only loop until the 11th cusp
            if normalized_cusps[i] <= normalized_longitude < normalized_cusps[i + 1]:
                return i + 1

        # If we haven't returned by this point, the planet is in the 12th house
        return 12
