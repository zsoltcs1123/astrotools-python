from datetime import datetime
from typing import List, Dict
from tools.horoscope.horoscope_config import HoroscopeConfig
from core.position_factory import PositionFactory
from core.angle_factory import AngleFactory
from events.aspect_finder import AspectFinder
from core.base_position import BasePosition as bp
from zodiac.mapped_position import MappedPosition as mp
from core.angle import Angle
from objects.points import PLANETS
from events.aspect import Aspect
import core.swisseph_api as swe_api


class Horoscope:
    dt: datetime
    config: HoroscopeConfig
    points: List[mp]
    angles: Dict[str, List[Angle]]
    aspects: Dict[str, List[Aspect]]
    cusps: List[float]

    def __init__(self,
                 dt: datetime,
                 config: HoroscopeConfig,
                 position_factory: PositionFactory,
                 angle_factory: AngleFactory = None,
                 aspect_finder: AspectFinder = None):
        self.dt = dt
        self.config = config
        self.cusps, self.ascmc = swe_api.get_houses_and_ascmc(
            dt, config.lat, config.lon, config.house_system)

        self.points = []

        self.angles = {}
        self.aspects = []
        planets = [planet for planet in PLANETS]

        asc_pos = bp(self.dt, 'ASC', self.ascmc[0], 0, 0, 0, 0)
        mc_pos = bp(self.dt, 'MC', self.ascmc[1], 0, 0, 0, 0)

        self.points.append(mp(asc_pos))
        self.points.append(mp(mc_pos))

        self.angles['ASC'] = []
        self.angles['MC'] = []

        # angles
        for planet in planets:
            pos = position_factory.create_position(planet, self.dt)
            mpos = mp(pos)
            self.points.append(mpos)
            angles = angle_factory.get_multiple_angles(planet, self.dt)

            self.angles[planet] = angles

            # ASC and MC
            self.angles['ASC'].append(Angle(pos, asc_pos))
            self.angles['MC'].append(Angle(pos, mc_pos))

        # aspects
        self.aspects = aspect_finder.find_aspects(self.angles)

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
