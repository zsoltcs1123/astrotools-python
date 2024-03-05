from dataclasses import dataclass
from typing import Optional

from astrotoolz.core.enums import CoordinateSystem, NodeCalc


@dataclass
class HoroscopeFactoryConfig:
    coord_system: CoordinateSystem
    include_aspects: bool
    node_calc: Optional[NodeCalc]
