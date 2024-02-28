from typing import Any, Callable, List

import numpy as np
from scipy.signal import argrelextrema

from astrotoolz.core.events.astro_event import (
    DeclinationExtreme,
    ExtremeEvent,
    LatitudeExtreme,
    SpeedExtreme,
)
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.util.logger_base import LoggerBase


class ExtremeEventFactory(LoggerBase):

    def __init__(self, event_types: List[type]):
        super().__init__()
        self.event_types = event_types

    def create_events(self, mps: List[MappedPosition]) -> List[ExtremeEvent]:
        events = []
        for event_type in self.event_types:
            if not issubclass(event_type, ExtremeEvent):
                continue

            attribute = self._event_type_to_attribute(event_type)

            self._logger.info(f"Generating {attribute} extreme events")

            events += self._create_events(
                self._find_local_extrema(mps, attribute, np.greater),
                event_type,
                f"{attribute} local max",
            )

            events += self._create_events(
                self._find_local_extrema(mps, attribute, np.less),
                event_type,
                f"{attribute} local min",
            )

            events += self._create_events(
                self._find_closest_to_zero(mps, attribute),
                event_type,
                f"{attribute} zero",
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

    @staticmethod
    def _create_events(
        extremes: List[MappedPosition], event_type: type, type: str
    ) -> List[ExtremeEvent]:
        return [event_type(mp.dt, type, mp) for mp in extremes]

    @staticmethod
    def _find_local_extrema(
        mapped_positions: List[MappedPosition],
        attribute: str,
        comparator: Callable[[Any, Any], bool],
    ) -> List[MappedPosition]:
        values = [getattr(mp.base_position, attribute) for mp in mapped_positions]
        values_array = np.array(values)
        extrema_indices = argrelextrema(values_array, comparator)
        extrema = [mapped_positions[i] for i in extrema_indices[0]]
        return extrema

    @staticmethod
    def _find_closest_to_zero(
        mapped_positions: List[MappedPosition],
        attribute: str,
    ) -> List[MappedPosition]:
        values = [
            getattr(mp.base_position, attribute).decimal for mp in mapped_positions
        ]
        values_array = np.array(values)
        signs = np.sign(values_array)
        sign_diff = np.diff(signs)
        shift_indices = np.where(sign_diff != 0)[0]
        return [mapped_positions[i] for i in shift_indices]
