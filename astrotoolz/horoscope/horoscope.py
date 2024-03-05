from datetime import datetime
from typing import Dict, List, Optional, Tuple

from astrotoolz.core.angles.angle import Angle
from astrotoolz.core.enums import CoordinateSystem, NodeCalc
from astrotoolz.core.events.aspect import Aspect
from astrotoolz.core.points import SUN
from astrotoolz.core.units.degree import Degree
from astrotoolz.core.units.degree_converter import degree_from_decimal
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.horoscope.horoscope_config import HoroscopeConfig


class Horoscope:
    dt: datetime
    coord_system: CoordinateSystem
    node_calc: NodeCalc
    config: HoroscopeConfig
    mgps: List[MappedPosition]
    pmgps: List[MappedPosition]
    angles: Dict[str, List[Angle]]
    aspects: Dict[str, List[Aspect]]
    cusps: List[float]

    def __init__(
        self,
        dt: datetime,
        coord_system: CoordinateSystem,
        node_calc: NodeCalc,
        config: HoroscopeConfig,
        mps: List[MappedPosition],
        pmgps: List[MappedPosition],
        angles: Dict[str, List[Angle]],
        aspects: Dict[str, List[Aspect]],
        cusps: List[float],
    ):
        self.dt = dt
        self.coord_system = coord_system
        self.node_calc = node_calc
        self.config = config
        self.mgps = mps
        self.pmgps = pmgps
        self.angles = angles
        self.aspects = aspects
        self.cusps = cusps

        self.indices = {}

        for p in config.points:
            self.indices[p] = {}
            for f in ["dec", "lat", "speed", "phase"]:
                self.indices[p][f] = self.get_daily_index(p, f)

    def get_daily_index(self, point: str, field_name: str) -> str:
        mgp = next(mgp for mgp in self.mgps if mgp.point == point)
        pmgp = (
            next(pmgp for pmgp in self.pmgps if pmgp.point == point)
            if self.pmgps is not None
            else None
        )

        if pmgp is None:
            return ""

        if field_name == "dec":
            return self._get_index(mgp.dec, pmgp.dec)
        elif field_name == "lat":
            return self._get_index(mgp.lat, pmgp.lat)
        elif field_name == "speed":
            return self._get_index(mgp.speed, pmgp.speed)
        elif field_name == "phase":
            phase_today = self.phase(point)
            phase_yesterday = self._phase(point, self.pmgps)
            return self._get_index(phase_today, phase_yesterday)

    def phase(self, point: str) -> Optional[Degree]:
        return self._phase(point, self.mgps)

    def _phase(self, point: str, list: List[MappedPosition]) -> Optional[Degree]:
        source = next(mgp for mgp in list if mgp.point == point)

        sun = next((mgp for mgp in list if mgp.point == SUN), None)

        if sun is None:
            return None
        return degree_from_decimal(Angle(source, sun).circular_diff)

    def _get_index(self, current_degree: Degree, previous_degree: Degree) -> str:
        if current_degree == previous_degree:
            return "="
        elif current_degree > previous_degree:
            return "+"
        elif current_degree < previous_degree:
            return "-"
