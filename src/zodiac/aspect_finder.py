from zodiac.enums import AspectType
from typing import List
from core.angle import Angle
from events.aspect import Aspect
from zodiac.orb_map import OrbMap

class AspectFinder:
    
    ASPECTS = {
        AspectType.CONJUNCTION: (0,),
        AspectType.SEXTILE: (60, 300),
        AspectType.QUINTILE: (72, 144, 216, 288),
        AspectType.SQUARE: (90, 270),
        AspectType.TRINE: (120, 240),
        AspectType.OPPOSITION: (180,),
        AspectType.INCONJUNCT: (150, )
    }
    
    
    def __init__(self, orb_map: OrbMap):
        self.orb_map = orb_map
        
    def find_aspects(self, angles: List[List[Angle]]) -> List[Aspect]:
        aspects = []
        
        merged = []
        for angle_list in angles:
            merged.extend(angle_list)
            
        for angle in merged:
            orbs = self.orb_map.get_aspects_orbs(angle.pos1.planet)
            for asp_to_orb in orbs:
                negative = angle.diff - asp_to_orb[1]
                positive = angle.diff + asp_to_orb[1]
                asp_value = self.ASPECTS[asp_to_orb[0]][0]
                
                if asp_value >= negative and asp_value <= positive:
                    asp = Aspect(angle.pos1.dt, angle, asp_to_orb[0], angle.diff)
                    aspects.append(asp)
        return aspects