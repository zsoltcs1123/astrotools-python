
from dataclasses import dataclass
from datetime import datetime
from typing import List
from core.longitude import get_tropical_longitude
from core.position import Position
from zodiac.division import Decan, Term, get_decan, get_term


@dataclass
class MappedPosition(Position):
    decan: Decan
    term: Term


def map_divisions(planet: str, date: datetime) -> MappedPosition:
    lon = get_tropical_longitude(planet, date)
    decan = get_decan(lon.degrees)
    term = get_term(lon.degrees)
    return MappedPosition(date, planet, lon, decan, term)