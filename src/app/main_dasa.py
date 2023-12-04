from datetime import datetime
from core import swisseph_api
from core.base_position import BasePosition
from timezonefinder import TimezoneFinder
import pytz
from core.position_factory import create_position
from tools.dasa.dasa import DasaLevel
from tools.dasa.dasa_factory import generate_dasas
from tools.dasa.dasa_printer import print_dasas
from util.geocoder import Geocoder
from objects.points import MEAN_NODE, MOON
from zodiac.mapped_position import MappedPosition

POSITION_FACTORY = PositionFactory(MEAN_NODE)


def aix_dasa():
    utc_dt = datetime(2023, 9, 15, 16, 25, 47, tzinfo=pytz.utc)
    moon_position = POSITION_FACTORY.create_position(MOON, utc_dt)
    ayanamsa = swisseph_api.get_ayanamsha(utc_dt.year, utc_dt.month, "LAHIRI")
    # moon_position = BasePosition(utc_dt, "moon", 149.186694 + ayanamsa, 0, 0, 0, 0)

    moon_mapped = MappedPosition(moon_position)

    res = generate_dasas(moon_mapped, DasaLevel.Sookshma)
    print(moon_mapped.vedic.lon)
    print(moon_mapped.vedic.position)
    print(moon_mapped.vedic.nakshatra.name)
    print(moon_mapped.vedic.nakshatra.ruler)
    print(moon_mapped.vedic.nakshatra.degree_range)

    current_date = datetime.now().astimezone(pytz.utc)
    current_maha_dasa = [d for d in res if d.start_date <= current_date <= d.end_date][
        0
    ]
    current_bhukti = [
        d
        for d in current_maha_dasa.sub_dasas
        if d.start_date <= current_date <= d.end_date
    ]

    print_dasas(current_bhukti)


def me_dasa():
    dt = datetime(1992, 7, 21, 3, 20)

    geocoder = Geocoder("ca667b3bd3ba943ee0ba411a150d443f")
    lat, lon = geocoder.get_lat_lon("Kecskemet", "Hungary")
    tf = TimezoneFinder()
    tz_name = tf.certain_timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)

    utc_dt = datetime(2023, 9, 15, 16, 25, 47, tzinfo=pytz.utc)

    moon_position = create_position(MOON, utc_dt)

    moon_position = BasePosition(utc_dt, "moon", 7.669722, 0, 0, 0, 0)
    moon_mapped = MappedPosition(moon_position)

    res = generate_dasas(moon_mapped, DasaLevel.Pratyantar)
    print(moon_mapped.vedic.lon)
    print(moon_mapped.vedic.position)
    print(moon_mapped.vedic.nakshatra.name)
    print(moon_mapped.vedic.nakshatra.ruler)
    print(moon_mapped.vedic.nakshatra.degree_range)


if __name__ == "__main__":
    aix_dasa()
