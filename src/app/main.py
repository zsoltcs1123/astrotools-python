from out.transit_table_printer import TransitTablePrinter
from util.common import measure
from util.geocoder import Geocoder
from datetime import datetime
from core.planetary_position import PlanetaryPosition as pp
from zodiac.mapped_planetary_position import MappedPlanetaryPosition as mpp
from events.astro_event import get_astro_events
from core.angle import get_all_angles
from events.aspect import get_all_aspects
from out.file import to_text_file
from core.planets import PLANETS
from itertools import groupby
from zodiac.horoscope import Horoscope
from out.horoscope_printer import HoroscopePrinter

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

    start = datetime(2023, 10, 21)
    end = datetime(2023, 11, 21)
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

    to_text_file('All oct 21 - sep 21.md', str)

if __name__ == "__main__":
    from timezonefinder import TimezoneFinder 
    import pytz
    
    geocoder = Geocoder("ca667b3bd3ba943ee0ba411a150d443f")
    lat, lon = geocoder.get_lat_lon("fort lauderdale", "USA")
    
    tf = TimezoneFinder()
    tz_name = tf.certain_timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_name)
    dt = datetime(1995, 1, 8, 1, 0)
    local_dt = tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    
    natal_horoscope = Horoscope(utc_dt, lat, lon, 'BB')
    utc_now = datetime.now(pytz.utc)
    utc_now_horoscope = Horoscope(utc_now, lat, lon, 'UTC_NOW')
    
    transit_table = natal_horoscope.generate_transit_table(utc_now_horoscope)
    
    transit_table_printer = TransitTablePrinter(transit_table)
    transit_table_printer.print_to_console()
    
    #horoscope_printer = HoroscopePrinter(natal_horoscope)
    #horoscope_printer.print_to_markdown('BB.md')

    
  



    
