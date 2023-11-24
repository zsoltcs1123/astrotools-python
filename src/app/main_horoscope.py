import pytz

from datetime import datetime
from timezonefinder import TimezoneFinder
from tools.horoscope.horoscope_config import HoroscopeConfig
from util.geocoder import Geocoder
from tools.horoscope.horoscope_factory import create_horoscope
from tools.horoscope.horoscope_printer import print_horoscope_to_console


def generate_nyc_horoscopes():
    start = datetime(2023, 11, 22, 9, 30)
    end = datetime(2023, 11, 13, 9, 30)

    geocoder = Geocoder("ca667b3bd3ba943ee0ba411a150d443f")
    lat, lon = geocoder.get_lat_lon("New York", "USA")
    tf = TimezoneFinder()
    tz_name = tf.certain_timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_name)
    local_start = tz.localize(start)
    utc_start = local_start.astimezone(pytz.utc)
    local_end = tz.localize(end)
    utc_end = local_end.astimezone(pytz.utc)

    config = HoroscopeConfig.default(lat, lon, f"NYC {local_start}")
    horoscope = create_horoscope(utc_start, config)

    print_horoscope_to_console(horoscope)


def me_horoscope():
    dt = datetime(1992, 7, 21, 3, 20)

    geocoder = Geocoder("ca667b3bd3ba943ee0ba411a150d443f")
    lat, lon = geocoder.get_lat_lon("Kecskemet", "Hungary")
    tf = TimezoneFinder()
    tz_name = tf.certain_timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)

    config = HoroscopeConfig.default(lat, lon, f"Zsolt {local_dt}")
    horoscope = create_horoscope(utc_dt, config)

    print_horoscope_to_console(horoscope)


if __name__ == "__main__":
    me_horoscope()
