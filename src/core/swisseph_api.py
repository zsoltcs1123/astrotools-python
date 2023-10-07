import swisseph as swe
from datetime import datetime
from typing import Tuple

def get_julian_date(dt: datetime) -> float:
    """Convert a datetime object to Julian date."""
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 + dt.second/3600)

def _calculate_xx(planet_name: str, dt: datetime, flag: int) -> Tuple[float, float, float, float]:
    jd = get_julian_date(dt)
    planet = getattr(swe, planet_name.upper())
    xx, _ = swe.calc_ut(jd, planet, flag)
    return xx

def get_ecliptic_position(planet_name: str, dt: datetime) -> Tuple[float, float, float]:
    """Get the ecliptic longitude, latitude, and speed for a given planet and datetime."""
    xx = _calculate_xx(planet_name, dt, swe.FLG_SPEED)
    return xx[0], xx[1], xx[3]  # Longitude, Latitude, Speed

def get_equatorial_position(planet_name: str, dt: datetime) -> Tuple[float, float]:
    """Get the right ascension and declination for a given planet and datetime."""
    xx = _calculate_xx(planet_name, dt, swe.FLG_EQUATORIAL)
    return xx[0], xx[1]  # Right Ascension, Declination


