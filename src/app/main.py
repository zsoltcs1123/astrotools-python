from util.common import measure
from datetime import datetime
from core.planetary_position import PlanetaryPosition as pp
from core.mapped_planetary_position import MappedPlanetaryPosition as mpp
from events.astro_event import get_astro_events
from core.angle import get_all_angles
from events.aspect import get_all_aspects
from out.file import to_text_file
from core.planet import PLANETS
from itertools import groupby

def main():
    start = datetime(2023, 10, 1)
    end = datetime(2023, 10, 10)
    interval = 1
    pos = pp.from_datetime_range('mercury', start, end, interval)
    mapped = mpp.from_planetary_positions(pos)
    events = get_astro_events(mapped)

    angles = get_all_angles('mercury', start, end, 1)
    aspects = get_all_aspects(angles)
    events += aspects

    events = sorted(events, key=lambda x: x.time)
    str = ""
    for e in events:
        str += e.__repr__() + '\n\n'
        print(e)
        print('------------')

    to_text_file('Mercury oct 1-10.md', str)


def all():

    start = datetime(2023, 10, 10)
    end = datetime(2023, 10, 20)
    interval = 1
    events = []
    str = ""

    planets = [planet for planet in PLANETS if planet != 'moon']
    for i, planet in enumerate(planets):
        print(f'calculating {planet}')
        pos = pp.from_datetime_range(planet, start, end, interval)
        mapped = mpp.from_planetary_positions(pos)
        events += get_astro_events(mapped)
        angles = get_all_angles(planet, start, end, 1)
        aspects = get_all_aspects(angles)
        events += aspects

    events = sorted(events, key=lambda x: x.time)
    grouped_events = []
    for k, g in groupby(events, key=lambda x: x.time.date()):
        grouped_events.append(list(g))
        
    for group in grouped_events:
        formatted_date = group[0].time.strftime('%A, %b %d %Y')
        str+= f'{formatted_date}:\n'
        str += ''.join([f'{i + 1}. {e.__repr__()} \n------------\n' for i, e in enumerate(group)]) + '\n'

    to_text_file('All oct 10-20.md', str)

if __name__ == "__main__":
    measure(lambda: all())



    
