
import datetime
import multiprocessing
import time

from angle import get_angles, get_angles_multi
from aspects.aspectcalc import get_aspects_best_fit
from aspects.aspectgen import get_aspects
from price import PriceArgs, aspect_to_prices

start = datetime.datetime(2023, 4, 1, 0, 0, 0)
end = datetime.datetime(2023, 5, 1, 0, 0, 0)


def print_aspects_with_prices():

    start_time = time.time()
    angles = get_angles_multi("moon", "pluto barycenter", start, end, 30)
    aspects = get_aspects(angles)

    aspects_with_prices = {}

    for asp in aspects:
        prices = aspect_to_prices(asp, PriceArgs(10, 4, 360, 1440))
        aspects_with_prices[asp] = prices

    end_time = time.time()

    for aspect, prices in aspects_with_prices.items():
        print(aspect, prices)

    elapsed_time = end_time - start_time  # Compute the elapsed time
    # Print the elapsed time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


def print_aspects():
    angles = get_angles_multi("mercury", "pluto barycenter", start, end, 30)
    aspects = get_aspects_best_fit(angles)

    for asp in aspects:
        print(asp)


def measure(func):
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    measure(print_aspects)
