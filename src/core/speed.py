from skyfield.api import Topos, load
from datetime import datetime

def get_planetary_speed(planet_name: str, dt: datetime):
    # Load the ephemeris file
    eph = load('de421.bsp')

    # Get the position of planet at a specific time
    planet = eph[planet_name]
    earth = eph['earth']

    ts = load.timescale()
    t1 = ts.utc(dt.year, dt.month, dt.day-1, dt.hour, dt.minute, dt.second)
    t2 = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    # Get the positions at t1 and t2
    p1 = earth.at(t1).observe(planet).apparent().ecliptic_latlon()[1]
    p2 = earth.at(t2).observe(planet).apparent().ecliptic_latlon()[1]

    # Calculate the speed in degrees per day
    speed = (p2.degrees - p1.degrees)

    return speed


if __name__ == "__main__":
    # Get the current date and time
    now = datetime.now()
    planet = 'mercury'
    # Call the function with the current date and time
    speed = get_planetary_speed(planet, now)
    print(f"The speed of {planet} today is {speed} degrees per day.")


