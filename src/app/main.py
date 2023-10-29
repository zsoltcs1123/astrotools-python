from typing import List
import pytz
from timezonefinder import TimezoneFinder
from out.timeline_printer import TimelinePrinter
from tools.timeline import Timeline
from out.transit_table_printer import TransitTablePrinter
from util.common import measure
from util.geocoder import Geocoder
from datetime import datetime
from core.position import Position as pp
from zodiac.mapped_position import MappedPosition as mp
from events.astro_event import get_astro_events
from core.angle import get_all_angles_in_date_range
from events.aspect import get_all_aspects
from out.file import to_text_file
from points.planets import PLANETS
from itertools import groupby
from tools.horoscope import Horoscope
from out.horoscope_printer import print_horoscopes_to_console, print_horoscopes_to_file


def main():
    start = datetime(2023, 10, 1)
    end = datetime(2023, 10, 10)
    interval = 1
    pos = pp.from_datetime_range('mercury', start, end, interval)
    mapped = mp.from_planetary_positions(pos)
    events = get_astro_events(mapped)

    angles = get_all_angles_in_date_range('mercury', start, end, 1)
    aspects = get_all_aspects(angles)
    events += aspects

    events = sorted(events, key=lambda x: x.time)
    str = ""
    for e in events:
        str += e.__repr__() + '\n\n'
        print(e)
        print('------------')

    to_text_file('Mercury oct 1-10.md', str)

    start = datetime(2023, 10, 28)
    end = datetime(2023, 10, 29)
    interval = 1
    events = []
    str = ""

    planets = [planet for planet in PLANETS if planet != 'moon']
    for i, planet in enumerate(planets):
        print(f'calculating {planet}')
        pos = pp.from_datetime_range(planet, start, end, interval)
        mapped = mp.from_planetary_positions(pos)
        events += get_astro_events(mapped)
        angles = get_all_angles_in_date_range(planet, start, end, 1)
        aspects = get_all_aspects(angles)
        events += aspects

    events = sorted(events, key=lambda x: x.time)
    grouped_events = []
    for k, g in groupby(events, key=lambda x: x.time.date()):
        grouped_events.append(list(g))

    for group in grouped_events:
        formatted_date = group[0].time.strftime('%A, %b %d %Y')
        str += f'{formatted_date}:\n'
        str += ''.join([f'{i + 1}. {e.__repr__()} \n------------\n' for i,
                       e in enumerate(group)]) + '\n'

    to_text_file(
        f'All {start.strftime("%m.%d")} - {end.strftime("%m.%d")}.md', str)


def horoscope():

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
    
    horoscope_printer = HoroscopePrinter(natal_horoscope)
    horoscope_printer.print_to_console()

    transit_table_printer = TransitTablePrinter(transit_table)
    transit_table_printer.print_to_console()



def timeline():
    start = datetime(2023, 10, 28)
    end = datetime(2023, 11, 4)
    interval = 1
    
    timeline = Timeline(start, end, interval, PLANETS)
    timeline_printer = TimelinePrinter(timeline)
    timeline_printer.print_to_file('timeline.txt') 
    

def generate_nyc_horoscopes():
    start = datetime(2023, 10, 28, 9, 30)
    end = datetime(2023, 11, 4, 9, 30)
    
    geocoder = Geocoder("ca667b3bd3ba943ee0ba411a150d443f")
    lat, lon = geocoder.get_lat_lon('New York', "USA")
    tf = TimezoneFinder()
    tz_name = tf.certain_timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_name)
    local_start = tz.localize(start)
    utc_start = local_start.astimezone(pytz.utc)
    local_end = tz.localize(end)
    utc_end = local_end.astimezone(pytz.utc)
    
    horoscopes = Horoscope.from_datetime_range(utc_start, utc_end, 1440, lat, lon, 'New York')
    
    print_horoscopes_to_file(horoscopes, 'horoscopes.txt', aspects_filter=['ASC', 'MC', 'moon']) 
     
    

if __name__ == "__main__":
    #generate_nyc_horoscopes()
    timeline()
