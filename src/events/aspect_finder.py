from itertools import groupby
from core.enums import AspectType
from typing import List, Dict
from core.angle import Angle
from events.aspect import Aspect
from objects.orb_map import OrbMap


class AspectFinder:
    ASPECTS = {
        AspectType.CONJUNCTION: (0,),
        AspectType.SEXTILE: (60, 300),
        AspectType.QUINTILE: (72, 144, 216, 288),
        AspectType.SQUARE: (90, 270),
        AspectType.TRINE: (120, 240),
        AspectType.OPPOSITION: (180,),
        AspectType.INCONJUNCT: (150,),
    }

    def __init__(self, orb_map: OrbMap, aspects_include: List[AspectType]):
        self.orb_map = orb_map
        self.aspects_include = aspects_include

    def find_aspects_list(self, angles: List[Angle]) -> List[Aspect]:
        aspects = []

        for angle in angles:
            for asp_type in self.aspects_include:
                orbs = self.orb_map.get_aspects_orbs(angle.source.name)
                orb = orbs[asp_type]
                negative = angle.diff - orb
                positive = angle.diff + orb
                
                asp_values = self.ASPECTS[asp_type]
                
                for asp_value in asp_values:
                    if asp_value >= negative and asp_value <= positive:
                        asp = Aspect(angle.source.dt, angle, asp_type, asp_value)
                        aspects.append(asp)
        return aspects

    def find_exact_aspects(self, angles: List[Angle]) -> List[Aspect]:
        # sort by dt to ensure that the min function will return the correct element (the first aspect when the diff is smallest)
        aspects = sorted(self.find_aspects_list(angles), key=lambda aspect: aspect.angle.dt)

        groups = groupby(
            aspects, key=lambda asp: f"{asp.type.name} vs {asp.angle.target.name}"
        )

        aspects = []

        for key, group in groups:
            min_diff_asp = min(
                group, key=lambda asp: abs(asp.angle.diff - asp.target_diff)
            )

            aspects.append(min_diff_asp)

        return aspects

    def find_aspects(self, angles: Dict[str, List[Angle]]) -> Dict[str, List[Aspect]]:
        aspects = {}

        for point, angle_list in angles.items():
            aspects[point] = []
            for angle in angle_list:
                orbs = self.orb_map.get_aspects_orbs(angle.source.name)
                for asp_to_orb in orbs:
                    negative = angle.diff - asp_to_orb[1]
                    positive = angle.diff + asp_to_orb[1]
                    asp_value = self.ASPECTS[asp_to_orb[0]][0]

                    if asp_value >= negative and asp_value <= positive:
                        asp = Aspect(angle.source.dt, angle, asp_to_orb[0], angle.diff)
                        aspects[point].append(asp)
        return aspects
