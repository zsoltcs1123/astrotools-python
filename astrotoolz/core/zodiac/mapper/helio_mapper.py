from astrotoolz.core.positions.helio_position import HelioPosition
from astrotoolz.core.zodiac.mapped_helio_position import MappedHelioPosition
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper


class HelioMapper(PositionMapper):
    def map_position(self, position: HelioPosition) -> MappedHelioPosition:

        return MappedHelioPosition(
            position,
            self.map_tropical_attributes(position),
            self.map_vedic_attributes(position),
        )
