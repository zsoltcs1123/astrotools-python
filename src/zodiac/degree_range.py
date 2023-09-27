from dataclasses import dataclass


@dataclass
class DegreeRange:
    start: float
    """Inclusive"""
    end: float
    """Exclusive"""

    def __init__(self, start: float, end: float):
        self.start = start
        self.end = end

    def __contains__(self, value: float) -> bool:
        return self.start <= value < self.end
