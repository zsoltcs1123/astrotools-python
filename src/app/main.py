from core.util import measure
from datetime import datetime
from core.planetary_position import PlanetaryPosition as pp
from core.mapped_planetary_position import MappedPlanetaryPosition as mpp
from zodiac.astro_event import get_astro_events


def main():
    start = datetime(2023, 10, 1)
    end = datetime(2023, 10, 10)
    interval = 1
    pos = pp.from_datetime_range('mercury', start, end, interval)
    mapped = mpp.from_planetary_positions(pos)
    events = get_astro_events(mapped)

    for e in events:
        print(e)
        print('------------')

if __name__ == "__main__":
    measure(lambda: main())
