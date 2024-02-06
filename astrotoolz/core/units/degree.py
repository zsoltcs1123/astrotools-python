from dataclasses import dataclass

from astrotoolz.core.units.dms import DMS


@dataclass
class Degree:
    dms: DMS
    decimal: float
    _precision = 4  # TODO make this configurable

    def __str__(self):
        return f"{self.decimal:.3f}° [{self.dms}]"

    def str_decimal(self):
        return f"{self.decimal:.3f}°"

    def __lt__(self, other):
        if not isinstance(other, Degree):
            return NotImplemented
        return self.decimal < other.decimal

    def __gt__(self, other):
        if not isinstance(other, Degree):
            return NotImplemented
        return self.decimal > other.decimal

    def __eq__(self, other: "Degree"):
        if not isinstance(other, Degree):
            return NotImplemented

        diff = round(self.decimal - other.decimal, self._precision)

        return diff == 0

    def __ne__(self, other: "Degree", decimals: int = 4):
        return not self.__eq__(other, decimals)
