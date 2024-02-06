from astrotoolz.core.positions.geo_position import GeoPosition
from astrotoolz.core.zodiac.mapped_geo_position import MappedGeoPosition
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper


class GeoMapper(PositionMapper):

    def map_position(self, position: GeoPosition) -> MappedGeoPosition:

        return MappedGeoPosition(
            position,
            self.map_tropical_attributes(position),
            self.map_vedic_attributes(position),
        )
