from datetime import datetime
import multiprocessing
from typing import List
from core.longitude import get_tropical_longitude
from core.util import measure
from out.file import to_text_file
from timegen.interval import calculate_intervals
from tv.moon_decans import generate
from zodiac.division import get_decan, get_term
from zodiac.event import DecanChange, TermChange
from zodiac.mapped_position import map_divisions


def map_multi(planet: str, dates: List[datetime]):
    args = [(planet, t) for t in dates]

    with multiprocessing.Pool() as pool:
        return pool.starmap(map_divisions, args)


def main():
    dates = calculate_intervals(
        datetime(2023, 6, 1), datetime(2023, 6, 30), 1)

    lst = map_multi("moon", dates)

    events = []

    for index, element in enumerate(lst):
        if index == 0:
            continue

        if (element.decan.id != lst[index - 1].decan.id):
            events.append(DecanChange(lst[index - 1], element))

    timestamps = []
    for event in events:
        timestamps.append(f'{event.tv_timestamp()},')

    joined = " ".join(timestamps)
    joined = joined[:-1]

    script = generate(joined)

    to_text_file("timestamps_moon_june.txt", script)


if __name__ == "__main__":
    measure(lambda: main())
