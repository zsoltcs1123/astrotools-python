from datetime import datetime
from longitude import planet_longitude
from price import PriceArgs, longitude_to_prices


mars_lon = planet_longitude("mars", datetime(2023, 5, 1))
prices = longitude_to_prices(
    mars_lon.degrees, "mars", PriceArgs(1, 1, 360, 1800))

print(prices)
