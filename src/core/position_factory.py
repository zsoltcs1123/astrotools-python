from datetime import datetime as dt
from core.position import Position
from objects.points import NN, PLANETS, SN
import core.swisseph_api as swe_api
from util.interval import calculate_intervals

class PositionFactory:
    def __init__(self, node_calc='MEAN_NODE'):
        self.node_calc = node_calc

    def _planet(self, planet_name: str, dt: dt):
        lon, lat, speed = swe_api.get_ecliptic_position(planet_name, dt)
        ra, dec = swe_api.get_equatorial_position(planet_name, dt)
        return Position(dt, planet_name, lon, lat, speed, ra, dec)

    def _north_node(self, dt: dt):
        pos = self._planet(self.node_calc, dt)
        pos.name = NN  
        return pos

    def _south_node(self, dt: dt):
        nn = self._north_node(dt)
        lon = (nn.lon + 180.0) % 360
        lat = 0
        speed = -nn.speed
        ra = (nn.ra + 12.0) % 24.0 
        dec = -nn.dec
        return Position(dt, NN, lon, lat, speed, ra, dec)  

    def create_position(self, point: str, dt: dt):
        if point in PLANETS:
            return self._planet(point, dt)
        elif point == NN:
            return self._north_node(dt)
        elif point == SN:
            return self._south_node(dt)

    def create_positions(self, point: str, start: dt, end: dt, interval_minutes: int):
        dts = calculate_intervals(start, end, interval_minutes)
        return [self.create_position(point, dt) for dt in dts]
