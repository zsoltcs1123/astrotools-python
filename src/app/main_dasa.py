from datetime import datetime
from core.base_position import BasePosition
from core.position_factory import PositionFactory
from timezonefinder import TimezoneFinder
import pytz
from tools.dasa.dasa import DasaLevel
from tools.dasa.dasa_factory import generate_dasas
from tools.dasa.dasa_printer import print_dasas
from tools.horoscope.horoscope import Horoscope
from util.geocoder import Geocoder
from objects.points import MEAN_NODE, MOON
from zodiac.mapped_position import MappedPosition


if __name__ == "__main__":
    position_factory = PositionFactory(MEAN_NODE)
    dt = datetime(1992, 7, 21, 3, 20)

    geocoder = Geocoder("ca667b3bd3ba943ee0ba411a150d443f")
    lat, lon = geocoder.get_lat_lon("Kecskemet", "Hungary")
    tf = TimezoneFinder()
    tz_name = tf.certain_timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)

    moon_position = position_factory.create_position(MOON, utc_dt)

    # moon_position = BasePosition(utc_dt, "moon", 7.669722, 0, 0, 0, 0)
    moon_mapped = MappedPosition(moon_position)

    res = generate_dasas(moon_mapped, DasaLevel.Bhukti)
    print(moon_mapped.sidereal_lon)
    print(moon_mapped.sidereal_pos)
    print(moon_mapped.nakshatra.name)
    print(moon_mapped.nakshatra.lord)
    print(moon_mapped.nakshatra.degree_range)

    print_dasas(res)
