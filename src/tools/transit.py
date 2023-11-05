
from typing import List
from dataclasses import dataclass
from core.angle import Angle
from tools.horoscope import Horoscope
from tools.transit_table import TransitTable

@dataclass
class Transit:
    natal_horoscope: Horoscope
    transit_horoscope: Horoscope
    
    def __init__(self, natal_horoscope: Horoscope, transit_horoscope: Horoscope):
        self.natal_horoscope = natal_horoscope
        self.transit_horoscope = transit_horoscope
        
        if self.natal_horoscope.coord_system != self.transit_horoscope.coord_system \
            or self.natal_horoscope.house_system != self.transit_horoscope.house_system \
            or self.natal_horoscope.zodiac_system != self.transit_horoscope.zodiac_system:
                raise Exception('Incompatible horoscopes')
            
    
    def generate_transit_table(self, points_filter: List[str] = []) -> TransitTable:
        angles = {}
        for point in [p for p in self.natal_horoscope.points if p.position.name not in points_filter]:
            point_angles = []
            for transit_point in [tp for tp in self.transit_horoscope.points if tp.position.name not in points_filter]:
                angle = Angle(transit_point.position.dt, point.position, transit_point.position)
                point_angles.append(angle)
            angles[point.position.name] = point_angles
        return TransitTable(angles)
        
    