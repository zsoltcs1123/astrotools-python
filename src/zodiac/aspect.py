from dataclasses import dataclass
from itertools import groupby
from typing import Optional, Tuple, List
from zodiac.angle import Angle, get_all_angles_multiproc
from zodiac.astro_event import AstroEvent
from datetime import datetime



@dataclass
class Aspect(AstroEvent):
    angle: Angle
    asp_str: str
    asp_diff: int
    
    def __init__(self, angle: Angle, asp_str: str, asp_diff: int):
        self.time = angle.time
        self.angle = angle
        self.asp_str = asp_str
        self.asp_diff = asp_diff

    def __hash__(self):
        return hash((self.angle, self.asp_str, self.asp_diff))

    def __eq__(self, other):
        if not isinstance(other, Aspect):
            return False
        return self.angle == other.angle and self.asp_str == other.asp_str and self.asp_diff == other.asp_diff

    def __repr__(self):
        return f"{self.angle}, {self.asp_str} ({self.asp_diff})"


def get_aspects(angles: List[Angle]):
    return filter(lambda asp: asp is not None, [get_aspect(angle) for angle in angles if angle])


def get_aspect(angle: Angle) -> Optional[Aspect]:
    asp = calculate_aspect(angle.diff)

    if asp is None:
        return None

    asp_str, asp_diff = asp
    return Aspect(angle, asp_str, asp_diff)


def calculate_aspect(diff: float) -> Optional[Tuple[str, int]]:
    """Return the aspect associated with the given angle difference."""
    ASPECTS = {
        0: "conjunction",
        60: "sextile",
        72: "quintile",
        90: "square",
        120: "trine",
        144: "quintile",
        180: "opposition",
        216: "quintile",
        240: "trine",
        270: "square",
        288: "quintile",
        300: "sextile"
    }

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

def calculate_all_aspects(planet: str, start: datetime, end: datetime, interval: int) -> List[Aspect]:
    angles = get_all_angles_multiproc(planet, start, end, interval)
    aspects = get_aspects_best_fit(angles)
    return aspects
