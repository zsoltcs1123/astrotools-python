from datetime import datetime
import pytz
from core.enums import CoordinateSystem
from tools.squares.square_out_generator import generate_square_outs
import json

from util.common import measure


def sq():
    dt = datetime(2021, 4, 14, 0, 0, 0, tzinfo=pytz.utc)
    degrees = 61.07
    square_outs = generate_square_outs(
        dt, degrees, ["moon", "mercury", "venus", "mars"], CoordinateSystem.HELIO
    )

    for p, so in square_outs.items():
        print(f"{p} [{so[0].lon}]")
        print(f"{so[1].dt} [{so[1].lon}]")
        print("------")


if __name__ == "__main__":
    measure(sq)
