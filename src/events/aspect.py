from dataclasses import dataclass
from itertools import groupby
from typing import Optional, Tuple, List
from core.angle import Angle, get_all_angles_in_date_range
from events.astro_event import AstroEvent
from datetime import datetime, timedelta


@dataclass
class Aspect(AstroEvent):
    angle: Angle
    asp_str: str
    asp_diff: int

    def __repr__(self):
        orb_start, orb_end = self.orb(2)
        #return f"aspect at {self.angle}, {self.asp_str} ({self.asp_diff})\n Orb of 2 starts at: {orb_start}, ends at: {orb_end}"
        return f'{self.time}\t{self.angle.pos1.name}\t{self.asp_str} [{self.asp_diff}] vs {self.angle.pos2.name}'
    
    
    def orb(self, orb_value: int) -> Tuple[datetime, datetime]:
    # Determine the direction of movement for each planet
        if self.angle.pos1.speed * self.angle.pos2.speed > 0:
            # Both planets are moving in the same direction
            combined_speed = abs(self.angle.pos1.speed - self.angle.pos2.speed)
        else:
            # Planets are moving in opposite directions
            combined_speed = abs(self.angle.pos1.speed + self.angle.pos2.speed)
        
        # Calculate the number of days for the aspect to move out of orb
        days_out_of_orb = orb_value / combined_speed
        
        # Calculate the start and end dates based on the exact aspect time
        start_date = self.angle.time - timedelta(days=days_out_of_orb)
        end_date = self.angle.time + timedelta(days=days_out_of_orb)
        
        return start_date, end_date


def get_aspects(angles: List[Angle]):
    return filter(lambda asp: asp is not None, [get_aspect(angle) for angle in angles if angle])


def get_aspect(angle: Angle) -> Optional[Aspect]:
    asp = calculate_aspect(angle.diff)

    if asp is None:
        return None

    asp_str, asp_diff = asp
    return Aspect(angle.time, angle, asp_str, asp_diff)


def calculate_aspect(diff: float) -> Optional[Tuple[str, int]]:
    """Return the aspect associated with the given angle difference."""
    ASPECTS = {
        0: "conjunction",
        60: "sextile",
        72: "quintile",
        90: "square",
        120: "trine",
        144: "quintile",
        150: "inconjunct",
        180: "opposition",
        216: "quintile",
        240: "trine",
        270: "square",
        288: "quintile",
        300: "sextile"
    }

    # rounded is 1 orb
    rounded = round(diff)
    asp = ASPECTS.get(rounded, None)

    if diff < 0 or diff > 360 or asp is None:
        return None

    return (asp, rounded)


def get_aspects_best_fit(angles: List[Angle]) -> List[Aspect]:
    aspects = get_aspects(angles)

    groups = groupby(aspects, key=lambda asp: asp.asp_diff)

    aspects = []

    for key, group in groups:
        min_diff_asp = min(group, key=lambda asp: abs(
            asp.angle.diff - asp.asp_diff))

        aspects.append(min_diff_asp)

    return aspects


def get_all_aspects(planet: str, start: datetime, end: datetime, interval: int) -> List[Aspect]:
    angles = get_all_angles_in_date_range(planet, start, end, interval)
    aspects = get_aspects_best_fit(angles)
    return aspects


def get_all_aspects(angles: List[Angle]) -> List[Aspect]:
    aspects = get_aspects_best_fit(angles)
    return aspects
