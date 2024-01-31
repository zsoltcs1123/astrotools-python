from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from core.enums import NodeCalc
from core.positions.base_position import BasePosition
from core.positions.factory.geo_factory import GeoFactory
from core.positions.factory.helio_factory import HelioFactory
from util.console_logger import ConsoleLogger
from util.interval import calculate_intervals


class PositionFactory(ABC):
    def __init__(self):
        self._logger = ConsoleLogger(self.__name__)

    def create_positions(
        self, point: str, start: datetime, end: datetime, interval_minutes: int
    ) -> List[BasePosition]:
        self._logger.debug(
            f"Generating positions for config: {point}, {start}, {end}, {interval_minutes}"
        )
        dts = calculate_intervals(start, end, interval_minutes)
        return [self.create_position(point, dt) for dt in dts]

    @abstractmethod
    def create_position(self):
        pass

    @staticmethod
    def geo(node_calc: NodeCalc) -> GeoFactory:
        return GeoFactory(node_calc)

    @staticmethod
    def helio() -> HelioFactory:
        return HelioFactory()
