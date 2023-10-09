from core.planetary_position import PlanetaryPosition
from typing import  List
from dataclasses import dataclass
import zodiac.division as zd


@dataclass
class MappedPlanetaryPosition:
    def __init__(self, position: PlanetaryPosition):
        self.position = position

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[PlanetaryPosition]):
        return [cls(position) for position in planetary_positions]

    @property
    def retrograde(self) -> bool:
        return self.position.speed < 0
    
    @property
    def stationary(self) -> bool:
        return self.position.speed == 0
    
    @property
    def direction(self) -> str:
        return 'retrograde' if self.retrograde else 'stationary' if self.stationary else 'direct'

    @property
    def sign(self) -> zd.Sign:
        return zd.map_sign(self.position.lon)

    @property
    def decan(self) -> zd.Decan:
        return zd.map_decan(self.position.lon)

    @property
    def term(self) -> zd.Term:
        return zd.map_term(self.position.lon)
    
    def __repr__(self):
        return f"{repr(self.position)}\nSign: {self.sign.name}\nDecan: {self.decan.name}\nTerm: {self.term.name}"
