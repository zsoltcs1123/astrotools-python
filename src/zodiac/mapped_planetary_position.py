from core.planetary_position import PlanetaryPosition
from typing import List
from dataclasses import dataclass
from zodiac.degree_converter import calculate_zodiac_position_dmm
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
        self.zodiac_pos = calculate_zodiac_position_dmm(self.position.lon)

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[PlanetaryPosition]):
        return [cls(position) for position in planetary_positions]

    def __repr__(self):
        return f"{repr(self.position)}\nSign: {self.sign.name}\nDecan: {self.decan.name}\nTerm: {self.term.name}"
