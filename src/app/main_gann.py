from datetime import datetime
import pytz
from core.enums import CoordinateSystem
from objects.points import PLANETS, SUN, MOON, SN, NN
from tools.gann.angle_table import AngleTable
from tools.gann.square_out_generator import find_lon_increases, generate_square_outs

from util.common import measure
from util.dictionary_printer import print_dict_as_table


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


def angles():
    dt = datetime(2023, 9, 11, 0, 0, 0, tzinfo=pytz.utc)
    planets = [p for p in PLANETS if p not in [SUN, MOON, SN, NN]]
    angle_table = AngleTable(dt, planets, CoordinateSystem.HELIO)

    for p in angle_table.mps:
        print(f"{p.point} [{p.base_position.lon.str_decimal()}]")

    print_dict_as_table(
        angle_table.angles,
        lambda angle: abs(angle.circular_diff),
        lambda obj, key: obj.target.point == key,
    )


if __name__ == "__main__":
    measure(angles)
