from datetime import datetime as dt
from typing import List, Type
from astro_event import AstroEvent
from zodiac.enums import CoordinateSystem

class AstroEventGenerator:
    start: dt
    end: dt
    interval_minutes: int
    planets: List[str]
    coordinate_system: CoordinateSystem
    events: List[Type[AstroEvent]]
    
    def _generate_geo(self):
        pass
    
    def _generate_helio(self):
        pass

    def generate(self):
        if (self.zodiac == CoordinateSystem.GEO):
            return self._generate_geo()
        else:
            return self._generate_helio()