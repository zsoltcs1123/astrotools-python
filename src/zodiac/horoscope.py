from datetime import datetime
from typing import List, Dict
import core.swisseph_api as swe_api
from zodiac.enums import HouseSystem, Zodiac, CoordinateSystem
from core.planetary_position import PlanetaryPosition as pp
from zodiac.mapped_planetary_position import MappedPlanetaryPosition as mpp
from core.angle import get_all_angles
from core.angle import Angle
from core.planets import PLANETS
from zodiac.aspect_finder import AspectFinder
from zodiac.orb_map import OrbMap
from events.aspect import Aspect
from zodiac.transit_table import TransitTable


class Horoscope:
    points: List[mpp]
    angles: Dict[str, List[Angle]]
    aspects: List[Aspect]
    cusps: List[float]
    
    
    def __init__(self, dt: datetime, lat: float, lon: float,
                 name: str,
                 house_system: HouseSystem = HouseSystem.PLACIDUS,
                 zodiac: Zodiac = Zodiac.TROPICAL,
                 coord_system: CoordinateSystem = CoordinateSystem.GEO):
        self.dt = dt
        self.lon = lon
        self.lat = lat
        self.name = name
        self.house_system = house_system
        self.zodiac_system = zodiac
        self.coord_system = coord_system

        self.cusps, self.ascmc = swe_api.get_houses_and_ascmc(
            dt, lat, lon, house_system)

        self.points = []
        self.angles = {}
        self.aspects = []
        planets = [planet for planet in PLANETS]

        asc_pos = pp(self.dt, 'ASC', self.ascmc[0], 0, 0, 0, 0)
        mc_pos = pp(self.dt, 'MC', self.ascmc[1], 0, 0, 0, 0)

        self.points.append(mpp(asc_pos))
        self.points.append(mpp(mc_pos))
        
        self.angles['ASC'] = []
        self.angles['MC'] = []

        # angles
        for planet in planets:
            pos = pp.from_datetime(planet, self.dt)
            mpos = mpp(pos)
            self.points.append(mpos)
            angles = get_all_angles(planet, self.dt, self.dt, 1)

            self.angles.update(angles)

            # ASC and MC
            self.angles['ASC'].append(Angle(self.dt, pos, asc_pos))
            self.angles['MC'].append(Angle(self.dt, pos, mc_pos))


        # aspects
        orb_map = OrbMap()
        asp_finder = AspectFinder(orb_map)
        self.aspects = asp_finder.find_aspects(self.angles)
        
    def generate_transit_table(self, transit_horoscope: 'Horoscope') -> TransitTable:
        angles = {}
        for point in [p for p in self.points if p.position.planet not in ['ASC', 'MC']]:
            point_angles = []
            for transit_point in [tp for tp in transit_horoscope.points if tp.position.planet not in ['ASC', 'MC']]:
                angle = Angle(transit_point.position.dt, point.position, transit_point.position)
                point_angles.append(angle)
            angles[point.position.planet] = point_angles
        return TransitTable(angles)
                
                

    @property
    def ascendant(self):
        return self.ascmc[0]

    @property
    def mc(self):
        return self.ascmc[1]

    @property
    def ic(self):
        ic = self.mc + 180
        if ic > 360:
            ic -= 360
        return ic

    @property
    def dc(self):
        dc = self.ascendant + 180
        if dc > 360:
            dc -= 360
        return dc
