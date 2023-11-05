from datetime import datetime
from typing import List, Dict
import core.swisseph_api as swe_api
from core.enums import HouseSystem, Zodiac, CoordinateSystem
from core.position import Position as pp
from util.interval import calculate_intervals
from zodiac.mapped_position import MappedPosition as mp
from core.angle import get_all_angles
from core.angle import Angle
from points.planets import PLANETS
from events.aspect_finder import AspectFinder
from points.orb_map import OrbMap
from events.aspect import Aspect


class Horoscope:
    points: List[mp]
    angles: Dict[str, List[Angle]]
    aspects: Dict[str, List[Aspect]]
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

        self.points.append(mp(asc_pos))
        self.points.append(mp(mc_pos))

        self.angles['ASC'] = []
        self.angles['MC'] = []

        # angles
        for planet in planets:
            pos = pp.from_datetime(planet, self.dt)
            mpos = mp(pos)
            self.points.append(mpos)
            angles = get_all_angles(planet, self.dt)

            self.angles.update(angles)

            # ASC and MC
            self.angles['ASC'].append(Angle(self.dt, pos, asc_pos))
            self.angles['MC'].append(Angle(self.dt, pos, mc_pos))

        # aspects
        orb_map = OrbMap()
        asp_finder = AspectFinder(orb_map)
        self.aspects = asp_finder.find_aspects(self.angles)

    @classmethod
    def from_datetime_range(cls, start: datetime, end: datetime, interval_minutes: int, lat: float, lon: float,
                            name: str,
                            house_system: HouseSystem = HouseSystem.PLACIDUS,
                            zodiac: Zodiac = Zodiac.TROPICAL,
                            coord_system: CoordinateSystem = CoordinateSystem.GEO):

        dts = calculate_intervals(start, end, interval_minutes)
        return [cls(dt, lat, lon, name, house_system, zodiac, coord_system) for dt in dts]

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
