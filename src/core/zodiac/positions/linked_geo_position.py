from dataclasses import dataclass
from core.positions.root_position import RootPosition
from core.zodiac.positions.mapped_geo_position import MappedGeoPosition

from core.zodiac.positions.mapped_position import MappedPosition


@dataclass
class LinkedGeoPosition(MappedGeoPosition):
    pass
