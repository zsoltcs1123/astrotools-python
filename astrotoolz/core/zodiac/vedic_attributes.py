from dataclasses import dataclass

import astrotoolz.core.zodiac.division as zodiac
from astrotoolz.core.units.degree import Degree


@dataclass
class VedicAttributes:
    lon: Degree
    zodiacal_position: str
    sign: zodiac.Sign
    sign_ruler: str
    nakshatra: zodiac.Nakshatra
    nakshatra_ruler: str
    house: int
