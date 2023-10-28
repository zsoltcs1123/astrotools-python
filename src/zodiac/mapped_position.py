from core.position import Position
from typing import List
from dataclasses import dataclass
from zodiac.degree_converter import float_to_zodiacal
import zodiac.division as zd


@dataclass
class MappedPosition:
    def __init__(self, position: Position):
        self.position = position
        self.retrograde = self.position.speed < 0
        self.stationary = self.position.speed == 0
        self.direction = 'R' if self.retrograde else 'S' if self.stationary else 'D'
        self.sign = zd.map_sign(self.position.lon)
        self.decan = zd.map_decan(self.position.lon)
        self.term = zd.map_term(self.position.lon)
        self.zodiac_pos = float_to_zodiacal(self.position.lon)

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[Position]):
        return [cls(position) for position in planetary_positions]

    def __repr__(self):
        return f"{repr(self.position)}\nSign: {self.sign.name}\nDecan: {self.decan.name}\nTerm: {self.term.name}"
    
    def house(self, cusps: List[float] = None):
        if cusps is None:
            return self.sign.id
        
        # Normalize values relative to the Ascendant (first cusp).
        normalized_cusps = [(cusp - cusps[0]) % 360 for cusp in cusps]
        normalized_longitude = (self.position.lon - cusps[0]) % 360
        
        for i in range(0, 11):  # Only loop until the 11th cusp
            if normalized_cusps[i] <= normalized_longitude < normalized_cusps[i + 1]:
                return i + 1
            
        # If we haven't returned by this point, the planet is in the 12th house
        return 12
