from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.util.interval import calculate_intervals
from astrotoolz.util.logger_base import LoggerBase


class PositionFactory(LoggerBase, ABC):

    def create_positions(
        self, point: str, start: datetime, end: datetime, interval_minutes: int
    ) -> List[BasePosition]:
        self._logger.info(
            f"Generating positions for config: {point}, {start}, {end}, {interval_minutes}"
        )
        dts = calculate_intervals(start, end, interval_minutes)
        return [self.create_position(point, dt) for dt in dts]

    @abstractmethod
    def create_position(self, point: str, dt: datetime) -> BasePosition:
        pass
