from dataclasses import dataclass
from core.positions.geo_position import GeoPosition
from core.zodiac.positions.mapped_geo_position import MappedPosition


@dataclass
class LinkedPosition(MappedPosition):
    _previous_lp: "LinkedPosition"

    def __init__(self, previous_lp: "LinkedPosition"):
        self._previous_lp = previous_lp

    @property
    def get_root_attr_index(self) -> str:
        if self._previous_lp is None:
            return ""

        return self._get_index(
            self.root_position.speed.decimal,
            self._previous_lp.root_position.speed.decimal,
        )

    @property
    def declination_index(self) -> str:
        if self._previous_lp is None or not isinstance(self.root_position, GeoPosition):
            return ""

        return self._get_index(
            self.root_position.dec.decimal, self._previous_lp.root_position.dec.decimal
        )

    @property
    def phase_index(self) -> str:
        if self._previous_lp is None:
            return ""

        return self._get_index(self.phase.decimal, self._previous_lp.phase.decimal)

    @property
    def latitude_index(self) -> str:
        if self._previous_lp is None:
            return ""

        return self._get_index(
            self.root_position.lat.decimal, self._previous_lp.root_position.lat.decimal
        )

    def _get_index(self, current_value: float, previous_value: float) -> str:
        diff = round(current_value - previous_value, 4)

        if diff == 0:
            return "="
        elif current_value > previous_value:
            return "+"
        elif current_value < previous_value:
            return "-"
