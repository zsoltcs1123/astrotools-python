from datetime import datetime
import multiprocessing
from typing import List
from core.util import measure
from out.file import to_text_file
from timegen.interval import calculate_intervals
from tv.script import generate_decans_progressions
from zodiac.event import get_decan_changes, get_progressions
from zodiac.mapped_position import map_divisions


def map_multi(planet: str, dates: List[datetime]):
    args = [(planet, t) for t in dates]

    with multiprocessing.Pool() as pool:
        return pool.starmap(map_divisions, args)


def main():
    dates = calculate_intervals(
        datetime(2023, 11, 15), datetime(2023, 12, 1), 1)

    lst = map_multi("moon", dates)

    decans = get_decan_changes(lst)
    progs = get_progressions(lst)

    timestamps = decans + progs

    lines = []

    for d in decans:
        lines.append(100)

    for p in progs:
        lines.append(50)

    timestamps_joined = " ".join(
        list(map(lambda x: f'{x.tv_timestamp()},', timestamps)))[:-1]

    lines_joined = " ".join(
        list(map(lambda x: f'{str(x)},', lines)))[:-1]

    script = generate_decans_progressions(
        "Moon Decans Oct 1-15", timestamps_joined, lines_joined)

    to_text_file("timestamps_moon_nov.txt", script)


if __name__ == "__main__":
    measure(lambda: main())
