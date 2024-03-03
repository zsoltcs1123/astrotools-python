from datetime import datetime, timedelta
from typing import Dict, List, Optional

import astrotoolz.core.ephemeris.swisseph_api as swe_api
from astrotoolz.core.angles.angle import Angle
from astrotoolz.core.angles.angle_factory import AngleFactory
from astrotoolz.core.angles.angle_target_calculator import AngleTargetCalculator
from astrotoolz.core.enums import CoordinateSystem, Zodiac
from astrotoolz.core.events.aspect import Aspect
from astrotoolz.core.events.factory.aspect_factory import AspectFactory
from astrotoolz.core.points import ASC, LUMINARIES, MC
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.positions.factory.position_factory import PositionFactory
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper
from astrotoolz.timeline.aspect_config import AspectsConfig
from astrotoolz.tools.horoscope.horoscope import Horoscope
from astrotoolz.tools.horoscope.horoscope_config import HoroscopeConfig
from astrotoolz.tools.horoscope.vedic_horoscope import VedicHoroscope
from astrotoolz.util.interval import calculate_intervals


class HoroscopeFactory:

    def __init__(
        self,
        coord_system: CoordinateSystem,
        position_factory: PositionFactory,
        position_mapper: PositionMapper,
        angle_target_calculator: Optional[AngleTargetCalculator],
        angle_factory: Optional[AngleFactory],
        aspect_factory: Optional[AspectFactory],
    ):
        self.coord_system = coord_system
        self.position_factory = position_factory
        self.position_mapper = position_mapper
        self.angle_target_calculator = angle_target_calculator
        self.angle_factory = angle_factory
        self.aspect_factory = aspect_factory

    def create_horoscopes(
        self,
        start: datetime,
        end: datetime,
        interval_minutes: int,
        config: HoroscopeConfig,
    ) -> List[Horoscope]:
        dts = calculate_intervals(start, end, interval_minutes)

        return [self.create_horoscope(dt, config) for dt in dts]

    def create_horoscope(self, dt: datetime, config: HoroscopeConfig) -> Horoscope:
        cusps, ascmc = (
            self._calculate_cusps_ascmc(dt, config)
            if ASC or MC in config.points
            else ([], [])
        )

        mps = self._generate_positions(dt, config, ascmc, cusps)
        pmps = self._generate_positions(dt - timedelta(days=1), config, ascmc, cusps)

        grouped_mps = self._group_bps(mps)
        angle_targets = self._get_angle_targets(config.points)
        angles = self.angle_factory.create_angles_dict(grouped_mps, angle_targets)
        aspects = self._generate_aspects(angles, config.aspects)

        for p, asp_list in aspects.items():
            self.position_mapper.map_aspects(asp_list, [config.zodiac])

        if config.zodiac == Zodiac.TROPICAL:
            return Horoscope(
                dt, self.coord_system, config, mps, pmps, angles, aspects, cusps
            )
        else:
            mp_asc = next(mp for mp in mps if mp.point == ASC)
            cusps = self._transform_cusps(dt, config, cusps, mp_asc.vedic.lon.decimal)
            return VedicHoroscope(
                dt, self.coord_system, config, mps, angles, aspects, cusps
            )

    def _generate_positions(
        self, dt: datetime, config: HoroscopeConfig, ascmc: tuple, cusps: tuple
    ) -> List[MappedPosition]:
        mps = []
        for point in config.points:
            bp = self._create_bp(point, dt, ascmc)
            mp = self.position_mapper.map_position(bp, [config.zodiac], cusps)
            mps.append(mp)
        return mps

    def _create_bp(self, point: str, dt: datetime, ascmc: tuple) -> BasePosition:
        if point == ASC:
            return self.position_factory.create_angular(point, dt, ascmc[0])
        elif point == MC:
            return self.position_factory.create_angular(point, dt, ascmc[1])
        else:
            return self.position_factory.create_position(point, dt)

    @staticmethod
    def _group_bps(bps: List[BasePosition]) -> Dict[str, List[BasePosition]]:
        grouped_mps = {}
        for mpp in bps:
            if mpp.point not in grouped_mps:
                grouped_mps[mpp.point] = [mpp]
            else:
                grouped_mps[mpp.point].append(mpp)
        return grouped_mps

    def _get_angle_targets(self, points: List[str]) -> Dict[str, List[str]]:
        return {p: self.angle_target_calculator.calculate(p) for p in points}

    @staticmethod
    def _calculate_cusps_ascmc(dt: datetime, config: HoroscopeConfig) -> tuple:
        return swe_api.get_tropical_houses_and_ascmc(
            dt, config.lat, config.lon, config.house_system
        )

    def _generate_aspects(
        self, angles: Dict[str, List[Angle]], configs: List[AspectsConfig]
    ) -> Dict[str, List[Aspect]]:

        aspects_dict = {}

        if self.angle_factory is None:
            return aspects_dict

        for p, angle_list in angles.items():
            for config in configs:
                asp_angles = self._generate_asp_family(config.angle)
                aspects = []

                for asp_angle in asp_angles:
                    orb = self._calculate_orb(p, asp_angle)
                    aspects += self.aspect_factory.find_aspects_list(
                        angle_list, orb, [asp_angle]
                    )
                aspects_dict[p] = aspects

        return aspects_dict

    @staticmethod
    def _calculate_orb(point: str, angle: int) -> float:
        if angle in [30, 60, 300, 330]:
            return 6 if point in LUMINARIES else 4
        elif angle in [0, 90, 120, 180, 360]:
            return 10 if point in LUMINARIES else 8
        elif angle in [150, 210]:
            return 5 if point in LUMINARIES else 3
        else:
            return 8 if point in LUMINARIES else 6

    @staticmethod
    def _generate_asp_family(root: float) -> List[float]:
        if root == 0:
            root = 360
        return [multiple for multiple in range(0, 361, root)]

    @staticmethod
    def _transform_cusps(
        dt: datetime, config: HoroscopeConfig, cusps: List[float], sid_asc: float
    ):
        ayanamsa = swe_api.get_ayanamsha(dt.year, dt.month, "LAHIRI")

        if config.house_system == Zodiac.PLACIDUS:
            return [(c - ayanamsa) % 360 for c in cusps]
        elif config.house_system == Zodiac.WHOLE_SIGN:
            asc_sign_start = int(sid_asc / 30) * 30
            return [(asc_sign_start + i * 30) % 360 for i in range(12)]
