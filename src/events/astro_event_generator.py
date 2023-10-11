from datetime import datetime as dt
from typing import List, Type
from enum import Enum, auto
from astro_event import AstroEvent

class Zodiac(Enum):
    GEO = auto()
    HELIO = auto() 

class AstroEventGenerator:
    start: dt
    end: dt
    interval_minutes: int
    planets: List[str]
    zodiac: Zodiac
    events: List[Type[AstroEvent]]
    
    def _generate_geo(self):
        pass
    
    def _generate_helio(self):
        pass

    def generate(self):
        if (self.zodiac == Zodiac.GEO):
            return self._generate_geo()
        else:
            return self._generate_helio()