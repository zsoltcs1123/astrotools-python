import swisseph as swe
from datetime import datetime
from typing import Tuple
from core.enums import HouseSystem
from functools import lru_cache


def _get_julian_date(dt: datetime) -> float:
    """Convert a datetime object to Julian date."""
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 + dt.second/3600)


def _calculate_xx(planet_name: str, dt: datetime, flag: int) -> Tuple[float, float, float, float]:
    jd = _get_julian_date(dt)
    planet = getattr(swe, planet_name.upper())
    xx, _ = swe.calc_ut(jd, planet, flag)
    return xx


def _get_house_system_code(house_system: HouseSystem) -> str:
    if house_system == HouseSystem.PLACIDUS:
        return b'P'
    elif house_system == HouseSystem.WHOLE_SIGN:
        return b'W'
    else:
        raise ValueError("Unsupported house system")


def get_ecliptic_position(planet_name: str, dt: datetime) -> Tuple[float, float, float]:
    """Get the ecliptic longitude, latitude, and speed for a given planet and datetime."""
    xx = _calculate_xx(planet_name, dt, swe.FLG_SPEED)
    return xx[0], xx[1], xx[3]  # Longitude, Latitude, Speed


def get_equatorial_position(planet_name: str, dt: datetime) -> Tuple[float, float]:
    """Get the right ascension and declination for a given planet and datetime."""
    xx = _calculate_xx(planet_name, dt, swe.FLG_EQUATORIAL)
    return xx[0], xx[1]  # Right Ascension, Declination


def get_houses_and_ascmc(dt: datetime, lat: float, lon: float, house_system: HouseSystem, altitude: float = 0) -> tuple:
    jd_ut = _get_julian_date(dt)
    delta_t = swe.deltat(jd_ut)
    cusps, ascmc = swe.houses(jd_ut + delta_t, lat,
                              lon, _get_house_system_code(house_system))
    return cusps, ascmc


@lru_cache(maxsize=128)
def get_ayanamsha(year: int, month: int, ayanamsa: str):
    swe.set_sid_mode(getattr(swe, f'SIDM_{ayanamsa.upper()}'))
    jd = swe.julday(year, month, 1)  # Use the first day of the month for caching
    ayanamsha = swe.get_ayanamsa_ut(jd)
    return ayanamsha
