import datetime

from core.angle import get_all_angles_multi
from core.aspects.aspectcalc import get_aspects_best_fit
from core.aspects.aspectgen import Aspect, get_aspects
from md.markdowngen import to_md_file
from price.price import PriceArgs, aspects_to_prices
from core.util import measure

start = datetime.datetime(2023, 1, 1, 0, 0, 0)
end = datetime.datetime(2023, 12, 31, 0, 0, 0)


def get_aspects():
    angles = get_all_angles_multi("mercury", start, end, 30)
    aspects = get_aspects_best_fit(angles)
    return sorted(aspects, key=lambda a: a.angle.time)


def map_prices(aspects):
    return {asp: aspects_to_prices(asp, PriceArgs(8, 4, 360, 1440)) for asp in aspects}


if __name__ == "__main__":
    measure(lambda: to_md_file(map_prices(get_aspects(),), "2023 Mercury.md"))
