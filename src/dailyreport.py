from datetime import datetime
from angle import get_all_angles_multi
from aspects.aspectcalc import get_aspects_best_fit
from planet import PLANETS
from price import PriceArgs, aspects_to_prices
from markdowngen import to_md_file
from util import measure


def generate_daily_reports(start: datetime, end: datetime) -> None:
    asps = []
    for planet in PLANETS:
        angles = get_all_angles_multi(planet, start, end, get_interval(planet))
        aspects = get_aspects_best_fit(angles)
        asps += aspects

    sorted_aspects = sorted(asps, key=lambda a: a.angle.time)
    mapped = map_prices(sorted_aspects)

    to_md_file(mapped, f"d.{start.strftime('%Y-%m-%d')}.md")


def get_interval(planet: str) -> int:
    if planet == 'moon' or planet == 'mercury':
        return 30
    elif planet == 'venus' or planet == 'sun':
        return 60
    else:
        return 120


def map_prices(aspects):
    return {asp: aspects_to_prices(asp, PriceArgs(8, 4, 360, 1440)) for asp in aspects}


if __name__ == "__main__":
    measure(lambda: generate_daily_reports(
        datetime(2023, 4, 10), datetime(2023, 4, 17)))
