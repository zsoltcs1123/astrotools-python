import swisseph as swe
from datetime import datetime

def get_julian_date(dt: datetime) -> float:
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 + dt.second/3600)

def compute_planet_attr(planet_name: str, dt: datetime, index: int, flag=0):
    jd = get_julian_date(dt)
    planet = getattr(swe, planet_name.upper())
    xx, _ = swe.calc_ut(jd, planet, flag)
    return xx[index]

get_planet_longitude = lambda planet_name, dt: compute_planet_attr(planet_name, dt, 0)
get_planet_speed = lambda planet_name, dt: compute_planet_attr(planet_name, dt, 3, swe.FLG_SPEED)
get_planet_declination = lambda planet_name, dt: compute_planet_attr(planet_name, dt, 1, swe.FLG_EQUATORIAL)

print(get_planet_longitude('mercury', datetime(2023,9,27)))
print(get_planet_speed('MERCURY', datetime(2023,9,27)))
print(get_planet_declination('MERCURY', datetime(2023,9,27)))
