from datetime import datetime
from core.longitude import get_tropical_longitude
from planet import PLANETS
from price.price import PriceArgs, longitude_to_prices
from time.timegen import calculate_intervals


dates = calculate_intervals(datetime(2023, 5, 1), datetime(2023, 6, 1), 1440)
prices_per_day = {}

for date in dates:
    lst = [(planet, longitude_to_prices(get_tropical_longitude(planet, date).degrees, planet,
            PriceArgs(1, 1, 360, 3960))[0].level) for planet in PLANETS if planet != 'moon']
    prices_per_day[date] = lst


with open('spx_prices_may.txt', 'w') as f:
    for key, value in prices_per_day.items():
        f.write(key.strftime('%Y-%m-%d %H:%M:%S\n'))
        f.write("-----------------\n")
        for v in prices_per_day[key]:
            f.write(f'{v[0]}: {v[1]}\n')
        f.write("\n")
