import pytz
import swisseph as swe
from datetime import datetime


def calculate_asc_mc(dt: datetime, lat: float, lon: float):
    # Convert the datetime to Julian Day
    jd = swe.julday(
        dt.year, dt.month, dt.day, dt.hour + dt.minute / 60 + dt.second / 3600
    )

    # Calculate sidereal time
    sidereal_time = swe.sidtime(jd) * 15  # Convert to degrees

    # Calculate Ascendant and Midheaven
    asc_mc = swe.houses_ex(jd, lat, lon, b"P")[
        1
    ]  # 'P' for Placidus, but we are only interested in Asc and MC

    ascendant = asc_mc[0]  # Ascendant
    midheaven = asc_mc[1]  # Midheaven

    return ascendant, midheaven


# Example usage
dt = datetime(2023, 12, 4, 14, 30, tzinfo=pytz.utc)  # Example date and time
lat, lon = 40.7128, -74.0060  # Example: New York City coordinates
ascendant, midheaven = calculate_asc_mc(dt, lat, lon)
print(f"Date and time: {dt}")
print(f"Ascendant: {ascendant}")
print(f"Midheaven: {midheaven}")
