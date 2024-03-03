import logging
from datetime import datetime

import pytz
from timezonefinder import TimezoneFinder

from astrotoolz.core.enums import CoordinateSystem, NodeCalc
from astrotoolz.horoscope.factory.horoscope_factory_builder import (
    build_horoscope_factory,
)
from astrotoolz.horoscope.factory.horoscope_factory_config import (
    HoroscopeFactoryConfig,
)
from astrotoolz.horoscope.horoscope_config import HoroscopeConfig
from astrotoolz.horoscope.horoscope_printer import (
    print_horoscope_to_console,
    print_horoscopes_to_file,
)
from astrotoolz.util.geocoder import Geocoder

logging.basicConfig(level=logging.DEBUG)


def generate_nyc_horoscopes():
    start = datetime(2023, 12, 3, 14, 30, tzinfo=pytz.utc)
    end = datetime(2023, 12, 31, 14, 30, tzinfo=pytz.utc)

    geocoder = Geocoder("ca667b3bd3ba943ee0ba411a150d443f")
    lat, lon = geocoder.get_lat_lon("New York", "USA")

    tz_name = TimezoneFinder().certain_timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_name)
    config = HoroscopeConfig.default_tropical(lat, lon, f"NYC {start.astimezone(tz)}")

    horoscope_factory_config = HoroscopeFactoryConfig(
        CoordinateSystem.GEO, True, NodeCalc.MEAN
    )
    horoscope_factory = build_horoscope_factory(horoscope_factory_config)
    horoscopes = horoscope_factory.create_horoscopes(start, end, 1440, config)

    print_horoscopes_to_file(
        horoscopes, "nyc_horoscopes_dec_3_dec_30.txt", columns_filter=["House"]
    )


def me_horoscope():
    dt = datetime(1992, 7, 21, 3, 20)

    geocoder = Geocoder("ca667b3bd3ba943ee0ba411a150d443f")
    lat, lon = geocoder.get_lat_lon("Kecskemet", "Hungary")
    tf = TimezoneFinder()
    tz_name = tf.certain_timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)

    config = HoroscopeConfig.default_vedic(lat, lon, f"Zsolt {local_dt}")

    horoscope_factory_config = HoroscopeFactoryConfig(
        CoordinateSystem.GEO, True, NodeCalc.MEAN
    )
    horoscope_factory = build_horoscope_factory(horoscope_factory_config)
    horoscope = horoscope_factory.create_horoscope(utc_dt, config)

    print_horoscope_to_console(horoscope)


def aix_horoscope():
    utc_dt = datetime(2023, 9, 15, 4, 25, 47, tzinfo=pytz.utc)
    config = HoroscopeConfig.default_vedic(0, 0, f"AIX {utc_dt}")

    horoscope_factory_config = HoroscopeFactoryConfig(
        CoordinateSystem.GEO, True, NodeCalc.MEAN
    )
    horoscope_factory = build_horoscope_factory(horoscope_factory_config)
    horoscope = horoscope_factory.create_horoscope(utc_dt, config)

    print_horoscope_to_console(horoscope)


if __name__ == "__main__":
    me_horoscope()
