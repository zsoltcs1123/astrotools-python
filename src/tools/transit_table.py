from dataclasses import dataclass
from typing import List, Dict
from core.angle import Angle
from events.aspect import Aspect
from events.aspect_finder import AspectFinder
from points.orb_map import OrbMap 

@dataclass
class TransitTable:
    angles: Dict[str, List[Angle]]
    aspects: Dict[str, List[Aspect]]
    
    def __init__(self, angles: List[Angle]):
        self.angles = angles
        
        orb_map = OrbMap()
        asp_finder = AspectFinder(orb_map)
        self.aspects = asp_finder.find_aspects(self.angles)