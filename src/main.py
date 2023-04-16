
import datetime
import multiprocessing
import time

from angle import get_all_angles_multi, get_angles, get_angles_multi
from aspects.aspectcalc import get_aspects_best_fit
from aspects.aspectgen import Aspect, get_aspects
from markdowngen import aspect_map_to_markdown, to_md_file
from price import PriceArgs, aspects_to_prices

start = datetime.datetime(2023, 4, 1, 0, 0, 0)
end = datetime.datetime(2023, 5, 1, 0, 0, 0)


def get_aspects():
    angles = get_all_angles_multi("sun", start, end, 120)
    aspects = get_aspects_best_fit(angles)
    return aspects


def map_prices(aspects):
    return {asp: aspects_to_prices(asp, PriceArgs(10, 4, 360, 1440)) for asp in aspects}


def measure(func):
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    measure(lambda: to_md_file(map_prices(get_aspects(),), "April Sun.md"))
