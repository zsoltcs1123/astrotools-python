from typing import List
from core.angle import Angle
from tools.transit import Transit
from tools.transit_table import TransitTable
from zodiac.degree_converter import float_to_zodiacal

import pandas as pd
import numpy as np


def _generate_transit_str(transit: Transit, points_filter: List[str] = []):
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


def _generate_transit_table_str(transit_table: TransitTable):
        str = ''
        # Extract diff from Angle objects and create DataFrame
        planets = list(transit_table.angles.keys())
        matrix = np.empty((len(planets), len(planets)), dtype=object)
        for i, planet1 in enumerate(planets):
            for j, planet2 in enumerate(planets):
                # Find the corresponding Angle or Aspect object
                angle = next((angle for angle in transit_table.angles[planet1] if angle.pos2.name == planet2), None)
                matrix[i, j] = round(angle.diff,3) if angle else ''
        angles_df = pd.DataFrame(matrix, index=planets, columns=planets)
        str +="Angles:\n"
        str +="-------\n"
        str += angles_df.to_string()
        str+= '\n'

        # Extract asp_diff from Aspect objects and create DataFrame
        matrix = np.empty((len(planets), len(planets)), dtype=object)
        for i, planet1 in enumerate(planets):
            for j, planet2 in enumerate(planets):
                # Find the corresponding Angle or Aspect object
                aspect = next((aspect for aspect in transit_table.aspects[planet1] if aspect.angle.pos2.name == planet2), None)
                matrix[i, j] = round(aspect.asp_diff,3) if aspect else ''
        aspects_df = pd.DataFrame(matrix, index=planets, columns=planets)
        str+="\nAspects:\n"
        str+="--------\n"
        str+=aspects_df.to_string()
        
        #aspects in text
        str += "\n\nAspects:\n--------"
        for k, v in transit_table.aspects.items():
            str += f"\n{k}\n-------"
            for asp in v:
                str += f"\n{asp.angle.print_no_time()}, {asp.asp_str}"
            str += '\n'

        str += '---------------------\n\n\n'
        
        return str

def print_transit_to_console(transit: Transit, points_filter: List[str] = []):
    transit_str = _generate_transit_str(transit, points_filter)
    transit_table_str = _generate_transit_table_str(transit.generate_transit_table())
    final_str = transit_str + '\n' + transit_table_str
    print(final_str)