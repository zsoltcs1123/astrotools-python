from enum import Enum, auto

class HouseSystem(Enum):
    PLACIDUS = auto()
    WHOLE_SIGN = auto()
    
class Zodiac(Enum):
    TROPICAL = auto()
    SIDEREAL = auto()
    
class CoordinateSystem(Enum):
    GEO = auto()
    HELIO = auto()
