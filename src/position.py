from datetime import datetime
from dataclasses import dataclass


@dataclass
class Position:
    time: datetime
    planet: str
    lon: float

    def __hash__(self):
        return hash((self.time, self.planet, self.lon))

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.time == other.time and self.planet == other.planet and self.lon == other.lon

    def __repr__(self):
        return f"[{self.planet}, {self.lon:.3f}])"
