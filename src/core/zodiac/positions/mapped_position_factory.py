from core.positions.root_position import RootPosition
from core.zodiac.positions.mapped_geo_position import MappedGeoPosition


def create_mapped_geo_position(root_position: RootPosition) -> MappedGeoPosition:
    return MappedGeoPosition(
        root_position,
    )
