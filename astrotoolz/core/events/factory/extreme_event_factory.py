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
        self.event_types = event_types

    def create_events(self, mps: List[MappedPosition]) -> List[ExtremeEvent]:
        events = []
        for event_type in self.event_types:
            if not issubclass(event_type, ExtremeEvent):
                continue

            events += self._create_events(
                self._find_local_extrema(
                    mps, self._event_type_to_attribute(event_type), np.greater
                ),
                event_type,
                "max",
            )

            events += self._create_events(
                self._find_local_extrema(
                    mps, self._event_type_to_attribute(event_type), np.less
                ),
                event_type,
                "min",
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
        return [event_type(mp.dt, mp, type) for mp in extremes]

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
