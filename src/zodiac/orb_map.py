from dataclasses import dataclass
from typing import Dict, List, Tuple
from zodiac.enums import AspectType
from core.planets import PLANETS

AspectToOrb = Tuple[AspectType, int]

@dataclass
class OrbMap:
    def __init__(self):
        self.orb_map = self._get_default_orb_map()
        
    def _get_default_orb_map(self) -> Dict[str, List[AspectToOrb]]:
        orb_map = {}
        for planet in PLANETS:
            aspect_types_orbs = [
                (AspectType.CONJUNCTION, 10 if planet in ['sun', 'moon'] else 8),
                (AspectType.SEXTILE, 6 if planet in ['sun', 'moon'] else 4),
                (AspectType.SQUARE, 10 if planet in ['sun', 'moon'] else 8),
                (AspectType.TRINE, 10 if planet in ['sun', 'moon'] else 8),
                (AspectType.OPPOSITION, 10 if planet in ['sun', 'moon'] else 8),
                (AspectType.QUINTILE, 8 if planet in ['sun', 'moon'] else 6),
            ]
            orb_map[planet] = aspect_types_orbs
        return orb_map
    
    def get_aspects_orbs(self, planet: str)-> List[AspectToOrb]:
        return self.orb_map.get(planet)