from datetime import datetime
import pytz
from core.enums import CoordinateSystem
from tools.gann.square_out_generator import find_lon_increases, generate_square_outs

from util.common import measure


def sq():
    dt = datetime(2021, 4, 14, 0, 0, 0, tzinfo=pytz.utc)
    degrees = 648
    square_outs = generate_square_outs(
        dt, degrees, ["mercury", "venus", "mars"], CoordinateSystem.HELIO
    )

    for p, so in square_outs.items():
        print(f"{p} [{so[0].lon}]")
        print(f"{so[1].dt} [{so[1].lon}]")
        print("------")


def lons():
    dt = datetime(2021, 4, 14, 0, 0, 0, tzinfo=pytz.utc)
    degrees = 90
    lon_increases = find_lon_increases(
        dt, degrees, 4, ["mercury"], CoordinateSystem.HELIO
    )

    for p, sl in lon_increases.items():
        print(f"{p} [{sl[0][0].lon}]")
        for sq in sl:
            print(f"{sq[1].dt} [{sq[1].lon}]")
            print("------")


if __name__ == "__main__":
    measure(lons)
