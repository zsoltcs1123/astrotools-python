from typing import Dict, List, Type

from astrotoolz.core.angles.angle import Angle
from astrotoolz.core.angles.angle_factory import AngleFactory
from astrotoolz.core.angles.angle_target_calculator import AngleTargetCalculator
from astrotoolz.core.enums import Zodiac
from astrotoolz.core.events.aspect import Aspect
from astrotoolz.core.events.astro_event import (
    AstroEvent,
    SiderealEvent,
    TropicalEvent,
)
from astrotoolz.core.events.factory.aspect_factory import AspectFactory
from astrotoolz.core.events.factory.extreme_event_factory import ExtremeEventFactory
from astrotoolz.core.events.factory.positional_event_factory import (
    PositionalEventFactory,
)
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.positions.factory.position_factory import PositionFactory
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

        self._logger.info(f"Timeline generation initiated with config: {config}")

        bps = self._generate_bps(config)
        premapped = False

        if self._premap_required(config):
            bps = self._premap_positions(bps, config)
            premapped = True

        grouped_bps = self._group_bps(bps)

        events = []

        if self.positional_event_factory:
            events += self._generate_positional_events(
                grouped_bps,
            )

        if self.extreme_event_factory:
            events += self._generate_extreme_events(
                grouped_bps,
            )

        aspects = []

        if config.aspects:
            for aspc in config.aspects:
                angles = self._generate_angles(config, aspc, grouped_bps)
                aspects += self._generate_aspects(
                    aspc,
                    angles,
                )

            if config.zodiacs:
                self.position_mapper.map_aspects(aspects, config.zodiacs)
            self._logger.debug(f"Identified {len(aspects)} aspects")

        if config.zodiacs and not premapped:
            self.position_mapper.map_events(events, config.zodiacs)

        return Timeline(events + aspects)

    @staticmethod
    def _premap_required(config: TimelineConfig) -> bool:
        return any(
            issubclass(event, TropicalEvent) or issubclass(event, SiderealEvent)
            for event in config.events
        )

    def _premap_positions(
        self, bps: List[BasePosition], config: TimelineConfig
    ) -> List[BasePosition]:
        zodiacs = []

        for e in config.events:
            if issubclass(e, TropicalEvent):
                zodiacs.append(Zodiac.TROPICAL)
            if issubclass(e, SiderealEvent):
                zodiacs.append(Zodiac.SIDEREAL)

        return self.position_mapper.map_positions(bps, zodiacs) if zodiacs else bps

    def _generate_bps(
        self,
        config: TimelineConfig,
    ) -> List[BasePosition]:

        bps = []
        for point in config.points:
            bps += self.position_factory.create_positions(
                point, config.start_date, config.end_date, config.interval_minutes
            )
        return bps

    @staticmethod
    def _group_bps(bps: List[BasePosition]) -> Dict[str, List[BasePosition]]:
        grouped_mps = {}
        for mpp in bps:
            if mpp.point not in grouped_mps:
                grouped_mps[mpp.point] = [mpp]
            else:
                grouped_mps[mpp.point].append(mpp)
        return grouped_mps

    def _generate_positional_events(
        self,
        mps: Dict[str, List[mp]],
    ) -> List[Type[AstroEvent]]:
        events = []
        for p, mp_list in mps.items():
            self._logger.info(f"Generating positional events for {p}")
            events += self.positional_event_factory.create_events(mp_list)
        return events

    def _generate_extreme_events(
        self,
        mps: Dict[str, List[mp]],
    ) -> List[AstroEvent]:
        events = []
        for p, mp_list in mps.items():
            self._logger.info(f"Generating extreme events for {p}")
            events += self.extreme_event_factory.create_events(
                mp_list,
            )
            self._logger.info(f"Identified {len(events)} extreme events")
        return events

    def _generate_angles(
        self,
        tl_config: TimelineConfig,
        asp_config: AspectsConfig,
        bps: Dict[str, List[BasePosition]],
    ) -> List[Angle]:
        targets = self._get_angle_targets(tl_config, asp_config)
        return self.angle_factory.create_angles_list(
            bps,
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

    @staticmethod
    def _generate_asp_family(root: float) -> List[float]:
        if root == 0:
            root = 360
        return [multiple for multiple in range(0, 361, root)]
