from astrotoolz.core.units.degree import Degree
from astrotoolz.core.units.degree_range import DegreeRange
from astrotoolz.core.units.dms import DMS


def degree_from_decimal(dec: float):
    if not isinstance(dec, (int, float)):
        raise TypeError("Invalid argument type")
    dms = _convert_from_decimal_to_zodiacal(dec)
    return Degree(dms, dec)


def degree_from_dms(degrees: int, minutes: int, seconds: int):
    if degrees > 360 or minutes > 60 or seconds > 60:
        raise ValueError(f"Invalid degree values: {degrees}, {minutes}, {seconds}")
    dms = DMS(degrees, minutes, seconds)
    dec = _convert_from_zodiacal_to_decimal(dms)
    return Degree(dms, dec)


def degree_range_from_degrees(start: Degree, end: Degree):
    return DegreeRange(start, end)


def degree_range_from_floats(start: float, end: float):
    return DegreeRange(degree_from_decimal(start), degree_from_decimal(end))


def _convert_from_zodiacal_to_decimal(zodiacal):
    sec = 0 if zodiacal.seconds == 0 else 60 / zodiacal.seconds
    min = zodiacal.minutes if sec == 0 else zodiacal.minutes + 1 / sec
    degree = zodiacal.degrees if min == 0 else zodiacal.degrees + 1 / (60 / min)
    return degree


def _convert_from_decimal_to_zodiacal(dec):
    decimal_part = dec - int(dec)

    minute = decimal_part * 60
    minute_decimal_part = minute - int(minute)

    second = minute_decimal_part * 60

    return DMS(int(dec), int(minute), int(second))
