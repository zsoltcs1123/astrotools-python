from dataclasses import dataclass
from core.degree import Degree


@dataclass
class DegreeRange:
    start: Degree
    """Inclusive"""
    end: Degree
    """Exclusive"""

    @classmethod
    def from_degrees(cls, start: Degree, end: Degree):
        return cls(start, end)

    @classmethod
    def from_floats(cls, start: float, end: float):
        return cls(Degree.from_decimal(start), Degree.from_decimal(end))

    def __contains__(self, value: float) -> bool:
        return self.start.dec <= value < self.end.dec

    def progress(self, value: float) -> float:
        return (value - self.start.dec) / (self.end.dec - self.start.dec)
