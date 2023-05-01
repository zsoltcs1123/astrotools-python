from dataclasses import dataclass
from aspects.aspectgen import Aspect
from longitude import planet_longitude_now
import numpy as np
from typing import List


@dataclass
class Price:
    planet: str
    longitude: float
    level: float
    harmonic: int

    def __repr__(self):
        return f"Price(planet='{self.planet}', longitude={self.longitude:.3f}, level={self.level:.3f}, harmonic={self.harmonic})"


@dataclass
class PriceArgs:
    count: int
    harmonics: int
    full_circle: int
    offset: int


def aspects_to_prices(aspect: Aspect, price_args: PriceArgs) -> List[List[Price]]:
    prices_planet1 = longitude_to_prices(
        aspect.angle.pos1.lon, aspect.angle.pos1.planet, price_args)
    prices_planet2 = longitude_to_prices(
        aspect.angle.pos2.lon, aspect.angle.pos2.planet, price_args)
    prices_diff = longitude_to_prices(
        aspect.angle.diff, f"{aspect.angle.pos1.planet} {aspect.asp_str} {aspect.angle.pos2.planet}", price_args)

    return [prices_planet1, prices_planet2, prices_diff]


def longitude_to_prices(longitude: float, name: str, price_args: PriceArgs) -> List[Price]:
    prices = []

    step_size = (price_args.full_circle / price_args.harmonics)

    price = (round(longitude, 3) + price_args.offset)
    prices.append(Price(name, longitude, price, 0))

    # Add step_size degrees to each longitude count times
    for i in range(1, price_args.count):
        prices.append(
            Price(name, longitude, prices[i-1].level + step_size, i % price_args.harmonics))

    # Return the array of longitudes
    return prices
