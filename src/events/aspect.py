from dataclasses import dataclass
from typing import Tuple
from core.angle import Angle
from core.enums import AspectType
from events.astro_event import AstroEvent
from datetime import datetime, timedelta


DEFAULT_ASPECTS = [
    AspectType.CONJUNCTION,
    AspectType.OPPOSITION,
    AspectType.SQUARE,
    AspectType.TRINE,
    AspectType.SEXTILE,
    AspectType.INCONJUNCT,
    AspectType.QUINTILE,
]


@dataclass
class Aspect(AstroEvent):
    angle: Angle
    type: AspectType
    target_diff: int

    def __repr__(self):
        # return f"aspect at {self.angle}, {self.asp_str} ({self.asp_diff})\n Orb of 2 starts at: {orb_start}, ends at: {orb_end}"
        return f"{self.dt}\t{self.angle.source.point}\t{self.type.name.lower()} [{self.angle.abs_diff:.3f}] vs {self.angle.target.point}"

    def label(self):
        return f"{self.angle.source.point} {self.type.name.lower()} [{self.angle.abs_diff:.0f}] vs {self.angle.target.point}"

    def print_tropical_no_time(self):
        return f"{self.angle.source.point} [{self.angle.source.tropical.lon.decimal:.3f}], {self.angle.target.point} [{self.angle.target.tropical.lon.decimal:.3f}], {self.angle.abs_diff:.3f}"

    def print_vedic_no_time(self):
        return f"{self.source.point} [{self.source.vedic.lon.decimal:.3f}], {self.target.point} [{self.target.vedic.lon.decimal:.3f}], {self.diff:.3f}"

    def orb(self, orb_value: int) -> Tuple[datetime, datetime]:
        # Determine the direction of movement for each planet
        if self.angle.source.speed * self.angle.target.speed > 0:
            # Both planets are moving in the same direction
            combined_speed = abs(self.angle.source.speed - self.angle.target.speed)
        else:
            # Planets are moving in opposite directions
            combined_speed = abs(self.angle.source.speed + self.angle.target.speed)

        # Calculate the number of days for the aspect to move out of orb
        days_out_of_orb = orb_value / combined_speed

        # Calculate the start and end dates based on the exact aspect time
        start_date = self.angle.dt - timedelta(days=days_out_of_orb)
        end_date = self.angle.dt + timedelta(days=days_out_of_orb)

        return start_date, end_date
