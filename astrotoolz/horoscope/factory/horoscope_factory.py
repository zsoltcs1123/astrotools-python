from datetime import datetime, timedelta
from typing import Dict, List, Optional

import astrotoolz.core.ephemeris.swisseph_api as swe_api
from astrotoolz.core.angles.angle import Angle
from astrotoolz.core.angles.angle_factory import AngleFactory
from astrotoolz.core.angles.angle_target_calculator import AngleTargetCalculator
from astrotoolz.core.enums import CoordinateSystem, HouseSystem, Zodiac
from astrotoolz.core.events.aspect import Aspect
from astrotoolz.core.events.factory.aspect_factory import AspectFactory
from astrotoolz.core.points import ANGULARS, ASC, MC
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.positions.factory.position_factory import PositionFactory
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper
from astrotoolz.horoscope.factory.horoscope_factory_config import HoroscopeFactoryConfig
from astrotoolz.horoscope.horoscope import Horoscope
from astrotoolz.horoscope.horoscope_config import HoroscopeConfig
from astrotoolz.horoscope.vedic_horoscope import VedicHoroscope
from astrotoolz.timeline.aspect_config import AspectsConfig
from astrotoolz.util.common import group_by
from astrotoolz.util.interval import calculate_intervals


class HoroscopeFactory:

    def __init__(
        self,
        config: HoroscopeFactoryConfig,
        position_factory: PositionFactory,
        position_mapper: PositionMapper,
        angle_target_calculator: Optional[AngleTargetCalculator],
        angle_factory: Optional[AngleFactory],
        aspect_factory: Optional[AspectFactory],
    ):
        self.config = config
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

        if config.house_system is None:
            config.house_system = HouseSystem.WHOLE_SIGN

        cusps, ascmc = (
            self._calculate_cusps_ascmc(dt, config)
            if any(point in ANGULARS for point in config.points)
            else ([], [])
        )

        mapped_positions = self._generate_positions(dt, config, ascmc, cusps)
        previous_mapped_positions = self._generate_positions(
            dt - timedelta(days=1), config, ascmc, cusps
        )

        grouped_mapped_positions = group_by(mapped_positions, lambda mp: mp.point)

        angle_targets = self.angle_target_calculator.calculate_dict(
            config.points, config.points
        )
        angle_targets = {k: v for k, v in angle_targets.items() if k in config.points}

        angles = self.angle_factory.create_angles_dict(
            grouped_mapped_positions, angle_targets
        )

        aspects = self._generate_aspects_dict(angles, config.aspects)
        for p, asp_list in aspects.items():
            self.position_mapper.map_aspects(asp_list, [config.zodiac])

        if config.zodiac == Zodiac.TROPICAL:
            return Horoscope(
                dt,
                self.config.coord_system,
                self.config.node_calc,
                config,
                mapped_positions,
                previous_mapped_positions,
                angles,
                aspects,
                cusps,
            )
        else:
            if ASC in config.points:
                mp_asc = next(mp for mp in mapped_positions if mp.point == ASC)
                cusps = self._transform_cusps(
                    dt, config, cusps, mp_asc.vedic.lon.decimal
                )
            return VedicHoroscope(
                dt,
                self.config.coord_system,
                self.config.node_calc,
                config,
                mapped_positions,
                previous_mapped_positions,
                angles,
                aspects,
                cusps,
            )

    @staticmethod
    def _calculate_cusps_ascmc(dt: datetime, config: HoroscopeConfig) -> tuple:
        return swe_api.get_tropical_houses_and_ascmc(
            dt, config.lat, config.lon, config.house_system
        )

    def _generate_positions(
        self, dt: datetime, config: HoroscopeConfig, ascmc: tuple, cusps: tuple
    ) -> List[BasePosition]:
        positions = []
        for point in config.points:
            bp = self._create_bp(point, dt, ascmc)
            bp = (
                self.position_mapper.map_position(bp, [config.zodiac], cusps)
                if config.zodiac
                else bp
            )
            positions.append(bp)
        return positions

    def _create_bp(self, point: str, dt: datetime, ascmc: tuple) -> BasePosition:
        if point == ASC:
            return self.position_factory.create_angular(point, dt, ascmc[0])
        elif point == MC:
            return self.position_factory.create_angular(point, dt, ascmc[1])
        else:
            return self.position_factory.create_position(point, dt)

    def _generate_aspects_dict(
        self, angles: Dict[str, List[Angle]], configs: List[AspectsConfig]
    ) -> Dict[str, List[Aspect]]:

        aspects_dict = {}

        if self.angle_factory is None:
            return aspects_dict

        for p, angle_list in angles.items():
            for config in configs:
                asp_angles = config.generate_asp_family()
                aspects = []

                for asp_angle in asp_angles:
                    orb = config.orb_calculator.calculate_orb(p, asp_angle)
                    aspects += self.aspect_factory.find_aspects_list(
                        angle_list, orb, [asp_angle]
                    )
                aspects_dict[p] = aspects

        return aspects_dict

    @staticmethod
    def _transform_cusps(
        dt: datetime, config: HoroscopeConfig, cusps: List[float], sid_asc: float
    ):
        ayanamsa = swe_api.get_ayanamsha(dt.year, dt.month, "LAHIRI")

        if config.house_system == HouseSystem.PLACIDUS:
            return [(c - ayanamsa) % 360 for c in cusps]
        elif config.house_system == HouseSystem.WHOLE_SIGN:
            asc_sign_start = int(sid_asc / 30) * 30
            return [(asc_sign_start + i * 30) % 360 for i in range(12)]
