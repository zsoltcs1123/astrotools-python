from typing import List
from out.file import to_text_file
from zodiac.degree_converter import float_to_zodiacal
from tools.horoscope import Horoscope


def _generate_str(horoscopes: List[Horoscope], points_filter: List[str] = [], aspects_filter: List[str] = []):
    str = ''
    for horoscope in horoscopes:
        str += f"Name: {horoscope.name}"
        str += f"\nDate and Time: {horoscope.dt}"
        str += f"\nLongitude: {horoscope.lon}"
        str += f"\nLatitude: {horoscope.lat}"
        str += f"\nHouse System: {horoscope.house_system}"
        str += f"\nZodiac System: {horoscope.zodiac_system}"
        str += f"\nCoordinate System: {horoscope.coord_system}"
        str += "\n\nPoints:\n--------\n"
        str += "{:<10}{:<3}{:<10}{:<10}{:<10}{:<10}".format(
            "Name", "", "Degrees", "House", "Term", "Tarot")
        for point in horoscope.points:
            if (point.position.name in points_filter):
                continue
            str += f"\n{point.position.name:<10}{(' R' if point.retrograde else ''):<3}{float_to_zodiacal(point.position.lon):<10}{point.house(horoscope.cusps):<10}{point.term.name:<10}{point.decan.name:<10}"

        str += "\n\nAspects:\n--------"
        for k, v in horoscope.aspects.items():
            if not bool(v) or k in aspects_filter:
                continue
            str += f"\n{k}\n-------"
            for asp in v:
                str += f"\n{asp.angle.print_no_time()}, {asp.asp_str}"
            str += '\n'

        str += '---------------------\n\n\n'
    return str


def print_horoscope_to_console(horoscope: Horoscope, points_filter: List[str] = [], aspects_filter: List[str] = []):
    print(_generate_str([horoscope], points_filter, aspects_filter))


def print_horoscopes_to_console(horoscopes: List[Horoscope], points_filter: List[str] = [], aspects_filter: List[str] = []):
    print(_generate_str(horoscopes, points_filter, aspects_filter))


def print_horoscope_to_file(horoscope: Horoscope, filename: str, points_filter: List[str] = [], aspects_filter: List[str] = []):
    to_text_file(_generate_str(
        filename, [horoscope], points_filter, aspects_filter))


def print_horoscopes_to_file(horoscopes: List[Horoscope], filename: str, points_filter: List[str] = [], aspects_filter: List[str] = []):
    to_text_file(filename, _generate_str(
        horoscopes, points_filter, aspects_filter))
