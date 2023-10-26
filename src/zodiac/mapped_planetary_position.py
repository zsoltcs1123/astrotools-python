from core.planetary_position import PlanetaryPosition
from typing import List
from dataclasses import dataclass
import zodiac.division as zd


@dataclass
class MappedPlanetaryPosition:
    def __init__(self, position: PlanetaryPosition):
        self.position = position
        self.retrograde = self.position.speed < 0
        self.stationary = self.position.speed == 0
        self.direction = 'retrograde' if self.retrograde else 'stationary' if self.stationary else 'direct'
        self.sign = zd.map_sign(self.position.lon)
        self.decan = zd.map_decan(self.position.lon)
        self.term = zd.map_term(self.position.lon)
        self.zodiac_pos = self.calculate_zodiac_position()

    def calculate_zodiac_position(self) -> str:
        sign_nr = (int)(self.position.lon / 30)
        deg = (int)(self.position.lon - sign_nr * 30)
        mins = self.position.zodiac_lon[1]
        return f"{deg}{self.sign.name[:3]}{mins}"
    

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[PlanetaryPosition]):
        return [cls(position) for position in planetary_positions]

    def __repr__(self):
        return f"{repr(self.position)}\nSign: {self.sign.name}\nDecan: {self.decan.name}\nTerm: {self.term.name}"