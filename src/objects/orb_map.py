from dataclasses import dataclass
from typing import Dict, List, Tuple
from core.enums import AspectType
from objects.points import ALL_POINTS

AspectToOrb = Tuple[AspectType, int]


@dataclass
class OrbMap:
    orbs: Dict[str, Dict[AspectType, int]] # {point_name to {AspectType, orb}}

    @classmethod
    def _get_default_orbs(cls) -> Dict[str, List[AspectToOrb]]:
        orb_map = {}
        for planet in ALL_POINTS + ["ASC", "MC"]:
            aspect_types_orbs = {
                AspectType.CONJUNCTION, 10 if planet in ["sun", "moon"] else 8,
                AspectType.SEXTILE, 6 if planet in ["sun", "moon"] else 4,
                AspectType.SQUARE, 10 if planet in ["sun", "moon"] else 8,
                AspectType.TRINE, 10 if planet in ["sun", "moon"] else 8,
                AspectType.OPPOSITION, 10 if planet in ["sun", "moon"] else 8,
                AspectType.QUINTILE, 8 if planet in ["sun", "moon"] else 6,
                AspectType.INCONJUNCT, 5 if planet in ["sun", "moon"] else 3,
            }
            orb_map[planet] = aspect_types_orbs
        return orb_map

    @classmethod
    def _generate_orbs(cls, orb: float) -> Dict[str, List[AspectToOrb]]:
        orb_map = {}
        for planet in ALL_POINTS + ["ASC", "MC"]:
            asp_types_orbs = {}
            for asp_type in AspectType:
                asp_types_orbs[asp_type] =  orb
            orb_map[planet] = asp_types_orbs
        return orb_map

    @classmethod
    def default_orb_map(cls):
        return cls(cls._get_default_orbs())

    @classmethod
    def orb_map(cls, orb: float):
        return cls(cls._generate_orbs(orb))

    def get_aspects_orbs(self, planet: str) -> Dict[AspectType, int]:
        return self.orbs.get(planet)
