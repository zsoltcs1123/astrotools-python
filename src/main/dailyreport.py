from datetime import datetime
from core.angle import get_all_angles_multi
from aspects.aspectcalc import get_aspects_best_fit
from planet import PLANETS
from price.price import PriceArgs, aspects_to_prices
from md.markdowngen import to_md_file
from util import measure


def generate_daily_reports(start: datetime, end: datetime) -> None:
    asps = []
    for planet in PLANETS:
        angles = get_all_angles_multi(planet, start, end, get_interval(planet))
        aspects = get_aspects_best_fit(angles)
        asps += aspects

    sorted_aspects = sorted(asps, key=lambda a: a.angle.time)
    mapped = map_prices(sorted_aspects)

    to_md_file(mapped, f"w.{start.strftime('%Y-%m-%d')}.spx.md")


def get_interval(planet: str) -> int:
    if planet == 'moon':
        return 1
    elif planet == 'mercury':
        return 30
    elif planet == 'venus' or planet == 'sun':
        return 60
    else:
        return 120


def map_prices(aspects):
    return {asp: aspects_to_prices(asp, PriceArgs(9, 4, 360, 3600)) for asp in aspects}


if __name__ == "__main__":
    measure(lambda: generate_daily_reports(
        datetime(2023, 5, 1), datetime(2023, 5, 8)))