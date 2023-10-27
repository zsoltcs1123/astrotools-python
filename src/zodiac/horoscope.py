import swisseph as swe
from datetime import datetime
import core.swisseph_api as swe_api
from zodiac.enums import HouseSystem, Zodiac, CoordinateSystem
from core.planetary_position import PlanetaryPosition as pp
from zodiac.mapped_planetary_position import MappedPlanetaryPosition as mpp
from core.planet import PLANETS


class Horoscope:
    def __init__(self, dt: datetime, lat: float, lon: float, 
                 house_system: HouseSystem = HouseSystem.PLACIDUS, 
                 zodiac: Zodiac = Zodiac.TROPICAL, 
                 coord_system: CoordinateSystem = CoordinateSystem.GEO):
        self.dt = dt
        self.lon = lon
        self.lat = lat
        self.house_system = house_system
        self.zodiac_system = zodiac
        self.coord_system = coord_system

        self.cusps, self.ascmc = swe_api.get_houses_and_ascmc(dt, lat, lon, house_system)
        
        self.planets = []
        planets = [planet for planet in PLANETS]
        for planet in planets:
            pos = pp.from_datetime(planet, self.dt)
            mpos = mpp(pos)
            self.planets.append(mpos)
        

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


