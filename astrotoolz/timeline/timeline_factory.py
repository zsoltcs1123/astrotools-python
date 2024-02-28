from typing import Dict, List, Type

from astrotoolz.core.angles.angle import Angle
from astrotoolz.core.angles.angle_factory import AngleFactory
from astrotoolz.core.angles.angle_target_calculator import AngleTargetCalculator
from astrotoolz.core.events.aspect import Aspect
from astrotoolz.core.events.astro_event import (
    AstroEvent,
)
from astrotoolz.core.events.factory.aspect_factory import AspectFactory
from astrotoolz.core.events.factory.extreme_event_factory import ExtremeEventFactory
from astrotoolz.core.events.factory.positional_event_factory import (
    PositionalEventFactory,
)
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.positions.factory.position_factory import PositionFactory
from astrotoolz.core.zodiac.mapped_geo_position import (
    MappedGeoPosition as MappedGeoPosition,
)
from astrotoolz.core.zodiac.mapped_position import MappedPosition as mp
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper
from astrotoolz.timeline.timeline import Timeline
from astrotoolz.timeline.timeline_config import (
    AspectsConfig,
    TimelineConfig,
)
from astrotoolz.util.logger_base import LoggerBase


class TimelineFactory(LoggerBase):

    def __init__(
        self,
        position_factory: PositionFactory,
        position_mapper: PositionMapper,
        angle_target_calculator: AngleTargetCalculator,
        angle_factory: AngleFactory,
        positional_event_factory: PositionalEventFactory,
        extreme_event_factory: ExtremeEventFactory,
        aspect_factory: AspectFactory,
    ):
        super().__init__()
        self.position_factory = position_factory
        self.position_mapper = position_mapper
        self.angle_target_calculator = angle_target_calculator
        self.angle_factory = angle_factory
        self.positional_event_factory = positional_event_factory
        self.extreme_event_factory = extreme_event_factory
        self.aspect_factory = aspect_factory

    def create_timeline(
        self,
        config: TimelineConfig,
    ) -> Timeline:

        bps = self._generate_bps(config)
        mps = self.position_mapper.map_positions(bps)

        events = []

        if self.positional_event_factory:
            events += self._generate_positional_events(
                config,
                mps,
            )

        if self.extreme_event_factory:
            events += self._generate_extreme_events(
                config,
                mps,
            )

        aspects = []

        if config.aspects:
            for aspc in config.aspects:
                angles = self._generate_angles(config, aspc, mps)
                aspects += self._generate_aspects(
                    aspc,
                    angles,
                )

        self._logger.debug(f"Identified {len(aspects)} aspects")
        return Timeline(events + aspects)

    def _generate_bps(
        self,
        config: TimelineConfig,
    ) -> List[BasePosition]:

        bps = []
        for point in config.points:
            self._logger.info(
                f"Generating {config.coordinate_system} positions for {point}"
            )
            bps += self.position_factory.create_positions(
                point, config.start_date, config.end_date, config.interval_minutes
            )
        return bps

    def _generate_positional_events(
        self,
        tl_config: TimelineConfig,
        mps: Dict[str, List[mp]],
    ) -> List[Type[AstroEvent]]:
        events = []
        for p, mp_list in mps.items():
            self._logger.info(
                f"Generating {tl_config.coordinate_system} positional events for {p}"
            )
            events += self.positional_event_factory.create_events(mp_list)
        return events

    def _generate_extreme_events(
        self,
        tl_config: TimelineConfig,
        mps: Dict[str, List[mp]],
    ) -> List[AstroEvent]:
        events = []
        for p, mp_list in mps.items():
            self._logger.info(
                f"Generating {tl_config.coordinate_system} extreme events for {p}"
            )
            events += self.extreme_event_factory.create_events(
                mp_list,
            )
        return events

    def _generate_angles(
        self,
        tl_config: TimelineConfig,
        asp_config: AspectsConfig,
        mps: List[mp],
    ) -> List[Angle]:
        self._logger.info("Generating angles")
        grouped_mps = {}

        for mp in mps:
            if mp.point not in grouped_mps:
                grouped_mps[mp.point] = [mp]
            else:
                grouped_mps[mp.point].append(mp)
        mps = grouped_mps

        targets = self._get_angle_targets(tl_config, asp_config)
        return self.angle_factory.create_angles_list(
            grouped_mps,
            targets,
        )

    def _get_angle_targets(
        self,
        tl_config: TimelineConfig,
        asp_config: AspectsConfig,
    ) -> Dict[str, List[str]]:
        ret = {}

        for p in tl_config.points:
            if not asp_config.targets:
                targets = self.angle_target_calculator.calculate(p)
                ret[p] = targets
            else:
                ret[p] = asp_config.targets
            self._logger.debug(f"Identified angle targets for {p}: {ret[p]}")

        return ret

    def _generate_aspects(
        self,
        asp_config: AspectsConfig,
        angles: List[Angle],
    ) -> List[Aspect]:
        self._logger.info("Calculating aspects...")
        asp_values = []
        if not asp_config.family:
            asp_values.append(asp_config.angle)
        else:
            asp_values = self._generate_asp_family(asp_config.angle)
        return self.aspect_factory.find_exact_aspects(
            angles, asp_config.orb, asp_values
        )

    def _generate_asp_family(self, root: float) -> List[float]:
        return [multiple for multiple in range(0, 361, root)]
