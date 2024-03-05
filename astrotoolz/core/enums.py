from enum import Enum, auto


class EnumBase(Enum):
    @classmethod
    def from_string(cls, s: str):
        try:
            return cls[s.upper()]
        except KeyError:
            raise ValueError(f"'{s}' is not a valid {cls.__name__}")


class NodeCalc(EnumBase):
    MEAN = "mean"
    TRUE = "true"

    def swe_flag(self) -> str:
        return "MEAN_NODE" if self == NodeCalc.MEAN else "TRUE_NODE"

    def __str__(self):
        return self.name


class HouseSystem(EnumBase):
    PLACIDUS = auto()
    WHOLE_SIGN = auto()

    def __str__(self):
        return self.name


class Zodiac(EnumBase):
    TROPICAL = auto()
    SIDEREAL = auto()

    def __str__(self):
        return self.name


class CoordinateSystem(EnumBase):
    GEO = "geo"
    HELIO = "helio"

    def __str__(self):
        return self.name
