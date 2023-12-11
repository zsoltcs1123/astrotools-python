from enum import Enum, auto


class HouseSystem(Enum):
    PLACIDUS = auto()
    WHOLE_SIGN = auto()

    def __str__(self):
        return self.name


class Zodiac(Enum):
    TROPICAL = auto()
    SIDEREAL = auto()

    def __str__(self):
        return self.name


class CoordinateSystem(Enum):
    GEO = auto()
    HELIO = auto()

    def __str__(self):
        return self.name


class AspectType(Enum):
    CONJUNCTION = 1
    OPPOSITION = 2
    SEXTILE = 3
    SQUARE = 4
    TRINE = 5
    QUINTILE = 6
    INCONJUNCT = 7

    def __str__(self):
        return self.name


class HoroscopeType(Enum):
    TROPICAL = auto()
    VEDIC = auto()
