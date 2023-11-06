from typing import List
from datetime import datetime as dt
from core.position import Position
from objects.points import NN, PLANETS, SN
from util.interval import calculate_intervals
import core.swisseph_api as swe_api


class PositionFactory:
    def __init__(self, node_calc):
        self.node_calc = node_calc

    def _planet(self, planet_name: str, dt: dt) -> Position:
        lon, lat, speed = swe_api.get_ecliptic_position(planet_name, dt)
        ra, dec = swe_api.get_equatorial_position(planet_name, dt)
        return Position(dt, planet_name, lon, lat, speed, ra, dec)

    def _north_node(self, dt: dt) -> Position:
        pos = self._planet(self.node_calc, dt)
        pos.name = NN  
        return pos

    def _south_node(self, dt: dt) -> Position:
        nn = self._north_node(dt)
        lon = (nn.lon + 180.0) % 360
        lat = 0
        speed = -nn.speed
        ra = (nn.ra + 12.0) % 24.0 
        dec = -nn.dec
        return Position(dt, SN, lon, lat, speed, ra, dec)  

    def create_position(self, point: str, dt: dt) -> Position:
        if point in PLANETS:
            return self._planet(point, dt)
        elif point == NN:
            return self._north_node(dt)
        elif point == SN:
            return self._south_node(dt)
        else:
            raise(ValueError(f'{point} not supported'))

    def create_positions(self, point: str, start: dt, end: dt, interval_minutes: int) -> List[Position]:
        dts = calculate_intervals(start, end, interval_minutes)
        return [self.create_position(point, dt) for dt in dts]
    
        
    
    
