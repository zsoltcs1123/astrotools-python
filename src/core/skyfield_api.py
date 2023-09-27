from datetime import datetime
from skyfield.api import load
from skyfield.framelib import ecliptic_frame

KP_AYANAMSA_CORRECTION = 23.77


def get_tropical_longitude(planet_name: str, dt: datetime):
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

def get_declination(planet_name:str, dt: datetime):
    # Load the ephemeris file
    eph = load('de421.bsp')

    planet = eph[convert_planet_name(planet_name)]
    earth = eph['earth']
    
    ts = load.timescale()
    time = ts.utc(dt.year, dt.month, dt.day,
                  dt.hour, dt.minute, dt.second)

    astrometric = earth.at(time).observe(planet)
    ra, dec, distance = astrometric.radec()

    return dec

# does not belong in here

def convert_to_kp_ayanamsa(longitude: float) -> float:
    kp_ayanamsa = longitude - KP_AYANAMSA_CORRECTION

    if kp_ayanamsa < 0:
        kp_ayanamsa += 360

    return kp_ayanamsa


def convert_planet_name(planet_name: str) -> str:
    unchanged = ['sun', 'moon', 'mercury', 'venus', 'mars']
    return planet_name if planet_name in unchanged else planet_name + ' barycenter'
