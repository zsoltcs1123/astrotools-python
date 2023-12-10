from datetime import datetime
import pytz
from tools.squares.square_out_generator import generate_square_outs
import json

from util.common import measure


def sq():
    dt = datetime(2021, 4, 14, 0, 0, 0, tzinfo=pytz.utc)
    degrees = 610.07
    square_outs = generate_square_outs(
        dt, degrees, ["sun", "moon", "mercury", "venus", "mars"]
    )

    for p, so in square_outs.items():
        print(f"{p} [{so[0].lon}]")
        print(f"{so[1].dt} [{so[1].lon}]")
        print("------")


if __name__ == "__main__":
    measure(sq)
