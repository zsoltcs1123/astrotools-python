import datetime
from skyfield.api import load
from skyfield.framelib import ecliptic_frame


def planet_longitude_now(planet_name):
    return planet_longitude(planet_name, datetime.datetime.now())


def planet_longitude(planet_name, date):
    # Load the ephemeris file
    eph = load('de421.bsp')

    # Get the position of planet at a specific time
    planet = eph[convert_planet_name(planet_name)]
    earth = eph['earth']

    ts = load.timescale()
    time = ts.utc(date.year, date.month, date.day,
                  date.hour, date.minute, date.second)

    planet_position = earth.at(time).observe(planet)

    lat, lon, distance = planet_position.frame_latlon(ecliptic_frame)

    # Return the longitude
    return lon


def convert_planet_name(planet_name):
    unchanged = ['sun', 'moon', 'mercury', 'venus', 'mars']
    return planet_name if planet_name in unchanged else planet_name + ' barycenter'
