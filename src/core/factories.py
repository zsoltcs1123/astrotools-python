from datetime import datetime
from typing import Callable, Dict, List
from core.angles.angle import Angle
from core.enums import CoordinateSystem
from core.events.aspects.aspect import Aspect
from core.events.astro_event import AstroEvent
from core.positions.base_position import BasePosition
from core.positions.position_factory_config import PositionFactoryConfig
from core.zodiac.positions.mapped_position import MappedPosition


PositionsFactory = Callable[[PositionFactoryConfig], List[BasePosition]]
PositionFactory = Callable[[str, datetime, CoordinateSystem], BasePosition]

MappedPositionFactory = Callable[[BasePosition], MappedPosition]
MappedPositionsFactory = Callable[[List[BasePosition]], List[MappedPosition]]

EventFactory = Callable[[List[MappedPosition], List[type]], List[AstroEvent]]

AngleFactory = Callable[
    [Dict[str, List[MappedPosition]], Dict[str, List[str]]], List[Angle]
]

AspectFactory = Callable[[List[Angle], float, List[int]], List[Aspect]]
