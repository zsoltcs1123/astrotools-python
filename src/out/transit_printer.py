
from typing import List
from core.angle import Angle
from tools.transit import Transit
from zodiac.degree_converter import float_to_zodiacal


def _generate_str(transit: Transit, points_filter: List[str] = []):
    str = ''
    str += f"Name: {transit.natal_horoscope.name}"
    str += f"\nNatal Date and Time: {transit.natal_horoscope.dt}"
    str += f"\nTransit Date and Time: {transit.transit_horoscope.dt}"
    str += f"\nHouse System: {transit.natal_horoscope.house_system}"
    str += f"\nZodiac System: {transit.natal_horoscope.zodiac_system}"
    str += f"\nCoordinate System: {transit.natal_horoscope.coord_system}"
    str += "\n\nPoints:\n--------\n"
    str += "{:<10}{:<10}{:<10}{:<10}{:<10}".format(
        "Name", "Natal", "Transit", "Diff", "Transit house")
    
    transit_points = {mp.position.name : mp for mp in transit.transit_horoscope.points}
    for point in transit.natal_horoscope.points:
        if (point.position.name in points_filter):
            continue
        transit_point = transit_points[point.position.name]
        angle = Angle(point.position.dt, point.position, transit_point.position)
        str += f"\n{point.position.name:<10}{float_to_zodiacal(point.position.lon):<10}{float_to_zodiacal(transit_point.position.lon):<10}{round(angle.diff,3):<10}{transit_point.house(transit.natal_horoscope.cusps):<10}"
        
    str += '\n---------------------\n\n\n'
    return str

def print_transit_to_console(transit: Transit, points_filter: List[str] = []):
    print(_generate_str(transit, points_filter))