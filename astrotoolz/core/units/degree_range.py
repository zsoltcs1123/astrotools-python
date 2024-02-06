from dataclasses import dataclass

from astrotoolz.core.units.degree import Degree


@dataclass
class DegreeRange:
    start: Degree
    """Inclusive"""
    end: Degree
    """Exclusive"""

    def __contains__(self, value: float) -> bool:
        return self.start.decimal <= value < self.end.decimal

    def progress(self, value: float) -> float:
        return (value - self.start.decimal) / (self.end.decimal - self.start.decimal)
