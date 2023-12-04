from typing import List
from core.enums import HoroscopeType
from events.aspect import Aspect
from out.file import to_text_file
from tools.horoscope.horoscope import Horoscope


def print_horoscope_to_console(
    horoscope: Horoscope, points_filter: List[str] = [], aspects_filter: List[str] = []
):
    print(_generate_str([horoscope], points_filter, aspects_filter))


def print_horoscopes_to_console(
    horoscopes: List[Horoscope],
    points_filter: List[str] = [],
    aspects_filter: List[str] = [],
):
    print(_generate_str(horoscopes, points_filter, aspects_filter))


def print_horoscope_to_file(
    horoscope: Horoscope,
    filename: str,
    points_filter: List[str] = [],
    aspects_filter: List[str] = [],
):
    to_text_file(_generate_str(filename, [horoscope], points_filter, aspects_filter))


def print_horoscopes_to_file(
    horoscopes: List[Horoscope],
    filename: str,
    points_filter: List[str] = [],
    aspects_filter: List[str] = [],
):
    to_text_file(filename, _generate_str(horoscopes, points_filter, aspects_filter))


def _generate_str(
    horoscopes: List[Horoscope],
    points_filter: List[str] = [],
    aspects_filter: List[str] = [],
):
    str = ""
    for horoscope in horoscopes:
        str += f"Name: {horoscope.config.name}"
        str += f"\nDate and Time: {horoscope.dt}"
        str += f"\nLongitude: {horoscope.config.lon}"
        str += f"\nLatitude: {horoscope.config.lat}"
        str += f"\nHouse System: {horoscope.config.house_system}"
        str += f"\nCoordinate System: {horoscope.config.coord_system}"
        str += "\n\nPoints:\n--------\n"
        str += _get_headers(horoscope.config.type)()
        str += _get_values(horoscope.config.type)(horoscope, points_filter)

        str += "\n\nAspects:\n--------"
        for k, v in horoscope.aspects.items():
            if not bool(v) or k in aspects_filter:
                continue
            str += f"\n{k}\n-------"
            for asp in v:
                str += f"\n{_get_aspect_str(horoscope.config.type, asp)}, {asp.type} ({asp.direction})"
            str += "\n"

        str += "---------------------\n\n\n"
    return str


def _get_aspect_str(type: HoroscopeType, asp: Aspect):
    if type == HoroscopeType.TROPICAL:
        return asp.print_tropical_no_time()
    elif type == HoroscopeType.VEDIC:
        return asp.print_vedic_no_time()


def _get_headers(type: HoroscopeType):
    if type == HoroscopeType.TROPICAL:
        return _get_tropical_headers
    elif type == HoroscopeType.VEDIC:
        return _get_vedic_headers
    else:
        return _get_mixed_headers


def _get_values(type: HoroscopeType):
    if type == HoroscopeType.TROPICAL:
        return _get_tropical_values
    elif type == HoroscopeType.VEDIC:
        return _get_vedic_values
    else:
        return _get_mixed_values


def _get_tropical_headers() -> str:
    return "{:<10}{:<3}{:<10}{:<10}{:<10}{:<10}{:<10}{:<15}{:<15}".format(
        "Name",
        "",
        "Position",
        "House",
        "Ruler",
        "Term",
        "Tarot",
        "Speed",
        "Declination",
    )


def _get_tropical_values(horoscope: Horoscope, points_filter: List[str] = []) -> str:
    str = ""
    for mp in horoscope.mps:
        if mp.point in points_filter:
            continue

        str += (
            f"\n{mp.point:<10}"
            f"{(' R' if mp.retrograde else ''):<3}"
            f"{mp.tropical.position:<10}"
            f"{mp.tropical.house(horoscope.cusps):<10}"
            f"{mp.tropical.sign_ruler:<10}"
            f"{mp.tropical.term.name:<10}"
            f"{mp.tropical.decan.name:<10}"
            f"{f'{mp.base_position.speed.str_decimal()} ({mp.daily_speed_index})':<15}"
            f"{f'{mp.base_position.dec.str_decimal()} ({mp.daily_declination_index})':<15}"
        )
    return str


def _get_vedic_headers() -> str:
    return "{:<10}{:<3}{:<10}{:<10}{:<10}{:<20}{:<10}".format(
        "Name",
        "",
        "Position",
        "House",
        "Ruler",
        "Star",
        "Star Lord",
    )


def _get_vedic_values(horoscope: Horoscope, points_filter: List[str] = []) -> str:
    str = ""
    for mp in horoscope.mps:
        if mp.point in points_filter:
            continue

        str += (
            f"\n{mp.point:<10}"
            f"{(' R' if mp.retrograde else ''):<3}"
            f"{mp.vedic.position:<10}"
            f"{mp.vedic.house(horoscope.cusps):<10}"
            f"{mp.vedic.sign_ruler:<10}"
            f"{mp.vedic.nakshatra.name:<20}"
            f"{mp.vedic.nakshatra_ruler:<10}"
        )
    return str


def _get_mixed_headers() -> str:
    return "{:<10}{:<3}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<20}{:<10}".format(
        "Name",
        "",
        "Tropical",
        "House",
        "Ruler",
        "Term",
        "Tarot",
        "Sidereal",
        "Lord",
        "Star",
        "Star Lord",
    )


def _get_mixed_values(horoscope: Horoscope, points_filter: List[str] = []) -> str:
    str = ""
    for mp in horoscope.mps:
        if mp.point in points_filter:
            continue

        str += (
            f"\n{mp.point:<10}"
            f"{(' R' if mp.retrograde else ''):<3}"
            f"{mp.tropical.position:<10}"
            f"{mp.tropical.house(horoscope.cusps):<10}"
            f"{mp.tropical.sign_ruler:<10}"
            f"{mp.tropical.term.name:<10}"
            f"{mp.tropical.decan.name:<10}"
            f"{mp.vedic.position:<10}"
            f"{mp.vedic.sign_ruler:<10}"
            f"{mp.vedic.nakshatra.name:<20}"
            f"{mp.vedic.nakshatra.ruler:<10}"
        )
    return str
