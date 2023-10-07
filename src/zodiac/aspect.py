from dataclasses import dataclass
from itertools import groupby
from typing import Optional, Tuple, List
from zodiac.angle import Angle, get_all_angles
from zodiac.astro_event import AstroEvent
from datetime import datetime


@dataclass
class Aspect(AstroEvent):
    angle: Angle
    asp_str: str
    asp_diff: int

    def __repr__(self):
        return f"aspect at {self.angle}, {self.asp_str} ({self.asp_diff})"


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
    angles = get_all_angles(planet, start, end, interval)
    aspects = get_aspects_best_fit(angles)
    return aspects


def get_all_aspects(angles: List[Angle]) -> List[Aspect]:
    aspects = get_aspects_best_fit(angles)
    return aspects
