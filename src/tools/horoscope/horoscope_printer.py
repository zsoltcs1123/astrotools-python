from typing import List
from out.file import to_text_file
from tools.horoscope.horoscope import Horoscope


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
        str += "{:<10}{:<3}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
            "Name",
            "",
            "Tropical",
            "House",
            "Ruler",
            "Term",
            "Tarot",
            "Sidereal",
            "Ruler",
        )
        for point in horoscope.points:
            if point.base_position.name in points_filter:
                continue

            str += (
                f"\n{point.base_position.name:<10}"
                f"{(' R' if point.retrograde else ''):<3}"
                f"{point.tropical_pos:<10}"
                f"{point.house(horoscope.cusps):<10}"
                f"{point.sign.modern_ruler:<10}"
                f"{point.term.name:<10}"
                f"{point.decan.name:<10}"
                f"{point.sidereal_pos:<10}"
                f"{point.sidereal_sign.vedic_ruler:<10}"
                # f"{point.nakshatra.name:<20}"
                # f"{point.nakshatra.lord:<10}"
            )

        str += "\n\nAspects:\n--------"
        for k, v in horoscope.aspects.items():
            if not bool(v) or k in aspects_filter:
                continue
            str += f"\n{k}\n-------"
            for asp in v:
                str += f"\n{asp.angle.print_no_time()}, {asp.type}"
            str += "\n"

        str += "---------------------\n\n\n"
    return str


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
