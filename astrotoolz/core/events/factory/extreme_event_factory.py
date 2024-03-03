from typing import Any, Callable, List

import numpy as np
from scipy.signal import argrelextrema

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.events.astro_event import (
    DeclinationExtreme,
    ExtremeEvent,
    LatitudeExtreme,
    SpeedExtreme,
)
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.util.logger_base import LoggerBase


class ExtremeEventFactory(LoggerBase):

    def __init__(self, event_types: List[type]):
        super().__init__()
        self.event_types = event_types

    def create_events(self, mps: List[BasePosition]) -> List[ExtremeEvent]:
        events = []
        for event_type in self.event_types:
            if not issubclass(event_type, ExtremeEvent):
                continue

            attribute = self._event_type_to_attribute(event_type)

            self._logger.info(f"Generating {attribute} extreme events")

            events += self._create_events(
                self._find_local_extrema(mps, attribute, np.greater),
                event_type,
                f"{attribute.capitalize()}LocalMax",
            )

            events += self._create_events(
                self._find_local_extrema(mps, attribute, np.less),
                event_type,
                f"{attribute.capitalize()}LocalMin",
            )

            events += self._create_events(
                self._find_closest_to_zero(mps, attribute),
                event_type,
                f"{attribute.capitalize()}Zero",
            )
        return events

    @staticmethod
    def _event_type_to_attribute(event_type) -> str:
        if event_type == DeclinationExtreme:
            return "dec"
        elif event_type == LatitudeExtreme:
            return "lat"
        elif event_type == SpeedExtreme:
            return "speed"

    def _create_events(
        self,
        bps: List[BasePosition],
        event_type: type,
        type: str,
    ) -> List[ExtremeEvent]:
        return [event_type(type, bp) for bp in bps]

    @staticmethod
    def _find_local_extrema(
        positions: List[BasePosition],
        attribute: str,
        comparator: Callable[[Any, Any], bool],
    ) -> List[BasePosition]:
        values = [getattr(position, attribute) for position in positions]
        values_array = np.array(values)
        extrema_indices = argrelextrema(values_array, comparator)
        extrema = [positions[i] for i in extrema_indices[0]]
        return extrema

    @staticmethod
    def _find_closest_to_zero(
        positions: List[BasePosition],
        attribute: str,
    ) -> List[BasePosition]:
        values = [getattr(position, attribute).decimal for position in positions]
        values_array = np.array(values)
        signs = np.sign(values_array)
        sign_diff = np.diff(signs)
        shift_indices = np.where(sign_diff != 0)[0]
        return [positions[i] for i in shift_indices]
