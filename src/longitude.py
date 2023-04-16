from datetime import datetime
from skyfield.api import load
from skyfield.framelib import ecliptic_frame


def planet_longitude_now(planet_name: str) -> float:
    return planet_longitude(planet_name, datetime.now())


def planet_longitude(planet_name: str, dt: datetime):
    # Load the ephemeris file
    eph = load('de421.bsp')

    # Get the position of planet at a specific time
    planet = eph[convert_planet_name(planet_name)]
    earth = eph['earth']

    ts = load.timescale()
    time = ts.utc(dt.year, dt.month, dt.day,
                  dt.hour, dt.minute, dt.second)

    planet_position = earth.at(time).observe(planet)

    lat, lon, distance = planet_position.frame_latlon(ecliptic_frame)

    # Return the longitude
    return lon


def convert_planet_name(planet_name: str) -> str:
    unchanged = ['sun', 'moon', 'mercury', 'venus', 'mars']
    return planet_name if planet_name in unchanged else planet_name + ' barycenter'
