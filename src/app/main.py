from core.util import measure
from datetime import datetime
from core.planetary_position import PlanetaryPosition


def main():
    start = datetime(2023, 9, 1)
    end = datetime(2023, 9, 30)
    interval = 60 * 24
    pos = PlanetaryPosition.from_datetime_range('mercury', start, end, interval)

    for p in pos:
        print(p)
        print('------------')

if __name__ == "__main__":
    measure(lambda: main())
