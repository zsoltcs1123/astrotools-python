from dataclasses import dataclass
from typing import Tuple
from core.angles.angle import Angle
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
