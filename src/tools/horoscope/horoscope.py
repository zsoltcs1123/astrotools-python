from datetime import datetime
from typing import List, Dict
from tools.horoscope.horoscope_config import HoroscopeConfig
from zodiac.mapped_position import MappedPosition as mp
from core.angle import Angle
from events.aspect import Aspect


class Horoscope:
    dt: datetime
    config: HoroscopeConfig
    mps: List[mp]
    angles: Dict[str, List[Angle]]
    aspects: Dict[str, List[Aspect]]
    cusps: List[float]

    def __init__(
        self,
        dt: datetime,
        config: HoroscopeConfig,
        mps: List[mp],
        angles: Dict[str, List[Angle]],
        aspects: Dict[str, List[Aspect]],
        cusps: List[float],
    ):
        self.dt = dt
        self.config = config
        self.mps = mps
        self.angles = angles
        self.aspects = aspects
        self.cusps = cusps

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
