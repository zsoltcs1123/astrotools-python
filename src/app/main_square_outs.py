from datetime import datetime
import pytz
from core.enums import CoordinateSystem
from tools.gann.square_out_generator import find_lon_increases, generate_square_outs

from util.common import measure


def sq():
    dt = datetime(2007, 11, 7, 0, 0, 0, tzinfo=pytz.utc)
    degrees = 747
    square_outs = generate_square_outs(dt, degrees, ["mars"], CoordinateSystem.HELIO)

    for p, so in square_outs.items():
        print(f"{p} [{so[0].lon}]")
        print(f"{so[1].dt} [{so[1].lon}]")
        print("------")


def lons():
    dt = datetime(2023, 9, 11, 0, 0, 0, tzinfo=pytz.utc)
    degrees = 90
    lon_increases = find_lon_increases(
        dt, degrees, 5, ["mercury"], CoordinateSystem.HELIO
    )

    for p, sl in lon_increases.items():
        print(f"{p} [{sl[0][0].lon}]")
        for sq in sl:
            print(f"{sq[1].dt} [{sq[1].lon}]")
            print("------")


if __name__ == "__main__":
    measure(sq)
