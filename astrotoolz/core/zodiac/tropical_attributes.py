from dataclasses import dataclass

import astrotoolz.core.zodiac.division as zodiac
from astrotoolz.core.units.degree import Degree


@dataclass
class TropicalAttributes:
    lon: Degree
    zodiacal_position: str
    sign: zodiac.Sign
    sign_ruler: str
    decan: zodiac.Decan
    term: zodiac.Term
    house: int
